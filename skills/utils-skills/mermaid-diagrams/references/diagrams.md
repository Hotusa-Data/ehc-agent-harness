# Diagrams — the eight types this skill covers

Catalog of the eight Mermaid diagram types covered by this skill, with exemplar templates. **General Mermaid rules** (`accTitle`, no `%%{init}`, no inline `style`, `snake_case` IDs, max one emoji per node, no identifier names in labels, edge labels on decisions, `classDef` use) live in `references/style.md`. Read that first; this file lists only type-specific notes on top.

| Diagram | Keyword | Primary use |
|---|---|---|
| ER | `erDiagram` | Data models, entities, relationships |
| C4 | `C4Container` / `C4Context` | Layered system architecture |
| Architecture-beta | `architecture-beta` | Cloud topology with named services |
| Block | `block-beta` | Geometric / spatial layout |
| Flowchart | `flowchart` | Processes, decisions, conditional flows |
| Sequence | `sequenceDiagram` | Temporal interactions between actors |
| State | `stateDiagram-v2` | Lifecycles, state machines |
| Mindmap | `mindmap` | Hierarchical concept maps |

---

## ER — Entity Relationship

**For**: data models, domain entities, their relationships.
**Anti-use**: class hierarchies with methods (use `class`), processes (use `flowchart`).

```mermaid
erDiagram
    accTitle: Bookings Data Model
    accDescr: Relationships between customer, booking, room, and typology in the hotel reservation system.

    CUSTOMER ||--o{ BOOKING : "places"
    BOOKING ||--|| ROOM : "occupies"
    ROOM }o--|| TYPOLOGY : "is_of"
    BOOKING ||--o{ INCIDENT : "may_trigger"

    CUSTOMER {
        uuid id PK "Identifier"
        string name "Full name"
        string email "Contact email"
        string segment "Commercial segment"
    }
    BOOKING {
        uuid id PK "Identifier"
        uuid customer_id FK "Customer"
        uuid room_id FK "Assigned room"
        date check_in "Check-in date"
        date check_out "Check-out date"
        string status "Booking status"
    }
    ROOM {
        uuid id PK "Identifier"
        uuid typology_id FK "Typology"
        string number "Visible number"
    }
    TYPOLOGY {
        uuid id PK "Identifier"
        string name "Commercial name"
        int capacity "Max capacity"
    }
    INCIDENT {
        uuid id PK "Identifier"
        uuid booking_id FK "Affected booking"
        string kind "Incident kind"
    }
```

**Type-specific:**
- **Cardinalities**: `||--o{` one-to-many, `||--||` one-to-one, `}o--o{` many-to-many. `o` = zero or more, `|` = exactly one. Relationship verbs as quoted strings.
- **Scope rule**: only **principal domain entities** — typically 5-12. Auxiliary tables (joins, logs, audit, translations) grouped or omitted. A 30-box ER doesn't read.

---

## C4 — Container and Context

**For**: layered architecture. Container is the most common level for "what pieces, how they talk"; Context for "where the system ends".

```mermaid
C4Container
    title Overbooking Decision System — Container View

    Person(rev_manager, "Revenue Manager", "Configures tolerance parameters and reviews decisions")
    System_Ext(pms, "Hotel PMS", "Property Management System")

    Container_Boundary(overbooking, "Overbooking System") {
        Container(api, "Decision API", "Python / FastAPI", "Receives booking acceptance queries")
        Container(risk, "Risk Calculator", "Python", "Estimates cancellation probability and optimal point")
        Container(inventory, "Inventory Keeper", "Python", "Maintains consistent inventory state")
        ContainerDb(state, "State", "PostgreSQL", "Bookings, inventory, parameters")
        ContainerQueue(events, "Events", "RabbitMQ", "Async recompute events")
    }

    Rel(rev_manager, api, "Configures and queries", "HTTPS")
    Rel(pms, api, "Asks whether to accept booking", "HTTPS")
    Rel(api, risk, "Requests decision", "gRPC")
    Rel(risk, state, "Reads history", "SQL")
    Rel(risk, events, "Publishes recomputes", "AMQP")
    Rel(inventory, events, "Consumes recomputes", "AMQP")
```

**Type-specific:**
- **Conventions**: `Person()` for humans, `System_Ext()` for external systems, `Container()` for your components, `ContainerDb()` for databases, `ContainerQueue()` for queues/buses. `Rel()` with action verb and tech/protocol.
- **Level**: Container as default. If a specific component deserves zoom, add a `C4Component` separately — **don't change the top-level view**.

---

## Architecture-beta — Cloud topology

**For**: when the system is really a topology of named cloud services (S3, Lambda, RDS, etc.) and C4 expresses it worse than icon-bearing boxes.

```mermaid
architecture-beta
    group hotel_cloud(cloud)[Hotel Cloud]

    service api(server)[Public API] in hotel_cloud
    service lambda_pricing(server)[Pricing Calculator] in hotel_cloud
    service rds(database)[Relational DB] in hotel_cloud
    service s3(disk)[Event Store] in hotel_cloud
    service queue(internet)[Event Queue] in hotel_cloud

    api:R --> L:lambda_pricing
    lambda_pricing:R --> L:rds
    lambda_pricing:B --> T:queue
    queue:R --> L:s3
```

**Type-specific:**
- **Anti-pattern**: using `architecture-beta` when what you have is really *application* (logical processes), not *topology* (named physical services). If component differentiation is semantic more than technical, go back to `C4Container`.

---

## Block — Geometric layout

**For**: when **spatial arrangement** matters (layers, columns, areas), not the flow between pieces.

