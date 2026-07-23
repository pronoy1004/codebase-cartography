---
name: inventory-tech-stack
description: Inventory the tech stack of a codebase: languages and versions, frameworks and major libraries, runtimes, package managers, build and test and lint tooling, and CI/CD. Produces docs/codebase-map/tech-stack.md. Use when the user asks about the tech stack, what the project is built with, the frameworks, the tooling, the runtime, or "what languages and tools does this use". Builds on explore-codebase.
---

# Inventory tech stack

The tech stack is the set of technologies a codebase is built on. A new engineer needs it first, because the language and framework decide how they read everything else. This is a factual inventory, taken from the manifests and config, not an opinion on the choices.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl. Read this first in the pipeline, since it frames the rest. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes.

Output: `docs/codebase-map/tech-stack.md`.

## Structure

```
# Tech stack

## Languages
Each language, its version (from the manifest or a version file), and its role
(backend, frontend, scripts, infra).

## Runtime and platform
The runtime (Node, JVM, CPython, Go binary), the target platform, and how it is
packaged (container, serverless, plain process). Cite the Dockerfile or config.

## Frameworks and major libraries
The frameworks that shape the code: web framework, ORM, frontend framework, test
framework. One line each on the role. Point at dependencies.md for the full list.

## Package managers and workspaces
The package manager per language and, for a monorepo, the workspace tool.

## Build, test, and lint tooling
The build tool, the test runner, the linter and formatter, and the commands that
run each (from the manifest scripts).

## CI/CD
The CI system and what its pipeline does: build, test, and deploy stages, from the
workflow files.

## Versions and support notes
Any end-of-life runtime, a pinned old version, or a version mismatch between the
manifest and the CI or Docker image.
```

## Guidance

- Take every fact from a file. The manifest gives the language and dependencies, a version file or the CI image gives the runtime version, the Dockerfile gives the packaging. Cite the source.
- Separate the frameworks that shape the code from the long dependency list. Name the web framework, the ORM, and the test runner here. Leave the full list to [map-dependencies](../map-dependencies/SKILL.md).
- Read the CI workflow for the real build and test commands. The CI file is the truth about how the project is built, more than the README.
- Flag version risk. An end-of-life runtime or a Node version in CI that differs from the Dockerfile is a real operational fact worth recording.
- For a monorepo, note the workspace tool and whether packages share one stack or differ.

## Common mistakes to avoid

- Guessing the stack from the folder names instead of reading the manifest.
- Repeating the entire dependency list here. Name the shaping frameworks, link the rest.
- Skipping the CI file, which holds the real build and test commands.
- Missing a version mismatch between the manifest, the CI image, and the Dockerfile.
- Reading the README's stated versions without checking the actual config.
