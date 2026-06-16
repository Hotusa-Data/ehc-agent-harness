---
triggers: [secret, password, token, api key, credential, pii, gdpr, injection, vulnerability, dependency]
requires: [CORE]
see-also: [PERSISTENCE, OBSERVABILITY, VALIDATION]
---

# Security And Sensitive Data

Rules for secrets, untrusted input, dependency safety, and handling sensitive data.

Load when: code touches credentials, environment config, external input, third-party APIs, dependencies, or user data.

## Rules

### SEC-1 Never commit secrets [MUST]

Secrets, tokens, API keys, and connection strings must not appear in source code, notebooks, fixtures, or committed outputs. Use environment-backed configuration or a secrets manager. Settings and credentials: **VAL-11** (`VALIDATION.md`).

### SEC-2 Never build SQL from untrusted strings [MUST]

Use parameter binding for untrusted values. Do not interpolate user input into SQL, `text()` clauses, or equivalent query strings.

### SEC-3 Never use `shell=True` with untrusted input [MUST]

Prefer argument lists to shell-built command strings whenever user-controlled values are involved.

### SEC-4 Name, isolate, and minimize PII [MUST]

Sensitive fields should be explicit in schemas, accessed only when needed, excluded from logs, and avoided in derived outputs unless there is a clear reason.

### SEC-5 Validate and bound external input [MUST]

External input must be validated at the boundary with limits on length, ranges, sizes, and allowed values. See **VAL-1**, **VAL-8** (`VALIDATION.md`).

### SEC-6 Never log secrets or PII [MUST]

Logs should use safe identifiers and redact or omit anything sensitive. **OBS-5** (`OBSERVABILITY.md`) defers here.

### SEC-7 Treat third-party data as untrusted [MUST]

Never use `eval`, `exec`, `yaml.load()` without a safe loader, or any untrusted deserialization on external data. Shape and bounds: **VAL-1**, **VAL-8** (`VALIDATION.md`).

### SEC-8 Keep dependency resolution reproducible [MUST]

Commit `uv.lock`. Security-sensitive upgrades should be reviewed deliberately. Workflow: **PY-7** (`PYTHON.md`); `deptry` violations must be addressed.

### SEC-9 Permissive licenses only [MUST]

Only packages with permissive licenses (MIT, Apache-2.0, BSD-*, ISC, MPL-2.0, PSF, Unlicense, Artistic) are allowed. **No GPL / AGPL / LGPL.** Exceptions require project-lead approval and an explicit entry in `[tool.liccheck.authorized_packages]`. `make license-check` enforces this in CI.

### SEC-10 Prefer least privilege [SHOULD]

Use credentials scoped to the minimum required access. Avoid shared all-powerful credentials when narrower ones are possible.

### SEC-11 Keep notebook outputs safe [MUST]

If a notebook exposes PII, secrets, or production-only identifiers, clear the outputs before commit.

## Anti-patterns

- Hardcoding credentials for convenience.
- Logging full payloads "for debugging".
- Building SQL with string interpolation.
- Using unsafe deserialization on network or file content.
- Committing fixtures with real or realistic sensitive data.

## Project Overrides

Project-specific security controls: `docs/docs-guide.md` §3 and this section. See **DOC-6** (`DOCUMENTATION.md`).

## See also

- [PERSISTENCE](PERSISTENCE.md)
- [OBSERVABILITY](OBSERVABILITY.md)
- [VALIDATION](VALIDATION.md)
