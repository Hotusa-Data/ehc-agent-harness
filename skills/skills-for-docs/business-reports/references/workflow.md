# Workflow — Five phases, hard contract

Detailed protocol behind `SKILL.md`. **Read before starting any report.**

The contract is strict because code analysis has a ceiling: it can read *what* code does but not *why*. Only the user can confirm intent. Writing without confirming intent buries assumptions in prose where no one reviews them. The phases exist to surface those assumptions before they ossify.

---

## Phase 0 — Verify inputs

Before touching code, verify four inputs. If any is missing or ambiguous, stop and ask. Don't proceed with an absent input or interpret silence as consent.

**Scope.** A list of paths — files, folders, or both. If missing, ask explicitly. Don't interpret globs or infer scope from conversation context. A single path is fine; just record it as a one-item list in the frontmatter.

**Report type.** `business-flow` or `system-narrative`. If explicitly named in the prompt, take it. Otherwise ask, giving one line on each:
- `business-flow` — explains a specific feature step by step, for someone who wants to understand what it does and how it decides.
- `system-narrative` — explains a whole subsystem organized by business intentions, readable by a PM without opening technical sections.

**Glossary.** Search: working directory → `./docs/` → `./glossary/` → repo root. Look for `UBIQUITOUS_LANGUAGE.md`, `glossary.md`, or equivalent.
- **Found** → load it, use as translation layer throughout.
- **Not found** → proceed. During phase 2, surface each key concept encountered and ask the user for its business name. Accumulate 5-12 terms into an ad-hoc mini-glossary. **Before phase 4, promote the terms to the root glossary via [`make-glossary`](../../make-glossary/SKILL.md)** — do not write a per-feature glossary file. If the user declines promotion, fall back to inlining the terms as a `## Glossary` section right after the executive summary of this report. Frontmatter: `glossary_version: ad-hoc-promoted` or `ad-hoc-inline` accordingly.

**Language.** Default: the glossary's language. If glossary is ad-hoc, the user's language. If the user explicitly asks for another language, write the prose in that language but keep glossary terms in their canonical form. Record in frontmatter as `language: <ISO 639-1>`.

If a prior report exists at the canonical output path for the same type **and exact same scope**, refresh mode auto-activates (see end of this file).

**Code commit.** When the scope lives in a git repo, capture the SHA once in phase 0 with `git rev-parse HEAD` (run via bash, not interactive). If not a repo, leave the frontmatter field blank — don't invent a value.

---

## Phase 1 — Silent analysis

Read glossary and code. Don't announce it; just do it and return with material for phase 2.

### What to look for

**1. Structural unit for the type.**

`business-flow` → the feature as a decision graph: entry point, branches, conditions, outcomes. Map the full shape before asking anything.

`system-narrative` → business intentions: coherent chunks of system behavior with business-observable outcomes. Examples: *"set a day's price"*, *"accept or reject a booking"*, *"reconcile inventory"*. An intention may cross multiple files. What defines it is what the system tries to achieve, not which file it lives in. Healthy scope: 3-8 intentions. Above 8 → scope is too open, surface in phase 2.

**2. Orphan terms.** Code identifiers that express domain concepts but don't appear in the glossary. Add to the question list for phase 2 mini-glossary resolution.

**3. Drift.** If scope includes two implementations of the same calculation (production module vs. notebook, two services computing the same thing, code vs. documented spec) and they differ → tentative ⚠️. Phase 2 confirms which is canonical before committing it.

**4. Hypotheses 💡 and limitations ⚠️.** Concrete leads:
- Magic constants without documented calibration (hardcoded `0.85`, `90`, `4.5`).
- Silent `try/except` blocks that swallow failures.
- Inputs read but never used, or expected inputs the code never validates.
- `TODO` / `FIXME` / `HACK` comments with business impact.
- Documented behavior (in comments, docstrings, README) the code doesn't seem to implement.
- A business rule the team mentioned that doesn't appear anywhere in the code.

### Phase 1 deliverable — three internal lists

- **Question list**: real ambiguities needing user input. Each entry: context + your recommendation.
- **Commitment list**: clear findings you'll include without asking (land directly in the assumptions summary).
- **Tentative 💡/⚠️ list**: items for §5.

### Decision after phase 1

Based on the three lists, decide which path through phase 2:

| Condition | Path |
|---|---|
| User signaled auto-confirm earlier (*"just do it"*, *"no me preguntes"*) | **Fast path** — skip 2a and 2b, go to phase 3 |
| Question list empty + no drift + no orphans + glossary complete | **Fast path** — skip 2a and 2b, go to phase 3 |
| Anything else | **Full path** — 2a then 2b then phase 3 |

Fast path replaces the upfront assumptions summary with a brief assumptions note appended at the **end** of the final report, so the user can still review what was decided after reading.

