# Map-codebase workflow

The ordered pipeline, with the reason each step sits where it does. Run the steps in this order because each one reuses what the earlier steps found.

## Phase 0: Frame the job

1. Confirm the repo path. For a monorepo, confirm which package or app is in scope, or agree to map the whole thing at the package level first.
2. Size the codebase. Count files by language. A small library and a large monorepo need different depth and a different number of Explore subagents.
3. Read the maintainers' own docs (`README`, `docs/`, `CONTRIBUTING`). Treat them as claims to verify against the code, not as ground truth.
4. Create `docs/codebase-map/` in the target repo.

## Phase 1: The static maps

Do these first. They describe the code at rest. Each one is cheap once explore-codebase has found the manifests and entry points.

1. **inventory-tech-stack**: first, because knowing the language and framework changes how you read everything else.
2. **map-architecture**: the component and layer map. The backbone the other docs hang on.
3. **map-dependencies**: external packages and the internal module graph. Reuses the architecture boundaries.
4. **map-apis**: endpoints created and services called. Reuses the entry points from explore-codebase.
5. **map-data-model**: entities and schemas. Often found near the API and persistence layers.
6. **map-config-and-env**: the config surface. Names only, never values.

## Phase 2: The dynamic view

7. **trace-flows**: run after the static maps. A flow crosses the architecture, the APIs, and the data model, so it is faster and more correct once those exist. Pick the two to five flows that matter most (the primary user action, auth, a background job) rather than every path.

## Phase 3: Visuals and the guide

8. **draw-diagrams**: turn the maps and flows into mermaid. The architecture map becomes a component diagram, each traced flow becomes a sequence diagram, the module graph becomes a dependency diagram, and the data model becomes an ER diagram.
9. **write-onboarding-guide**: last, because it points at everything above. It is the reader's on-ramp: what the system does, how to run it, the five files to read first, and the glossary.

## Phase 4: The index

Write `docs/codebase-map/README.md`. Two-sentence summary, the commit sha and date, then a linked list of every doc. This is the front door.

## Pacing

- Pause after each phase, not each file. Let the user skip a phase they do not need.
- If time is short, complete phase 1 and the index, then stop. A full static map with no flows still onboards a new engineer.
- Re-run against a later commit to refresh the map. Update the sha on the index each time.
