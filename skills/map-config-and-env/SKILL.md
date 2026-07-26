---
name: map-config-and-env
description: >-
  Map the configuration surface of a codebase: environment variables, config files, feature flags,
  secrets handling (names only, never values), and how settings differ per environment. Produces
  docs/codebase-map/config-and-env.md. Use when the user asks about configuration, environment
  variables, config files, feature flags, secrets, or "what do I need to set to run this". Builds
  on explore-codebase.
license: MIT
metadata:
  author: pronoy1004
  version: "0.2.0"
---

# Map config and env

Configuration is every knob that changes how the system runs without changing the code: environment variables, config files, and feature flags. A new engineer needs this to run the system and to understand why it behaves differently across environments. Record the names and the shape, never the secret values.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes.

Output: `docs/codebase-map/config-and-env.md`.

## Safety: names only, never values

This is the firm rule of this skill. Record the name of every variable and config key. Never copy a value from a `.env` file, a secrets manager, or a committed config. If you find a real secret committed to the repo, note that it exists and where, so it can be rotated, but do not reproduce it.

## Structure

```
# Config and env

## Environment variables
| Name | Required | Purpose | Where read (path:line) | Default |
Value column is intentionally absent. Names and defaults only, never secrets.

## Config files
Each config file, its format, its scope, and what it controls. Point at the example
file (`.env.example`, `config.sample.*`) a newcomer copies from.

## Feature flags
The flags, where they are defined, and what each toggles. The flag system, if any.

## Secrets handling
How secrets are supplied (a secrets manager, env vars, a vault) and how the code
reads them. Names of the secrets, never the values. Flag any secret committed to
the repo as a finding to rotate.

## Per-environment differences
How local, staging, and production differ: which variables change, which services
are stubbed, which flags are on. This explains "works on my machine" gaps.
```

## Guidance

- Find where config is read, not just where it is declared. Grep the access idiom (`process.env`, `os.environ`, `getenv`, a config object) and record the call site. That proves the variable is actually used.
- Mark each variable required or optional, and give its default if the code sets one. "Required, no default" is the list a newcomer must fill to boot the system.
- Point at the example file. Most projects ship a `.env.example` or sample config. It is the safe template a new engineer copies. Link it.
- Cover feature flags. A flag that changes behavior at runtime is config, and an unexplained flag is a common source of confusion.
- Explain the per-environment differences. Most "it works locally but not in staging" problems live here.
- Hold the line on secrets. Names and purposes only. If a real secret is committed, that is a finding to report for rotation, not content to copy.

## Gotchas

- Names only, never values. This rule is absolute. If you find a real secret committed to the repo, record that it exists and where, so it can be rotated, and do not reproduce it.
- A declared variable the code never reads is noise. Prove each one with a call site.
- Required or optional is the fact a newcomer needs most. Without it they cannot tell what they must set to boot the system.
- Feature flags are configuration. A flag that changes runtime behavior with no explanation is a common source of confusion.
- Most "works on my machine" gaps live in the per-environment differences section. Do not skip it.

## Common mistakes to avoid

- Copying a value from a `.env` file into the doc. Names only.
- Listing declared variables the code never reads. Prove use with a call site.
- Omitting the required-or-optional mark. A newcomer cannot tell what they must set.
- Skipping the example file that is the safe starting template.
- Ignoring feature flags. They change runtime behavior and confuse newcomers.
- Reproducing a committed secret instead of flagging it for rotation.

## Self-check before returning the document

Run this list before you hand the document back. Fix anything it catches, then run it again.

1. No secret value appears anywhere in the document.
2. Every variable is marked required or optional.
3. Every variable has a call site proving the code reads it.
4. The example config file is linked.
5. Per-environment differences are documented.