```mermaid
block-beta
    columns 3
    a["Presentation Layer"]:3
    b["Application Services"]:3
    c1["Pricing"] c2["Inventory"] c3["Bookings"]
    d["Event Bus"]:3
    e["Persistence"]:3
```

**Type-specific:**
- **Pick block over C4** when the system has a layered or banded shape the reader recognizes by form (classical three layers, CQRS columns, platform functional bands). If the system is flat (five services at the same level), C4 tells it better.

---

## Flowchart — Process and decision flows

**For**: process steps, decisions with branches, conditional logic. Most versatile type.

```mermaid
flowchart TD
    accTitle: Booking Acceptance Flow
    accDescr: Process the system follows when a booking request arrives, from availability check to confirmation or rejection, including overbooking decision if the typology is apparently full.

    start_node(["Booking request arrives"])
    check["Check availability of requested typology"]
    available{"Room free?"}
    ob_margin{"Overbooking margin?"}
    accept(["Accept booking"])
    reject(["Reject — no availability"])
    assign["Assign specific room"]
    confirm["Send confirmation"]

    start_node --> check --> available
    available -->|yes| assign --> accept --> confirm
    available -->|no| ob_margin
    ob_margin -->|yes| accept
    ob_margin -->|no| reject

    classDef start_end fill:#1e293b,stroke:#1e293b,stroke-width:2px,color:#f1f5f9
    classDef action    fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
    classDef decision  fill:#f1f5f9,stroke:#475569,stroke-width:1.5px,color:#1e293b
    classDef ok        fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#15803d
    classDef ko        fill:#fef2f2,stroke:#dc2626,stroke-width:1.5px,color:#991b1b

    class start_node start_end
    class check,assign,confirm action
    class available,ob_margin decision
    class accept ok
    class reject ko
```

**Type-specific:**
- **Actions begin with a verb**: *"Check availability"*, *"Apply discount"*. Not nouns.
- **Start and end as `()` or `(([...]))`** so they look visually distinct from intermediate actions.

---

## Sequence — Temporal interactions

**For**: how several actors/components talk over time. Natural type for *"what happens when a request comes in"*.

```mermaid
sequenceDiagram
    accTitle: Booking Acceptance Request
    accDescr: Sequence of messages from the PMS asking whether to accept a booking to the response, including risk calculation and inventory check.

    participant PMS as Hotel PMS
    participant API as Decision API
    participant Inv as Inventory Keeper
    participant Risk as Risk Calculator
    participant Q as Event Bus

    PMS->>API: Accept booking for X dates?
    API->>Inv: Room of this typology free?
    Inv-->>API: None directly free
    API->>Risk: Overbooking margin?
    Risk->>Risk: Estimate cancellations (Poisson 90d)
    Risk-->>API: Yes, 3.2% margin
    API-->>PMS: Accept
    API->>Q: Publish booking_accepted
    Q->>Inv: Consume event
    Inv->>Inv: Mark room occupied (idempotent)
```

**Type-specific:**
- **Conventions**: `->>` synchronous message, `-->>` response or async message. `participant` declared at the top in left-to-right order.
- **Activations (`activate`/`deactivate`) only when they add information** — most diagrams don't need them.

---

## State — State machines

**For**: an entity's lifecycle with event-triggered transitions.

```mermaid
stateDiagram-v2
    accTitle: Booking Lifecycle
    accDescr: States a booking goes through from customer creation to completion, with expected transitions and the ones that release inventory.

    [*] --> Draft
    Draft --> Pending_Payment : Customer confirms details
    Pending_Payment --> Confirmed : Payment received
    Pending_Payment --> Expired : No payment in 24h
    Confirmed --> In_Progress : Check-in day
    Confirmed --> Cancelled : Customer cancels
    In_Progress --> Completed : Check-out day
    In_Progress --> No_Show : Customer doesn't show
    Cancelled --> [*]
    Expired --> [*]
    Completed --> [*]
    No_Show --> [*]
```

**Type-specific:**
- **State names** in `Snake_Case` or `Title Case`. Transitions labeled with their triggering event.
- **Don't mix** automatic transitions with event-driven ones without marking them (*"30 days"*, *"automatic"*).

---

## Mindmap — Concept hierarchy

**For**: hierarchically organized concepts without a linear flow between them.

```mermaid
mindmap
  root((Revenue System))
    Pricing
      Daily rate calculation
      Discount application
      Demand-based adjustment
    Inventory
      Availability by typology
      Room-typology assignment
      Manual blocks
    Overbooking
      Cancellation estimation
      Configured tolerance
      Accept/reject decision
    Reporting
      Daily snapshot
      Year-on-year comparison
```

**Type-specific:**
- **Pick mindmap over C4-context or block** when you're showing *what something covers* (concepts/intentions), not *how it's structured* (components). If the reader needs to see how pieces talk, mindmap is the wrong type — use C4 or block.

---

## Types not covered by this skill (and why)

To remove temptation:

- **`class`** — class hierarchies with methods. Out of scope for this skill's documentation focus.
- **`gantt`** — timelines with dependencies. Use a project management tool instead.
- **`pie`, `xychart-beta`, `radar-beta`, `sankey`, `treemap`** — **data** diagrams, not **structure**. For aggregate metrics use a real charting tool (Matplotlib, Vega, Recharts).
- **`timeline`, `gitGraph`, `packet`, `requirement`, `quadrant`, `user_journey`, `kanban`** — niche types out of scope here.
- **`zenuml`** — programming-syntax alternative to sequence. Brings implementation jargon to the diagram; prefer sequence.

If you need one of these, don't add it as Mermaid in this skill's documents — use the appropriate dedicated tool.
