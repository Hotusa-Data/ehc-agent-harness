# Registers — business and mixed

The register controls vocabulary, level of detail, and what kind of references are allowed in prose. **Fixed by report type, no override.**

| Type | Register |
|---|---|
| `business-flow` | `business` |
| `system-narrative` | `mixed` |

Applies to **all prose in the document** — sections 1 through 6. YAML frontmatter values and the traceability appendix are exempt (metadata, not prose).

Language follows the rules in `SKILL.md` (glossary's language by default; user override allowed). Register is language-independent — these rules apply equally in English, Spanish, or any other language.

---

## `business`

**Audience**: business stakeholders, PMs, functional analysts. People who understand the problem but don't open the code.

**Hard rules:**

- **Zero variable, function, or class names in prose.** Zero. If an entity matters, it has a domain name; that's what appears.
- **Zero file references.** Not *"in `pricing.py`"*, not *"in the pricing module"*. Traceability lives in the appendix, invisible from prose.
- **Zero implementation jargon.** These words signal the wrong register: API, endpoint, cache, queue, microservice, deserialize, idempotent, throughput, latency (unless business-relevant: *"the customer is notified within a minute"* is OK; *"latency < 60s"* is technical in disguise). Translate or drop.
- **Examples over abstractions.** *"When a customer books a double room and another customer cancels a double room within the next half hour, the system reassigns the room to the first customer automatically"* beats *"the system reconciles room inventory after recent cancellations"*.
- **Code traceability lives only in the appendix.** Prose never references it visibly — no *"see appendix"*, no superscripts, no footnotes.
- **§5 filter:** only items affecting user- or business-perceived behavior. Technical debt that only matters to developers doesn't appear in a `business-flow` report.

### Self-check before delivering

After writing each section, apply this check mentally — Claude can run it on its own draft without external input:

1. **Identifier scan.** Search the section for backticks. Any backticks in prose (excluding the appendix and `<details>` blocks)? If yes, replace with the domain term or drop. The appendix is the only place identifiers live.
2. **Jargon scan.** Re-read looking for the jargon list above (API, endpoint, cache, queue, microservice…). Any hits? Rewrite in domain terms.
3. **Abstraction scan.** For each paragraph, ask: would a PM who's never seen this code know which real scenario this describes? If the answer is *"only abstractly"*, add a concrete example or rewrite around one.
4. **File-reference scan.** Search for `.py`, `.ts`, `.js`, *"the module"*, *"the function"*, *"the class"*. Any in prose? Drop.

If all four pass, the section is in `business` register.

**Good example:**

> When a customer tries to confirm a booking, the system checks whether at least one room of the exact requested typology is free for those dates. If it is, the flow continues normally — the day's price is applied and the booking is confirmed. If not, before returning *"no availability"* the system checks whether any free room of a higher typology can be offered at the same price. This is what the team calls *"silent upgrade"*, and it only activates for customers with a flexible rate and for dates where occupancy is below 70%.

**Bad example** (technical register in disguise):

> The `upgrade_engine.py` module evaluates upgrade eligibility after a failed `check_availability()` call with typology filter. The logic is in `UpgradeRule.evaluate()` and returns an `UpgradeOffer` object the booking endpoint consumes.

---

## `mixed`

**Audience**: hybrid — a handover read by a PM and a new developer together.

**Operative rule:** a business stakeholder reads the entire document **without opening a single `<details>`** and understands it. If a business reader needs to open one to follow the main flow, `mixed` failed.

**Rules:**

- **Main prose follows all `business` rules above** (zero identifiers, zero jargon, examples over abstractions, no file references). The four self-check scans apply to main prose only — not to `<details>` content.
- **Technical detail inside `<details>` blocks**, with a descriptive `<summary>` (e.g. `Technical detail: how the cancellation probability is computed`). Never bare `Technical detail`. Default collapsed.
- **Inside `<details>`, register switches to `technical`**: module names, class and function references, implementation description allowed.
- **Diagrams in domain terms** (same as `business`). Diagrams go inside `<details>` only when genuinely technical (e.g. architecture-beta of cloud services).
- **§5 admits both families** (perceived-behavior + technical with business impact). Each item names its intention for cross-reference. This is the only section that acknowledges the hybrid audience.

`<details>` formatting (mandatory `---` after closing, descriptive summary) in `references/style.md`.

**Good example** (system-narrative, intention *"decide on overbooking"*):

> The system decides how many extra bookings to accept per room typology per day. The decision has two parts: an estimate of how many cancellations the system expects (from the historical pattern over the last 90 days for the same typology and weekday), and a risk tolerance ceiling (how many customers the hotel is willing to leave without a room, expressed as a percentage of the day's total bookings). The system accepts overbooking up to the point where the probability of running short equals that ceiling.
>
> <details>
> <summary>Technical detail: how the probability is computed and where it lives</summary>
>
> The cancellation count estimate is modeled as a Poisson distribution with `lambda` fit to the last 90 equivalent dates (same weekday, same typology), in `risk-calculator/models/poisson.py`. The walking tolerance is a per-channel and per-typology configurable parameter read from `risk-calculator/config/tolerance.yaml`. The optimal-point search is bisection over the Poisson CDF, in `risk-calculator/solver.py:find_optimal_overbooking`. Iteration converges in 5-7 evaluations.
> </details>
>
> ---

---

## Edge cases and tie-breakers

**Glossary terms that match code identifiers** (e.g. glossary defines *"Booking"* and code has class `Booking`): treat as domain term — *"the Booking is confirmed"* in `business` is valid. Glossary capitalization wins.

**Domain acronyms that are also class names** (e.g. *"ADR"* for Average Daily Rate, also a module name): if it's in the glossary, domain register. *"The ADR is recomputed nightly"* is valid in any register.

**Numbers and units always concrete.** *"90 days"*, *"4.5%"*, *"200ms"* — not *"the window"* or *"the threshold"* without a value. Exception: if a value is configurable and named in the glossary (*"pickup window"*), prose can use the name and the concrete value goes to §5 as 💡 with its unit.

**Unavoidable technical content in `business`.** If a critical limitation is genuinely technical, describe it **in its business consequences**, not its mechanics. *"Once a month the system needs an hour of maintenance during which new bookings aren't accepted"* — not *"there's a monthly schema migration with 1h downtime"*.
