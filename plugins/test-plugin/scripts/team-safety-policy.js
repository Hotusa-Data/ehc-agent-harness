#!/usr/bin/env node

const eventName = process.argv[2] || "";

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
