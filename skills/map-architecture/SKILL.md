---
name: map-architecture
description: >-
  Map the architecture of a codebase: its components, layers, module boundaries, responsibilities,
  and how the parts communicate. Produces docs/codebase-map/architecture.md. Use when the user
  asks for the architecture, the high-level design, the components, or "how is this project
  structured". Builds on explore-codebase.
license: MIT
metadata:
  author: pronoy1004
  version: "0.2.0"
---

# Map architecture

Architecture is the shape of the system: the major parts, what each one owns, and how they talk. A new engineer needs this before anything else, because it is the frame every other fact hangs on. Map the design, not the folder tree.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes.

Output: `docs/codebase-map/architecture.md`.

## Structure

```
# Architecture

## What this system is
Two or three sentences. What it does and for whom.

## Components
A table or list of the major components. For each: name, responsibility, key path.

## Layers
The layer boundaries (for example: transport, application, domain, persistence).
State the rule for what each layer may call. Name where the rule is broken.

## How components communicate
In-process calls, HTTP or RPC, events or a queue, a shared database. State which pairs
talk and by what mechanism.

## Cross-cutting concerns
Auth, logging, error handling, config, caching. Where each lives and how it is applied.

## Notable patterns and decisions
The patterns a reader must know to not be surprised (event sourcing, CQRS, a plugin
system, a service locator). One line each, with a path.

## Risks and rough edges
Where the design strains: a god module, a circular boundary, a layer that leaks.
```

## Guidance

- Map the design, not the disk. Follow the import graph from the entry points. A folder named `services` is a hint, not proof of a service layer.
- Name the responsibility of each component in one line. If you cannot, the component is unclear, and that is itself a finding worth recording.
- State the communication mechanism for each pair of components. "The API calls the billing service over HTTP" tells a reader far more than a box and an arrow.
- Record where the stated boundaries leak. A layer rule the code breaks is one of the most useful things a new engineer can know.
- Anchor every component to a `path`. The reader must be able to jump to it.
- Keep it to the major parts. A map with 40 boxes is not a map. Group and summarize.

## Communication mechanisms to identify

- In-process: direct function or method calls, dependency injection.
- Network: HTTP or REST, gRPC, GraphQL, WebSocket.
- Asynchronous: message queue, event bus, pub/sub, webhooks.
- Shared state: a common database, a cache, a shared file store.

## Gotchas

- Directory names are the most common false signal in this job. Follow the import graph from the entry points, because the filesystem shows how someone filed the code, not how it runs.
- A component whose responsibility you cannot state in one line is a finding, not a hole in your notes. Record the ambiguity.
- "A talks to B" is half a fact. Without the mechanism, in-process call or HTTP or queue or shared table, the reader cannot reason about failure or latency.
- Record the boundary violations. The layer rule the code breaks is often the most useful thing a new engineer can learn.
- A diagram with 40 boxes has stopped being a map. Group the parts and raise the abstraction.

## Common mistakes to avoid

- Describing the folder tree and calling it architecture. Follow the calls, not the filesystem.
- Listing every file. Name the major components and group the rest.
- Skipping the communication mechanism. "A talks to B" is half a fact without "how".
- Hiding the rough edges. The leaks and the god module are the point, not an embarrassment to omit.
- Boxes with no code anchors. Every component names a path.

## Self-check before returning the document

Run this list before you hand the document back. Fix anything it catches, then run it again.

1. Every component names a responsibility in one line and a path.
2. Every communication edge names its mechanism.
3. The layer rules are stated, and any place the code breaks them is recorded.
4. The component count is small enough to read as a map.
5. Nothing in the doc is inferred from a directory name alone.
