---
name: map-apis
description: >-
  Map the API surface of a codebase in both directions. APIs created: the endpoints, RPC methods,
  and public interfaces the code exposes. APIs called: the outbound HTTP, third-party SDKs, and
  database or queue clients the code consumes. Produces docs/codebase-map/apis.md. Use when the
  user asks about endpoints, routes, the API surface, integrations, or "what does this expose and
  what does it call". Builds on explore-codebase.
license: MIT
metadata:
  author: pronoy1004
  version: "0.2.0"
---

# Map APIs

A codebase has two API surfaces. The one it creates is what other systems call: its endpoints and public interfaces. The one it calls is what it depends on at runtime: other services, SDKs, and data stores. A new engineer needs both to know the system's contract with the outside world.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes.

Output: `docs/codebase-map/apis.md`.

## Structure

```
# APIs

## APIs created
The surface this system exposes. One table per protocol.

### HTTP / REST
| Method | Path | Handler (path:line) | Auth | Purpose |

### GraphQL / RPC / gRPC
Queries, mutations, and RPC methods, with the resolver or handler location.

### Public library interface
For a library: the exported functions, classes, and types that form the public API.

## APIs called
The services and stores this system consumes.

### Outbound HTTP and third-party services
| Service | Where called (path:line) | Purpose | Auth mechanism |

### SDKs and clients
Third-party SDKs (payment, cloud, email) and the operations used.

### Data and messaging clients
Databases, caches, and queues the code connects to, and for what.

## Contracts and versioning
Where the API contract lives (OpenAPI spec, proto files, GraphQL schema) and how
versioning is handled, if at all.
```

## Guidance

- Split created from called and never blur them. "The endpoints we serve" and "the services we call" are different facts a reader needs kept apart.
- For each created endpoint, give the method, the path, the handler location, and whether it needs auth. Auth-or-not is one of the first things a new engineer asks.
- For each outbound call, give the target, the call site, and the purpose. This is the system's runtime dependency list at the request level.
- Find the route definitions by the framework idiom, not by guessing. See [explore-codebase](../explore-codebase/SKILL.md), which carries the search terms per framework.
- Prefer the source of truth. If an OpenAPI spec, a proto file, or a GraphQL schema exists, read it, then verify it against the handlers, because specs drift from code.
- Sample repeated shapes. Fifty CRUD endpoints with the same pattern get the pattern described once plus the table, not fifty prose paragraphs.

## Gotchas

- Created and called answer different questions. Never merge them into one list.
- An OpenAPI spec, a proto file, or a GraphQL schema is a claim, not the truth. Check it against the handlers, because specs drift from code.
- Whether an endpoint needs auth is a security-relevant fact. Do not drop the column because filling it in is tedious.
- Outbound calls hide outside the route table. Grep the client idioms, `fetch`, `axios`, `requests`, `HttpClient`, and SDK imports, or you will miss most of the integrations.
- Fifty CRUD endpoints that share one shape get a single pattern note and a table, not fifty paragraphs.

## Common mistakes to avoid

- Merging created and called APIs into one list. They answer different questions.
- Listing endpoint paths with no handler location. A reader cannot jump to the code.
- Omitting the auth column. "Which endpoints are public" is a security-relevant fact.
- Missing outbound calls because you only looked at the route table. Grep the client idioms too.
- Trusting an OpenAPI spec without checking it against the handlers.
- Writing a paragraph per endpoint when a table plus one pattern note would do.

## Self-check before returning the document

Run this list before you hand the document back. Fix anything it catches, then run it again.

1. Created and called APIs are in separate sections.
2. Every created endpoint has a method, a path, a handler location, and an auth note.
3. Every outbound call has a target, a call site, and a purpose.
4. Any spec file was checked against the handlers.
5. Repeated endpoint shapes are covered by one pattern note plus a table.
