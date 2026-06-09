#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const eventName = process.argv[2] || "";
const workspaceRoot = process.cwd();
const stateDir = path.join(__dirname, ".state");
const readStatePath = path.join(stateDir, "read-files.json");
const isWindows = process.platform === "win32";
const STATE_TTL_MS = 4 * 60 * 60 * 1000;

function readStdin() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
  });
}

function respond(output) {
  process.stdout.write(`${JSON.stringify(output)}\n`);
}

function normalizePath(value) {
  if (typeof value !== "string" || value.trim() === "") {
    return null;
  }

  const cleanValue = value.replace(/^file:\/\//, "");
  const absolutePath = path.isAbsolute(cleanValue)
    ? path.normalize(cleanValue)
    : path.resolve(workspaceRoot, cleanValue);

  return isWindows ? absolutePath.toLowerCase() : absolutePath;
}

// --- State management with TTL ---

function readState() {
  try {
    return JSON.parse(fs.readFileSync(readStatePath, "utf8"));
  } catch {
    return { files: {} };
  }
}

function writeState(state) {
  fs.mkdirSync(stateDir, { recursive: true });
  fs.writeFileSync(readStatePath, JSON.stringify(state, null, 2));
}

function purgeStaleEntries(state) {
  const now = Date.now();
  for (const [filePath, timestamp] of Object.entries(state.files)) {
    if (now - new Date(timestamp).getTime() > STATE_TTL_MS) {
      delete state.files[filePath];
    }
  }
}

function recordRead(filePath) {
  const normalized = normalizePath(filePath);
  if (!normalized) {
    return;
  }

  const state = readState();
  purgeStaleEntries(state);
  state.files[normalized] = new Date().toISOString();
  writeState(state);
}

function wasReadSinceLastModification(filePath) {
  const normalized = normalizePath(filePath);
  if (!normalized) {
    return false;
  }

  const state = readState();
  const readTime = state.files[normalized];
  if (!readTime) {
    return false;
  }

  try {
    const mtime = fs.statSync(normalized).mtime;
    return new Date(readTime) >= mtime;
  } catch {
    return true;
  }
}

// --- Input extraction helpers ---

function collectStrings(value, results = []) {
  if (typeof value === "string") {
    results.push(value);
    return results;
  }

  if (Array.isArray(value)) {
    for (const item of value) {
      collectStrings(item, results);
    }
    return results;
  }

  if (value && typeof value === "object") {
    for (const [key, nestedValue] of Object.entries(value)) {
      if (/path|file|uri/i.test(key)) {
        collectStrings(nestedValue, results);
      } else if (typeof nestedValue === "object") {
        collectStrings(nestedValue, results);
      }
    }
  }

  return results;
}

function extractCommand(input) {
  const command =
    input.command ||
    input.cmd ||
    input.shell_command ||
    input.tool_input?.command ||
    input.toolInput?.command ||
    input.input?.command ||
    input.arguments?.command ||
    "";

  return typeof command === "string" ? command : JSON.stringify(command);
}

function extractToolName(input) {
  return String(
    input.tool_name ||
      input.toolName ||
      input.tool ||
      input.name ||
      input.type ||
      input.tool_call?.name ||
      input.toolCall?.name ||
      input.tool_call?.type ||
      input.toolCall?.type ||
      ""
  );
}

function extractPotentialPaths(input) {
  const values = collectStrings(input);
  const paths = values
    .filter((value) => {
      if (/^https?:\/\//i.test(value)) {
        return false;
      }
      return /[\\/]/.test(value) || /\.[a-z0-9]{1,8}$/i.test(value);
    })
    .map(normalizePath)
    .filter(Boolean);

  return [...new Set(paths)];
}

// --- Command parsing ---

function splitCommandSegments(command) {
  const segments = [];
  let current = "";
  let quoteChar = null;
  let escaped = false;

  for (let i = 0; i < command.length; i++) {
    const ch = command[i];

    if (escaped) {
      current += ch;
      escaped = false;
      continue;
    }

    if (ch === "\\") {
      current += ch;
      escaped = true;
      continue;
    }

    if (quoteChar) {
      current += ch;
      if (ch === quoteChar) {
        quoteChar = null;
      }
      continue;
    }

    if (ch === '"' || ch === "'" || ch === "`") {
      current += ch;
      quoteChar = ch;
      continue;
    }

    if (ch === ";") {
      segments.push(current);
      current = "";
      continue;
    }

    if (ch === "&" && command[i + 1] === "&") {
      segments.push(current);
      current = "";
      i++;
      continue;
    }

    if (ch === "|") {
      if (command[i + 1] === "|") {
        i++;
      }
      segments.push(current);
      current = "";
      continue;
    }

    current += ch;
  }

  if (current.trim()) {
    segments.push(current);
  }

  return segments.map((s) => s.trim()).filter(Boolean);
}

// --- Shell command classifiers ---

function isPublishCommand(command) {
  const normalized = String(command).toLowerCase().replace(/[\r\n]+/g, " ");
  const segments = splitCommandSegments(normalized);

  const publishPatterns = [
    /\bgit(?:\.exe)?\b(?:\s+(?:-[a-z]\s+\S+|--[a-z0-9-]+(?:=\S+)?))*\s+push\b/,
    /\bnpm\s+publish\b/,
    /\byarn\s+(?:npm\s+)?publish\b/,
    /\bpnpm\s+publish\b/,
    /\bdocker(?:\.exe)?\s+push\b/,
    /\bgh\s+(?:pr\s+merge|repo\s+sync)\b/,
  ];

  return segments.some((segment) =>
    publishPatterns.some((pattern) => pattern.test(segment))
  );
}

function isDeletionCommand(command) {
  const normalized = String(command).toLowerCase().replace(/[\r\n]+/g, " ");
  const segments = splitCommandSegments(normalized);

  const deletionPatterns = [
    /^(?:sudo\s+)?rm(?:\.exe)?\s/,
    /^(?:sudo\s+)?rmdir(?:\.exe)?\s/,
    /^(?:sudo\s+)?remove-item\b/,
    /^(?:sudo\s+)?del(?:ete)?\s/,
    /^(?:sudo\s+)?erase\s/,
    /^(?:sudo\s+)?rd\s/,
    /^(?:sudo\s+)?trash\s/,
    /^(?:sudo\s+)?unlink\s/,
  ];

  return segments.some((segment) =>
    deletionPatterns.some((pattern) => pattern.test(segment))
  );
}

function isIndirectExecution(command) {
  const normalized = String(command).toLowerCase().replace(/[\r\n]+/g, " ");

  const indirectionPatterns = [
    /\b(?:bash|sh|zsh|dash|ksh|csh|fish)(?:\.exe)?\s+-c\b/,
    /\bpowershell(?:\.exe)?\s+.*-(?:command|encodedcommand)\b/,
    /\bpwsh(?:\.exe)?\s+.*-(?:command|encodedcommand)\b/,
    /\bnode(?:\.exe)?\s+-e\b/,
    /\bpython[23]?(?:\.exe)?\s+-c\b/,
    /\bruby(?:\.exe)?\s+-e\b/,
    /\bperl(?:\.exe)?\s+-e\b/,
    /\beval\s+/,
  ];

  return indirectionPatterns.some((pattern) => pattern.test(normalized));
}

// --- Tool classifiers ---

function isEditTool(toolName, input) {
  const name = toolName.toLowerCase();
  if (/write|edit|multiedit|applypatch|delete|rename|move/.test(name)) {
    return true;
  }

  const serialized = JSON.stringify(input).toLowerCase();
  return /"old_string"|"new_string"|"patch"|"diff"|"target_file"|"file_path"/.test(serialized);
}

// --- Main ---

async function main() {
  const rawInput = await readStdin();
  let input = {};
  try {
    input = rawInput.trim() ? JSON.parse(rawInput) : {};
  } catch {
    input = { rawInput };
  }

  if (eventName === "beforeShellExecution") {
    const command = extractCommand(input);

    if (isPublishCommand(command)) {
      respond({
        permission: "deny",
        user_message:
          "Team policy blocks publish and push commands from Cursor agents. A human must publish code.",
        agent_message:
          "Do not run publish or push commands. Repository and package publishing must be done by a human.",
      });
      return;
    }

    if (isDeletionCommand(command)) {
      respond({
        permission: "ask",
        user_message:
          "This command appears to delete files or directories. Team policy requires human approval.",
        agent_message:
          "Ask for explicit human approval before executing deletion commands.",
      });
      return;
    }

    if (isIndirectExecution(command)) {
      respond({
        permission: "ask",
        user_message:
          "This command runs code through a subshell or interpreter. Team policy requires human approval.",
        agent_message:
          "Ask for explicit human approval before running commands via subshell or interpreter invocation.",
      });
      return;
    }

    respond({ permission: "allow" });
    return;
  }

  if (eventName === "beforeReadFile") {
    for (const filePath of extractPotentialPaths(input)) {
      recordRead(filePath);
    }

    respond({ permission: "allow" });
    return;
  }

  if (eventName === "preToolUse") {
    const toolName = extractToolName(input);
    if (!isEditTool(toolName, input)) {
      respond({ permission: "allow" });
      return;
    }

    const paths = extractPotentialPaths(input);
    const existingUnreadPaths = paths.filter(
      (filePath) =>
        fs.existsSync(filePath) && !wasReadSinceLastModification(filePath)
    );

    if (existingUnreadPaths.length > 0) {
      respond({
        permission: "deny",
        user_message:
          "Team policy requires reading the current file contents before editing. Please read the target file first.",
        agent_message: `Read these files before editing them: ${existingUnreadPaths.join(", ")}`,
      });
      return;
    }

    respond({
      permission: "ask",
      user_message:
        "Team policy requires human approval before Cursor changes files.",
      agent_message:
        "Ask for explicit human approval before changing files.",
    });
    return;
  }

  respond({ permission: "allow" });
}

main().catch((error) => {
  respond({
    permission: "deny",
    user_message:
      "Team safety hook failed closed. Review the hook output before proceeding.",
    agent_message: error instanceof Error ? error.message : String(error),
  });
});
