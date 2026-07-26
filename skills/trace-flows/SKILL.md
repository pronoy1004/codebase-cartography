---
name: trace-flows
description: >-
  Trace the key flows of a codebase end to end, from entry point through handlers, services, and
  data, to the response or side effect, anchored to path:line at every hop. Produces
  docs/codebase-map/flows.md. Use when the user asks how a request works, how a feature flows
  through the code, the request lifecycle, "walk me through what happens when", or the path of a
  specific user action. Builds on explore-codebase.
license: MIT
metadata:
  author: pronoy1004
  version: "0.2.0"
---

# Trace flows

A flow is the path one action takes through the code: a request arrives, handlers and services process it, data is read or written, a response or side effect comes out. Static maps show the parts. A traced flow shows them working together, which is how an engineer actually learns a system.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl. Run this after the static maps (architecture, APIs, data model), because a flow crosses all of them and is faster to trace once they exist. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes.

Output: `docs/codebase-map/flows.md`.

## Pick the flows that matter

Do not trace every path. Trace the two to five flows a new engineer must understand:

- The primary user action (the thing the product is for).
- Authentication and authorization.
- A representative write path (create or update, with validation and persistence).
- A background or async job, if the system has one.
- Any flow the maintainers' docs call out as central.

## Structure

```
# Flows

## Flow: <name, for example "Place an order">
Trigger: <what starts it: an HTTP request, a cron, an event>

Steps:
1. <Entry> (path:line): what happens.
2. <Handler / controller> (path:line): validation, auth, routing.
3. <Service / domain logic> (path:line): the real work.
4. <Data access> (path:line): what is read or written.
5. <Response / side effect> (path:line): what comes out.

Notes: error paths, retries, transactions, and events emitted along the way.

## Flow: <next one>
...
```

## Guidance

- Anchor every hop to `path:line`. A flow a reader cannot follow in the code is a story, not documentation.
- Follow the real calls. Step into each function the previous step calls. Do not assume a name means what it says.
- Note where the flow branches: the auth check that can reject, the validation that can fail, the retry, the transaction boundary. The error paths are half of how a system behaves.
- Record side effects. An event emitted, a queue message published, or a cache invalidated mid-flow is easy to miss and important to know.
- Keep each flow to its main line plus the notable branches. A flow with 40 steps is too fine-grained. Group the mechanical hops.
- Each traced flow is the raw material for a sequence diagram. Hand it to [draw-diagrams](../draw-diagrams/SKILL.md).

## Gotchas

- Run this after the static maps. Tracing a flow before you know the architecture and the data model costs several times more reading.
- Never infer a step from a function name. Open it. Names lie, especially after a refactor.
- The error, retry, and transaction branches are half of how the system behaves. A happy-path-only trace misrepresents it.
- Side effects hide between the obvious steps: an event published, a cache invalidated, an audit row written. Look for them on purpose.
- A 40-step flow is too fine-grained. Group the mechanical hops down to steps a reader can hold in their head.

## Common mistakes to avoid

- Tracing every endpoint. Pick the few flows that teach the system.
- Guessing a step from a function name instead of reading it.
- Dropping the `path:line` anchors. The value is that a reader can follow along in the code.
- Ignoring error and retry paths. They are how the system behaves when things go wrong.
- Missing emitted events and other side effects between the obvious steps.

## Self-check before returning the document

Run this list before you hand the document back. Fix anything it catches, then run it again.

1. Between two and five flows are traced, not every path.
2. Every hop is anchored to path:line.
3. Each flow records its error, retry, or transaction branches.
4. Side effects such as emitted events are noted where they occur.
5. Each step was read in the code, not inferred from a name.