---

## Phase 2 — Grilling + assumptions summary

Two sub-phases in strict order: questions first, summary second. The summary never appears before all questions are answered.

### 2a — Questions

**One question per turn is the default.** Each carries:
1. Brief context (1-2 sentences) in domain language on which part of the code causes the doubt.
2. The concrete question.
3. Your recommendation — *"I'd treat this as X, not Y, because [short reasoning]"*. **Mandatory** — lets the user reply yes/no instead of drafting from scratch.

**Grouping is allowed when questions are tightly related.** If three questions share a single concept (e.g. three thresholds in the same rule), present them together in one turn with one recommendation each — better than three near-identical turns. **If the question list is 6+, present a numbered list of all questions in one turn with a recommendation per item.** The user can reply *"all yes"* or *"all yes except 4 and 7"*. One-per-turn is for ambiguities that need real back-and-forth, not for ticking boxes.

**Good example** (business-flow, pricing feature):
> The code has two paths to compute the pickup factor: one in the production module using the mean of the last 30 same-length-of-stay dates, and another in the exploration notebook using the median of the last 14. Which is canonical? I'd go with the production module (mean, 30 dates) and mark the notebook version as an ⚠️ drift — exploration not yet promoted.

**Don't:**
- Ask without a recommendation.
- Ask about things the code resolves unambiguously (those go directly to the commitment list).
- Drag out unrelated questions over many turns when the user is clearly waiting.

**When 2a ends:** question list is empty. If a user reply opens a new question, append it and continue.

### 2b — Assumptions summary

Present this when 2a ends. Skip 2b entirely when on the fast path (the brief assumptions note moves to the end of the report).

On the full path, the summary is **mandatory** even if 2a was empty. It's the point of no return before the outline.

**Structure:** numbered list of 4-8 concrete, attackable items. One sentence each in domain language. After the list:
> *"Do you confirm all the points? Let me know if any needs adjustment before I start writing."* — translate to the report's language before sending.

**Includes:**
- Term translations: *"the variable `pickup_factor` translates as 'pickup factor'"*.
- Resolved choices: *"the canonical calculation is the production module's, not the notebook's"*.
- Thresholds and windows with units: *"4.5% per typology"*, *"90-day window"*.
- The nature of detected things: *"the three switch branches are the three business scenarios you confirmed"*.
- Structural decisions: *"the system has 5 intentions; above that, the scope would be too open for one report"*.

**Does NOT include:**
- Generic openers (*"I'll now generate a report"*).
- Scope-obvious things (*"the code lives in folder X"*).
- Hypotheses and limitations already identified (those go directly to §5, unless you need user confirmation on their nature).

**Confirmation — three possible replies:**
1. Confirms everything → phase 3.
2. Amends one point, no new ambiguity → absorb, update the summary showing the change, ask again.
3. Amends and opens a new question → return to 2a, resolve, present updated summary.

**Only on full confirmation of the final summary does phase 3 begin.**

---

## Phase 3 — Outline

Present the report's planned structure. This is the last thing the user confirms before writing. On the fast path, this is the **only** thing the user confirms before writing.

**Format:** a numbered list mirroring the six-section frame, one or two sentences per section describing what will go there for this specific report — specific content, not generic descriptions.

**Must include:**
- §3: which diagram type, approximate node count.
- §4: which sub-sections apply, what each covers, which additional diagrams appear and where.
- §5: count of 💡 and ⚠️ and their topics.
- §6: approximate entry count.

**Example:**
> **Outline — Silent Upgrade (business-flow)**
> 1. Frontmatter — scope: `booking/upgrade.py`, glossary: ad-hoc-promoted (5 terms promoted to `docs/glossary.md`), language: `es`, commit: `a3f9c2`.
> 2. Executive summary — what the rule does, for whom, when it activates.
> 3. Anchor flowchart — full flow from booking attempt to confirmation or rejection, including upgrade branch. ~9 nodes.
> 4. Body:
>    - §4.1 — What it does: 3 sentences on problem, audience, trigger.
>    - §4.2 — Flow step by step: prose for 4 decision nodes (availability check, flexible rate check, occupancy check, upgrade offer).
>    - §4.3 — States: omitted (no explicit lifecycle states).
>    - §4.4 — Rules table: flexible rate condition, 70% occupancy threshold, early booking exception.
>    - §4.5 — Outcomes: booking saved, customer receives confirmation with upgraded room.
> 5. Hypotheses and limitations — 2💡 (flexible rate definition assumed stable, occupancy threshold calibration), 1⚠️ (phone bookings not contemplated by the rule).
> 6. Appendix — 4 entries.

After presenting: *"Are you OK with this outline, or do we adjust anything before I start?"* — translate to the report's language before sending.

Only on confirmation does phase 4 start.

