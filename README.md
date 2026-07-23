# Codebase Cartography

Skills that crawl an unfamiliar codebase and map it for a new engineer. Point them at a repo and they generate the docs you actually need to understand a system fast: architecture, dependencies, the API surface in both directions, request and data flows, the data model, the tech stack, the config surface, mermaid diagrams, and a getting-started guide. Everything lands as markdown in `docs/codebase-map/` inside the target repo.

Built for the common problem of landing in a large codebase, or several at once, with no map. The base layer is a disciplined crawl method: read the manifests, find the entry points, follow the import graph, and sample instead of reading everything. The focused skills sit on top and each write one doc.

## Install

As a Claude Code plugin, add this repo as a marketplace and install `codebase-cartography`. Or use the `npx skills` installer:

```bash
npx skills@latest add pronoy1004/codebase-cartography
```

The generated docs read best with the [writing-skills](https://github.com/pronoy1004/writing-skills) plugin installed, which supplies the `writing-style` and `write-tech-doc` prose layers these skills apply. It is optional. Without it the skills fall back to plain, human prose.

## Use

Point the entry-point skill at a repo:

> map this codebase

It runs the whole pipeline and pauses between steps. Or invoke a single skill on its own, for example "map the architecture" or "trace the main request flow".

## Skills

### The engine

- **[explore-codebase](skills/explore-codebase/SKILL.md)** the base crawl method every other skill builds on. Read manifests first, find entry points, follow the graph, sample representative files, use Explore subagents for breadth. Includes a per-language manifest and entry-point cheatsheet.
- **[map-codebase](skills/map-codebase/SKILL.md)** the entry point. Runs the full pipeline in order and assembles the `docs/codebase-map/` index that ties every doc together.

### The maps

- **[map-architecture](skills/map-architecture/SKILL.md)** components, layers, boundaries, and how the parts communicate. The design, not the folder tree.
- **[inventory-tech-stack](skills/inventory-tech-stack/SKILL.md)** languages, frameworks, runtimes, package managers, build and test tooling, and CI/CD.
- **[map-dependencies](skills/map-dependencies/SKILL.md)** external packages with the reason for each, plus the internal module graph, coupling hot spots, and cycles.
- **[map-apis](skills/map-apis/SKILL.md)** the API surface both ways: endpoints and interfaces created, and the services, SDKs, and stores called.
- **[map-data-model](skills/map-data-model/SKILL.md)** entities, schemas, relationships, migrations, and where each entity is read and written, with an ER diagram.
- **[trace-flows](skills/trace-flows/SKILL.md)** the key flows traced end to end, entry to response, anchored to `path:line` at every hop.
- **[map-config-and-env](skills/map-config-and-env/SKILL.md)** the config surface: env vars, config files, feature flags, and secrets handling. Names only, never values.

### The visuals and the on-ramp

- **[draw-diagrams](skills/draw-diagrams/SKILL.md)** turns the maps and flows into mermaid: component, sequence, dependency, and ER diagrams that render in markdown.
- **[write-onboarding-guide](skills/write-onboarding-guide/SKILL.md)** the getting-started guide: what it does, how to run and test it, the five files to read first, and a glossary.

## Output

Every skill writes into `docs/codebase-map/` in the target repo:

```
docs/codebase-map/
  README.md          index, with the commit sha and date
  onboarding.md      start here
  architecture.md
  tech-stack.md
  dependencies.md
  apis.md
  data-model.md
  flows.md
  config-and-env.md
  diagrams.md
```

The skills read and document only. They never run the code, and they never print a secret value, only its name.

## Why

A new codebase is expensive to enter. The knowledge is in the code, but it takes days to assemble the map that a senior engineer carries in their head. These skills build that map on demand, keep it in the repo next to the code, and stamp it with the commit it was built from, so it can be refreshed instead of going stale in someone's memory.
