
# EHC Agent Harness

Guides, rules and templates that make AI-assisted Data Science and Data Engineering work reproducible, reviewable and documented — without losing speed.

![guides: stable](https://img.shields.io/badge/guides-stable-22c55e) ![harness: experimental](https://img.shields.io/badge/harness-experimental-eab308) ![installer: not built](https://img.shields.io/badge/installer-not%20built-94a3b8)

---

## A metarepo, not a project

This repository is **not** application code. It is a **metarepo**: a single source of guides, rules, templates and (early) automations that other repositories and developers draw from. Three different audiences pull different parts of it.

```mermaid
---
config:
  theme: neutral
---
flowchart LR
    accTitle: Metarepo to Project Repo Relationship
    accDescr: How the metarepo guides, agent-kit, AGENTS.md, skills, and subagents flow into the project repo and developer IDE.

    metarepo["This metarepo<br/>(guides, agent-kit, skills, subagents)"]
    target["Your project repo<br/>(real code + docs/)"]
    ide["Your IDE<br/>(Cursor)"]

    metarepo -->|copy by hand| target
    metarepo -->|reference| ide
    ide <-->|reads & writes| target

```

| Folder                                                              | Audience                | How it is consumed                              | Status              |
| ------------------------------------------------------------------- | ----------------------- | ----------------------------------------------- | ------------------- |
| [`guides/`](./guides/)                                              | Developers learning     | Read in place. Never copied.                    | Stable              |
| [`agent-kit/`](./agent-kit/)                                        | Project repositories    | Copied **by hand** into the project repo root.  | Stable (manual)     |
| [`skills/`](./skills/)                                              | Developers' IDEs        | Referenced from the IDE.                        | Experimental        |
| [`subagents/`](./subagents/)                                        | Developers' IDEs        | Referenced from the IDE.                        | Experimental        |

> [!IMPORTANT]
> The **stable core** is the development cycle plus the `agent-kit/` that lives in every project repo. That is what you are expected to adopt. Skills and subagents are automation on top of that core — useful, but still being validated.

> [!WARNING]
> There is **no installer** yet. Today, `agent-kit/` is copied into the project repo manually, and skills/subagents are configured per developer in their IDE. Automation is on the [roadmap](#roadmap).

---

## The development cycle

Five phases, three human review checkpoints. The stable core of the framework. Full reference in [`guides/onboarding/lifecycle.md`](./guides/onboarding/lifecycle.md).

```mermaid
---
config:
  theme: neutral
---
flowchart LR
    accTitle: Development Cycle with Human Reviews
    accDescr: Five phases from Context to Document, with Spec Review, Plan Review and PR Review as human checkpoints.

    ctx["Context"] --> spec["Spec"]
    spec --> rev1(["Spec Review"])
    rev1 --> plan["Plan"]
    plan --> rev2(["Plan Review"])
    rev2 --> build["Build"]
    build --> rev3(["PR Review"])
    rev3 --> doc["Document"]
    doc --> merge(("Merge"))

    classDef ok fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#14532d

    class merge ok
```

### Phases

| Phase        | What you do                                                                                  | Typical artefacts                                  |
| ------------ | -------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Context**  | Load `AGENTS.md` and project docs so the AI is grounded, not guessing.                       | `AGENTS.md`, `docs/docs-guide.md`, `docs/architecture.md`, glossary   |
| **Spec**     | Define what changes, why, and what "done" looks like — before touching code.                 | `docs/features/<feature>/specs.md`                 |
| **Plan**     | Decide how to slice, test and document.                                                      | `docs/features/<feature>/plan.md`                  |
| **Build**    | Ship small, reviewable slices with evidence (test runs, notebook output).                    | code, tests, notebook outputs                      |
| **Document** | Update every durable doc the change touched.                                                 | glossary, CHANGELOG, `report.md`                   |

### Human review checkpoints

Three points where a person — not the AI — has to approve before work continues. The cycle does not move past a checkpoint without sign-off.

| Checkpoint        | What is reviewed                                                | Who                          |
| ----------------- | --------------------------------------------------------------- | ---------------------------- |
| **Spec Review**   | `specs.md` — scope, acceptance criteria, business rules. | Domain expert or lead        |
| **Plan Review**   | `plan.md` — approach, slices, evidence strategy. | Technical lead               |
| **PR Review**     | PR diff, tests and updated docs.                                | Reviewer assigned to the PR  |

**Non-negotiable rule:** lightweight work may skip phases, but the skipped ones must be named explicitly — usually in the PR description or `CHANGELOG.md`.

---

## Adoption

Two parallel tracks: set up the project repo once, and set up each developer's IDE once. Both are manual today.

### Track 1 — Project repo (manual)

1. Copy [`agent-kit/`](./agent-kit/) into the project repo root (`cp -r`, drag-and-drop or `git subtree` — your call).
2. Bootstrap docs and session gitignore (optional but recommended):

   ```bash
   python agent-kit/adopt.py --agents --feature <feature-name>
   ```

   This creates `docs/` from skeletons, ensures `.gitignore` excludes `.local-context/`, and copies `AGENTS.md` from the kit template when missing. Existing files are kept unless you pass `--force`. Run `python agent-kit/adopt.py --dry-run` first to preview.

3. Adapt root `AGENTS.md` to the project: fill in §Commands, confirm §Boundaries, and set overrides in `docs/docs-guide.md` §3 (step 2 copies the template when you pass `--agents`).
4. If you skipped the script, instantiate the base docs manually from [`agent-kit/skeletons/`](./agent-kit/skeletons/) into `docs/`: `architecture.md`, `database.md`, `docs-guide.md`, `glossary.md`.
5. Per feature, create `docs/features/<feature>/` with `specs.md`, `plan.md`, `CHANGELOG.md` (or use `--feature` in step 2). Add `report.md` only when the cycle closes.
6. If you skipped the script, add `.local-context/` to the project [`.gitignore`](./.gitignore) (or create one). Session handoffs and scratch notes live there — never committed. See [managing-context.md](./guides/onboarding/managing-context.md#setting-it-up).

Resulting repo shape:

```text
repo-root/
├── AGENTS.md                    ← from agent-kit/AGENTS.md template
├── agent-kit/                   ← copied from this metarepo
├── .gitignore                   ← must exclude .local-context/
└── docs/
    ├── architecture.md
    ├── database.md
    ├── glossary.md
    ├── docs-guide.md
    └── features/<feature>/
        ├── specs.md
        ├── plan.md
        └── CHANGELOG.md

.local-context/                  ← created on demand; gitignored; handoffs and session notes
```

> [!NOTE]
> Only `agent-kit/` is copied into the project repo (the root `AGENTS.md` is generated from its template in step 2). `skills/` and `subagents/` stay in this metarepo and are referenced from the IDE.

### Track 2 — Developer IDE (optional, experimental)

Each developer points their IDE at the skills and subagents in this metarepo. They are **referenced, not copied** — updates here reach everyone automatically.

Full details in [`guides/onboarding/ai-configuration.md`](./guides/onboarding/ai-configuration.md).

| Tool        | Project instructions            | Skills                         | Subagents        |
| ----------- | ------------------------------- | ------------------------------ | ---------------- |
| Cursor 2.4+ | `AGENTS.md` or `.cursor/rules/` | Team plugin + metarepo `skills/` (referenced, not copied) | metarepo `subagents/` (referenced) |

> [!NOTE]
> Skills and subagents are **not** copied into `.cursor/skills/` in each project. Install the team plugin and/or point Cursor at this metarepo so updates propagate automatically. See [ai-configuration.md](./guides/onboarding/ai-configuration.md).

> [!NOTE]
> `AGENTS.md` is the portable project entrypoint. The Cursor plugin includes a minimal `rules/entrypoint.mdc` rule that points back to `agent-kit/AGENTS.md`; the kit remains the canonical source.

---

## Repository map and glossary

```text
this-metarepo/
├── .github/workflows/   ← CI runs python skills/lint.py on push/PR
├── guides/              ← theory, onboarding, cycle in detail (stable)
├── agent-kit/
│   ├── adopt.py         ← bootstrap docs/ + .gitignore in consumer repos
│   ├── AGENTS.md        ← template copied to consumer root on adoption
│   ├── agent-rules/     ← rules loaded just-in-time by agents
│   └── skeletons/       ← templates for docs/ in consumer repos
├── skills/              ← slash-command workflows (experimental)
│   └── lint.py          ← validate skills + plugin sync + skeleton casing
└── subagents/           ← optional context-delegation templates (experimental)
```

<details>
<summary><strong>Quick glossary</strong></summary>

- **Coding agent** — an LLM-driven tool (Cursor) that reads and edits the repo.
- **Context engineering** — the practice of deliberately controlling what an agent sees, so its output is grounded.
- **SDD (Spec-Driven Development)** — writing the spec before writing the code, so the agent has something to be measured against.
- **AI entrypoint** — the instruction entry your IDE treats as project guidance. For portable project repos this is `AGENTS.md`; for Cursor, the plugin's `rules/entrypoint.mdc` points back to `agent-kit/AGENTS.md`.
- **agent-kit** — the bundle of rules, doc skeletons, `adopt.py` bootstrap script, and the `AGENTS.md` template (this repo's `agent-kit/`) that gets copied into a project repo.
- **adopt.py** — script inside `agent-kit/` that scaffolds `docs/`, `.gitignore` (`.local-context/`), and optionally root `AGENTS.md` after manual kit copy.
- **Vertical slice** — a minimal end-to-end chunk of a feature (data → logic → output) rather than one full layer.

</details>

---

## Roadmap

**Stable, use today**

- [x] The guides
- [x] The development cycle
- [x] `agent-kit/` as reference template
- [x] CI lint for skills catalog and skeleton path casing (`.github/workflows/lint.yml`)

**Experimental, expect changes**

- [ ] `skills/` — naming, selection and scope still being tuned with real use
- [ ] `subagents/` — context-delegation patterns still being tuned with real use
- [x] `agent-kit/adopt.py` — bootstrap `docs/` + `.gitignore` after manual copy (no full installer yet)

**Not built yet**

- [ ] CLI plugin to register skills and subagents in one step
- [ ] One-command delivery of the whole metarepo into a target repo
- [ ] Versioning between this metarepo and the repos that consume it

Contributions welcome — see [Contributing](#contributing).

---

## FAQ

<details>
<summary><strong>Is this production-ready?</strong></summary>

The **guides and the cycle** are — apply them today in Cursor. The **harness and the installation flow** are not. Read first, copy `agent-kit/` second, tinker with skills third.

</details>

<details>
<summary><strong>What if my feature is trivial? Do I still run all five phases?</strong></summary>

No. You may skip phases, but you must state explicitly what you skipped and why — usually in the PR description or `CHANGELOG.md`.

</details>

<details>
<summary><strong>Does everyone need the same Cursor setup?</strong></summary>

Yes. `AGENTS.md` is the shared source of truth for project guidance. Cursor also reads `.cursor/rules/` and plugin rules, but `AGENTS.md` remains the canonical entrypoint. Install the team plugin so safety rules and shared skills load consistently.

</details>

<details>
<summary><strong>Does this replace human code review?</strong></summary>

No. The cycle has three explicit human review checkpoints (Spec, Plan, PR) precisely because architecture, risk and trade-off calls stay human.

</details>

---

## Contributing

1. Open an issue describing the problem or the improvement, especially for roadmap items.
2. New rules or skills must include at least one real example where the addition would have changed an outcome.
3. Keep PRs small and focused — the framework preaches this; the framework should practice it.
4. If you modify a skill, test it end-to-end in your IDE before opening the PR.
5. Run `python skills/lint.py` before opening a PR that touches skills or skeletons — CI runs the same check on every push.
6. When changing skeletons or adoption flow, update `agent-kit/adopt.py`, `agent-kit/AGENTS.md`, and the guides under `guides/onboarding/` so consumer repos stay aligned.

### Conventions worth knowing

| Topic | Convention |
|-------|------------|
| Lifecycle | Five phases (Context → Spec → Plan → Build → Document); SDD-inspired, not pure SDD — see [spec-driven-development.md](./guides/theory/spec-driven-development.md) |
| Session notes | `.local-context/` at repo root, gitignored, never committed |
| Feature changelog | `CHANGELOG.md` (uppercase), not `changelog.md` — Keep a Changelog convention |
| Cycle-close report | `docs/features/<feature>/report.md` — the `business-reports` skill writes here |
| Plugin skills | Edit `skills/utils-skills/`; sync with `python skills/lint.py --sync-plugin` |
| Consumer bootstrap | `python agent-kit/adopt.py` after copying `agent-kit/` into a project repo |

---

## Maintainers

Maintained by the **Eurostars Data Science** team. For questions, reach out through internal channels.
