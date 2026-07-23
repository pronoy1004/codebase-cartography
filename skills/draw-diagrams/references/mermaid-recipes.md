# Mermaid recipes

Copy the template, then fill it with what the maps and flows found. Every block must parse. Keep each diagram under about 15 nodes.

## Component / architecture diagram

From `architecture.md`. Use `flowchart TD` for layers, `LR` for pipelines. Label every edge with the mechanism.

```mermaid
flowchart TD
    Client[Web client] -->|HTTP| API[API server]
    API -->|calls| Auth[Auth service]
    API -->|calls| Orders[Order service]
    Orders -->|SQL| DB[(Postgres)]
    Orders -->|publishes| Queue[[Order events]]
    Worker[Job worker] -->|consumes| Queue
    Worker -->|SQL| DB
```

Node shapes: `[box]` service or module, `[(cylinder)]` database, `[[subroutine]]` queue or topic, `{diamond}` decision, `((circle))` external actor.

## Sequence diagram

From each flow in `flows.md`. One participant per component the flow touches. Order the messages as the flow runs.

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant S as OrderService
    participant D as Database
    C->>A: POST /orders
    A->>A: validate + authorize
    A->>S: createOrder(payload)
    S->>D: INSERT order
    D-->>S: order id
    S-->>A: order
    A-->>C: 201 Created
    Note over S,D: emits OrderCreated event
```

Use `->>` for a call, `-->>` for a return, `Note over` for a side effect.

## Module dependency graph

From `dependencies.md`. Nodes are modules, edges are "imports". Mark a cycle or a hot spot in the caption.

```mermaid
flowchart LR
    api --> services
    services --> domain
    services --> data
    data --> domain
    utils --> domain
    api --> utils
    services --> utils
```

## Entity relationship diagram

From `data-model.md`. One entity per table or model. Use crow's-foot cardinality.

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "appears in"
    USER {
        uuid id PK
        string email
    }
    ORDER {
        uuid id PK
        uuid user_id FK
        string status
    }
```

Cardinality: `||` one, `o{` zero or many, `|{` one or many.

## State diagram

Only if the system has an explicit state machine (an order status, a job lifecycle).

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Paid: payment ok
    Pending --> Cancelled: timeout
    Paid --> Shipped
    Shipped --> Delivered
    Delivered --> [*]
```