---

## Phase 4 — Write

Compose following: shared frame (§§1-6), body spec in `templates/<report_type>.md`, register in `references/registers.md`, style in `references/style.md`, diagrams in `references/diagrams.md`.

Optionally start from the template skeleton; it has all rules embedded as comments.

### Size targets

Size is a signal: when a report grows too big, the scope is usually wrong, not the writing.

| Type | Healthy | Soft cap | If exceeded |
|---|---|---|---|
| `business-flow` | 100-250 lines | 400 lines | Scope too broad — split into sub-features or surface in phase 2. |
| `system-narrative` | 300-600 lines | 800 lines | Too many intentions — partition by area (`system-narrative-pricing.md`, `system-narrative-inventory.md`). |

---

### Sanity-check diagrams before including

Each Mermaid block passes a sanity check before inclusion. A broken block can break the whole document in some renderers.

**Honest about what the check covers**: the bundled checker (`scripts/check_mermaid.sh` on bash; `scripts/check_mermaid.ps1` on PowerShell / Windows) validates structural surface (balanced braces, `accTitle`/`accDescr` present, `classDef` well-formed, no obvious malformed lines). It does **not** fully parse Mermaid grammar — that would need a real Mermaid renderer (`mmdc` from `@mermaid-js/mermaid-cli`).

**Procedure:**
1. After writing, run the checker appropriate to your shell:
   - bash / WSL / git-bash: `bash scripts/check_mermaid.sh <path-to-report.md>`
   - PowerShell: `pwsh -File scripts/check_mermaid.ps1 <path-to-report.md>`
2. If `mmdc` is installed in the environment, the bash variant chains it for real validation; the PowerShell variant only does surface checks. Use the bash version under WSL if you need real parser validation on Windows.
3. If a block flags: fix once and re-run.
4. If still broken: return to phase 2 with a concrete question on how to represent what the diagram was trying to show. **Don't ship a broken diagram or a *"diagram omitted due to error"* note.**

A self-check Claude can apply mentally: every `flowchart`/`stateDiagram-v2`/`sequenceDiagram` block starts with the type keyword on its own line, every `{...}` or `[...]` is closed, every decision node has labeled branches on all exits, every `classDef` line follows the `classDef name fill:#...,stroke:#...` shape. If any of these fail visually, fix before running the script.

### Hard return to phase 2 if something new surfaces

A new ambiguity that phase 1 missed may appear during writing. When it does:
1. Stop writing.
2. Return to 2a with that question (context + question + recommendation).
3. Resolve.
4. Update the assumptions summary with the added point, request re-confirmation.
5. **If the new resolution changes the outline** (e.g. you discover the system has 6 intentions, not 4), re-confirm the outline too. **If it only affects a single 💡/⚠️ or a threshold value**, skip the outline re-confirmation and resume writing.

Never write with a best guess. Never mark an unresolved item as 💡 to avoid asking. Never leave a TODO.

### Output and backup

Write to `docs/features/<feature>/report.md`. Folder resolution rules:

1. **If the scope maps to an existing feature folder** in `docs/features/` (look for one whose name matches the scope, or whose `requirements.md` / `design.md` reference the same paths), **reuse it**. Don't create a parallel folder. This is the AGENTS.md convention — the report lives next to `requirements.md`, `design.md`, `tasks.md`, `CHANGELOG.md`.
2. **Otherwise** derive `<feature>` as a kebab-case `scope_slug` from the scope (single file `booking/upgrade.py` → `booking-upgrade`; multiple paths joined with `-and-`) and create the folder.

If refresh mode: `cp <output_path> <output_path>.bak` before overwriting (overwrites any prior `.bak`).

On completion, deliver a short message: file path, hypothesis and limitation count, whether terms were promoted to the root glossary, and — on fast path — that the assumptions summary is at the end of the report.

---

## Refresh mode

If the output path already has a prior report of the same type **and exact same scope** (same paths, same order), refresh mode auto-activates on file presence. A different scope produces a different `scope_slug` and a different file — no refresh, no collision.

**Differences from normal flow:**
- Phase 1 also parses the prior report: structural units (features/intentions), prior 💡/⚠️, glossary version, timestamp, language.
- Computes a semantic diff: new/modified/removed units; changed thresholds or rules; glossary delta.
- In phase 2 (full path) or before phase 3 (fast path), present the diff: *"Since the prior report I detect these changes in the code — reflect all of them, or skip any?"*. Normal phase 2 grilling follows on the full path.
- In phase 4, before overwriting: `cp <output_path> <output_path>.bak`.

Refresh does NOT: produce a line-by-line markdown diff; detect or preserve manual edits in the prior report (`.bak` is the safety net); carry text from the prior report into the new one (phase 4 writes from scratch using confirmed info).
