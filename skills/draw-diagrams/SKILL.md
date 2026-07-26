---
name: draw-diagrams
description: >-
  Turn the maps and traced flows of a codebase into mermaid diagrams that render in markdown:
  component and architecture diagrams, one sequence diagram per traced flow, a module dependency
  graph, and an ER diagram from the data model. Produces docs/codebase-map/diagrams.md and
  reusable blocks for the other docs. Use when the user asks for diagrams, a visual, a flowchart,
  a sequence diagram, an ER diagram, or "draw the architecture". Builds on explore-codebase.
license: MIT
metadata:
  author: pronoy1004
  version: "0.2.0"
---

# Draw diagrams

A diagram shows in one glance what a page of prose describes. This skill turns the other docs into mermaid, which renders in GitHub, GitLab, and most markdown viewers with no image files. Diagrams supplement the prose maps, they do not replace them.

Build on [explore-codebase](../explore-codebase/SKILL.md), and reuse what the map and flow skills already found. Do not re-crawl. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to any captions. If that plugin is not installed, keep captions plain: short, active, no em dashes.

Read [references/mermaid-recipes.md](references/mermaid-recipes.md) when you are about to write a diagram type you have not produced yet in this run, or when a mermaid block fails to parse.

Output: `docs/codebase-map/diagrams.md`. Reuse individual blocks inside `architecture.md`, `flows.md`, and `data-model.md` where they help.

## Which diagram for which map

| Source doc | Diagram type | Mermaid kind |
|------------|--------------|--------------|
| architecture.md | Component / container diagram | `flowchart` |
| flows.md (each flow) | Sequence diagram | `sequenceDiagram` |
| dependencies.md | Module dependency graph | `flowchart` |
| data-model.md | Entity relationship diagram | `erDiagram` |
| a state machine, if one exists | State diagram | `stateDiagram-v2` |

## Structure

```
# Diagrams

## System components
```mermaid
flowchart ...
```
One-line caption.

## Flow: <name>
```mermaid
sequenceDiagram ...
```

## Module dependencies
```mermaid
flowchart ...
```

## Data model
```mermaid
erDiagram ...
```
```

## Guidance

- Match the diagram to the doc it came from. Do not invent structure the maps do not show.
- Keep each diagram readable. Aim for under about 15 nodes. If it is larger, split it into a high-level diagram plus one per sub-area.
- Label the edges. An arrow with "HTTP" or "publishes event" on it carries the real information. A bare arrow does not.
- Use a stable direction. `flowchart TD` (top down) for layers, `flowchart LR` (left to right) for pipelines and request flows.
- One caption per diagram, one line, stating what it shows.
- Verify the mermaid parses before you commit it. A broken block renders as an error box, which is worse than no diagram.

## Gotchas

- Reuse what the map and flow skills already found. Re-crawling produces a diagram that quietly contradicts the prose.
- Verify that every mermaid block parses. A broken block renders as an error box, which is worse than no diagram at all.
- A bare arrow carries no information. Label the mechanism or the action on every edge.
- Past roughly 15 nodes a diagram stops being readable. Split it into a high-level view plus one diagram per sub-area.
- Never invent a component to make the picture look complete. The diagram must not know more than the maps do.

## Common mistakes to avoid

- A 40-node diagram no one can read. Split it or raise the abstraction.
- Bare arrows with no labels. Label the mechanism or the action.
- Diagrams that contradict the prose maps. Regenerate from the same source.
- Inventing components or relationships to make the picture look complete.
- Shipping mermaid that does not parse. Check it first.

## Self-check before returning the document

Run this list before you hand the document back. Fix anything it catches, then run it again.

1. Every mermaid block parses.
2. Every edge is labelled.
3. No diagram exceeds roughly 15 nodes.
4. Every diagram has a one-line caption.
5. Nothing appears in a diagram that is not in the prose maps.
