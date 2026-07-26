---
name: map-dependencies
description: >-
  Map the dependencies of a codebase in both directions: external packages (from the manifests,
  with why each one matters) and the internal module dependency graph, including coupling hot
  spots and cycles. Produces docs/codebase-map/dependencies.md. Use when the user asks about
  dependencies, third-party packages, the module graph, coupling, or "what does this rely on".
  Builds on explore-codebase.
license: MIT
metadata:
  author: pronoy1004
  version: "0.2.0"
---

# Map dependencies

A codebase depends on two things: the external packages it pulls in, and its own modules on each other. A new engineer needs both. The external list tells them the vocabulary and the risk. The internal graph tells them what breaks when they change one file.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes.

Output: `docs/codebase-map/dependencies.md`.

## Structure

```
# Dependencies

## External dependencies
Grouped by role (framework, data, auth, HTTP, testing, build, observability).
For each that matters: name, version, and the one reason it is here.
Do not annotate every transitive package. Cover the ones a reader must know.

## Runtime vs development
Which dependencies ship in production and which are build or test only.

## Internal module graph
The major modules and which depend on which. A mermaid graph or a table.
Name the direction of each edge.

## Coupling hot spots
The modules everything imports (a change here is high blast radius) and any
dependency cycles. These are the danger zones for a new engineer.

## Version and risk notes
Pinned or floating versions, obviously stale or unmaintained packages, and any
package doing something surprising (a small utility with a large footprint).
```

## Guidance

- Read the manifest for the declared dependencies and the lockfile for the resolved versions. Trust the lockfile for what actually installs.
- Do not list every transitive package. Cover the direct dependencies that shape the code, grouped by what they do.
- Give one reason per external dependency. "`zod` for runtime schema validation at the API boundary" earns its line. "`zod`: a library" does not.
- For the internal graph, follow imports between the top-level modules, not every file. The reader wants the module-level shape.
- Call out the hot spots explicitly. The module imported by 30 others and any import cycle are the highest-value facts in this doc.
- Separate runtime from dev dependencies. A new engineer must know what actually ships.

## How to find it

- External: the manifest and lockfile named in [explore-codebase](../explore-codebase/SKILL.md).
- Internal: follow `import` / `require` / `use` statements between modules. Grep the import idiom of the language and aggregate by source and target module.
- Cycles: a module graph that loops (A imports B imports A, directly or through a chain). Note each cycle and the files that close it.

## Gotchas

- Read the lockfile for what actually installs. The manifest range tells you what is allowed, not what is there.
- Do not annotate transitive packages. Cover the direct dependencies that shape the code, grouped by role.
- The internal module graph is where a code change actually lands. A dependency doc that stops at third-party packages answers the less useful half of the question.
- Import cycles and the module that 30 files import are the highest-value facts here. They explain why a small change breaks something far away.
- Keep dev and runtime dependencies separated. A newcomer needs to know what ships to production.

## Common mistakes to avoid

- Pasting the whole `package.json` dependency list with no grouping and no reasons.
- Documenting external packages and skipping the internal graph. The internal graph is what a code change touches.
- Ignoring cycles and hot spots. They are the reason a "small" change breaks something far away.
- Trusting the manifest version range over the lockfile's resolved version.
- Mixing dev and runtime dependencies into one undifferentiated list.

## Self-check before returning the document

Run this list before you hand the document back. Fix anything it catches, then run it again.

1. External dependencies are grouped by role, each with a reason.
2. Runtime and development dependencies are separated.
3. The internal module graph is present, not just the package list.
4. Cycles and high-fan-in modules are called out explicitly.
5. Versions come from the lockfile.
