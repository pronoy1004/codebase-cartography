---
name: explore-codebase
description: The method for crawling an unfamiliar codebase fast and completely. Read the build manifests first, find the entry points, follow the graph from there, and sample representative files instead of reading everything. Use Explore subagents in parallel for breadth. Every other codebase-cartography skill builds on this. Use when the user wants to understand, map, document, or onboard onto a codebase, or asks how to explore a repo you do not know yet.
---

# Explore codebase

This is the crawl method the rest of the plugin builds on. The goal is a correct map of a codebase in the least reading. You do not read every file. You read the files that tell you where everything else is, then follow the structure they reveal.

Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to any notes you write. If that plugin is not installed, keep the prose plain: short sentences, active voice, no em dashes.

Per-language manifest and entry-point cheatsheet: [references/crawl-checklist.md](references/crawl-checklist.md).

## The method

Follow these phases in order. Do not skip to reading source before you have the map from phase 1 and 2.

1. **Read the manifests first.** The build and package files name the language, the dependencies, the scripts, and the entry points. Read them before any source. See the cheatsheet for the file per ecosystem.
2. **Find the entry points.** Every codebase has a small number of places execution starts: a `main`, a server bootstrap, a CLI command, a route table, a request handler, a job worker. List them.
3. **Map the top-level shape.** List the top-level directories and name the role of each one. Do not open their contents yet. A directory tree plus one line per folder is enough.
4. **Follow the graph, do not scan the disk.** From each entry point, follow imports and calls inward. This shows the real structure. A folder listing shows the filesystem, not the design.
5. **Sample, do not boil the ocean.** For a repeated pattern (50 route files, 30 React components), read three representatives, not all of them. Note the pattern once.
6. **Record as you go.** Write findings into `docs/codebase-map/` in the target repo. Notes you do not write down, you lose.

## Use Explore subagents for breadth

Launch `Explore` subagents in parallel to cover ground you cannot read yourself in time. Give each one a narrow, concrete target, for example:

- "Find every HTTP route or endpoint definition and report file:line and the path."
- "Find all database models, schemas, or migration files and list the entities."
- "Find where config and environment variables are read and list the variable names."

Explore agents read excerpts, not whole files. Use them to locate things, then read the key files yourself in full before you document them.

## Scope and size

- Size the job first. A 5-file library and a 5,000-file monorepo need different depth. Count files by language before you plan the crawl.
- For a monorepo, map the package boundaries first, then treat each package as its own smaller crawl.
- Timebox breadth. It is better to map the whole system at low resolution, then deepen the parts that matter, than to document one corner in full and never see the rest.

## Output location

All generated docs go in `docs/codebase-map/` inside the target repo. One file per concern (`architecture.md`, `dependencies.md`, and so on) plus a `README.md` index. This is the only place these skills write. See [map-codebase](../map-codebase/SKILL.md) for the full file set.

## Read-only and safe

- Read and document only. Never run install, build, or the code itself to explore it. Read the scripts, do not execute them, unless the user asks.
- Never print secret values. When you find a config key or a `.env` reference, record the name, never the value.
- Do not edit source. The only writes are the markdown files under `docs/codebase-map/`.

## Common mistakes to avoid

- Reading source files before reading the manifests. You will not know what you are looking at.
- Listing folders instead of following the import graph. The filesystem layout is not the architecture.
- Reading all 50 instances of one pattern. Read three, note the pattern, move on.
- Documenting one area in perfect detail and never mapping the rest. Breadth first, then depth.
- Running the build or the app to "see what it does." Read it. Execute only on request.
- Copying a secret value into a doc. Names only.
