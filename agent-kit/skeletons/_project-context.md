---
type: context
scope: project
last_updated: YYYY-MM-DD
owner: TBD
---

# Project Context

> Always loaded at session start (see `agent-rules/documentation.md` §DOC-1).
> Keep this file short — it should be readable in one glance.
> Update when project-level decisions change.

---

## Mission

<!-- One or two sentences. What problem does this project solve? Who benefits? -->

---

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Language | Python 3.x | |
| Data | <!-- pandas, dbt, Spark, etc. --> | |
| ML / Analytics | <!-- scikit-learn, MLflow, etc. --> | |
| Persistence | <!-- PostgreSQL + SQLAlchemy, etc. --> | |
| API | <!-- FastAPI, etc. --> | |
| Orchestration | <!-- Airflow, Prefect, etc. --> | |
| CI/CD | <!-- GitHub Actions, etc. --> | |

---

## Features In Active Scope

Features with active work in `docs/features/`:

| Feature | Folder | Status | Description |
|---|---|---|---|
| <!-- feature name --> | `docs/features/<feature>/` | draft / active / implemented | <!-- one-line description --> |

Add a row whenever a new feature folder is created. Remove rows for archived or superseded features.

---

## Key Global Decisions

<!-- Decisions that apply across all features and cannot be overridden at feature level. -->
<!-- Use concise bullet points. Link to ADRs or specs when the decision has history. -->

- <!-- decision 1 -->
- <!-- decision 2 -->

---

## Hard Constraints

<!-- Cross-cutting constraints that apply to the entire project. -->
<!-- Examples: GDPR / data residency, regulatory compliance, mandatory audit trails, -->
<!-- approved cloud providers, data retention policies. -->
<!-- If none, write "None identified." -->

- <!-- constraint 1 -->

---

## Team

| Role | Who | Scope |
|---|---|---|
| Developer | | |
| Lead / Reviewer | | |
| Business Reviewer | | |

---

## Open Questions

<!-- Questions that affect multiple features or have not been assigned to a feature yet. -->
<!-- Move resolved questions to the relevant feature's requirements.md. -->

| Question | Owner | Blocking? |
|---|---|---|
| | | |
