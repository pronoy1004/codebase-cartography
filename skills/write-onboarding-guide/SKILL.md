---
name: write-onboarding-guide
description: >-
  Write the getting-started guide for a new engineer on a codebase: what the system does, how to
  install and run and test it locally, the entry points, the five files to read first, and a
  glossary of domain terms. Produces docs/codebase-map/onboarding.md. Use when the user asks for
  an onboarding guide, a getting-started doc, a new-developer tour, or "how would someone new get
  up to speed on this". Builds on explore-codebase.
license: MIT
metadata:
  author: pronoy1004
  version: "0.2.0"
---

# Write onboarding guide

This is the on-ramp. A new engineer reads it first and, by the end, can run the system and knows where to look for everything else. It points at the other maps rather than repeating them. Write it last, once the maps exist.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl, and reuse what the other codebase-cartography skills found. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes. Follow the `writing-skills` plugin's `write-readme` shape for the run-it-fast section.

Output: `docs/codebase-map/onboarding.md`.

## Structure

```
# Onboarding guide: <project name>

## What this system does
Two or three sentences. What it is for and who uses it. No jargon.

## Run it locally
The shortest path to a running system.
1. Prerequisites (language version, services, tools).
2. Install.
3. Configure (which env vars to set, pointing at config-and-env.md).
4. Run.
5. Verify it works (the URL to open, the command to run, the expected output).

## Run the tests
The command, where the tests live, and how long they take.

## The five files to read first
An ordered list. For each: the path and why it matters. Start at an entry point.

## How the code is organized
Three or four sentences pointing at architecture.md, plus the one rule of thumb
for where a given kind of change goes.

## Where to look for X
A quick lookup table: "to change an endpoint, see ...", "to add a field, see ...",
"to change config, see ...". Link the relevant map docs.

## Glossary
The domain terms and internal names a newcomer will not know. One line each.

## Who to ask
Code owners, the main maintainers from git history, or the team channel, if known.
```

## Guidance

- Lead with running it. The single biggest onboarding win is a system the new engineer can start on day one. Give the exact commands.
- Test the path in your head against the manifests. If the README says `npm start` but the script is `npm run dev`, use the truth from `package.json`.
- Pick the five first files deliberately. Start at an entry point, then the main router or handler, the core domain module, the data model, and the config. Order them.
- The glossary earns its place. Every codebase has names a newcomer cannot decode (internal service names, domain nouns, abbreviations). Define them.
- Point, do not repeat. Link architecture.md and the other maps rather than restating them. This doc is the index of first moves, not a second copy.
- Never print a secret. For config, name the variables and point at config-and-env.md. Values come from the team, not the doc.

## Gotchas

- Verify the run commands against the manifest scripts, not against the README. If the README says `npm start` and the script is `npm run dev`, the script wins.
- Write this last. It points at the other maps, and pointing at documents that do not exist yet produces broken links.
- Pick the five first files deliberately and put them in order: an entry point, the main router or handler, the core domain module, the data model, then config.
- The glossary is the part a newcomer cannot get anywhere else. Internal service names and domain nouns are exactly what blocks them.
- Name the variables and link the config map. Never put a real secret value in the run steps.

## Common mistakes to avoid

- Burying the run instructions under paragraphs of background. Run-it-fast comes first.
- Copying stale commands from the README without checking the scripts.
- A vague "read the code" instead of five named files in order.
- Skipping the glossary. The domain names are exactly what a newcomer lacks.
- Repeating the architecture doc instead of linking it.
- Putting real secret values in the run steps. Names and a pointer only.

## Self-check before returning the document

Run this list before you hand the document back. Fix anything it catches, then run it again.

1. The run and test commands were checked against the manifest scripts.
2. The run-it-locally section comes before everything except the one-line description.
3. Exactly five first files are listed, in a deliberate order, each with a reason.
4. The glossary defines the internal and domain terms a newcomer cannot infer.
5. No secret value appears in the run steps.
