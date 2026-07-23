---
name: map-data-model
description: Map the data model of a codebase: the entities, database schemas, fields, relationships, migrations, and where each entity is read and written. Produces docs/codebase-map/data-model.md with an ER diagram. Use when the user asks about the data model, the database schema, entities, tables, the ER diagram, or "what data does this store". Builds on explore-codebase.
---

# Map data model

The data model is what the system stores and how the pieces relate. It is often the most stable part of a codebase and the fastest way to understand the domain. Names of entities and their relationships tell a new engineer what the system is really about.

Build on [explore-codebase](../explore-codebase/SKILL.md) for the crawl. Apply the `writing-skills` plugin's `writing-style` and `write-tech-doc` skills to the prose. If that plugin is not installed, keep it plain: short sentences, active voice, no em dashes.

Output: `docs/codebase-map/data-model.md`, including an ER diagram (see [draw-diagrams](../draw-diagrams/SKILL.md)).

## Structure

```
# Data model

## Overview
Two or three sentences on the domain the data represents. The store technology
(Postgres, MongoDB, DynamoDB, and so on).

## Entities
One block per entity or table.

### <Entity name>
Purpose: one line.
Source: path:line (the model, schema, or migration).
Key fields: name, type, and note for the fields that matter (ids, foreign keys,
status enums, unique constraints). Do not list every column of a wide table.
Relationships: what it links to and the cardinality.

## Relationships
The entity relationship diagram.
```mermaid
erDiagram ...
```

## Access patterns
For the core entities: where each is created, read, updated, and deleted (path:line).
This connects the data model to the code that uses it.

## Migrations and evolution
Where migrations live, the migration tool, and any notable schema history
(a table being split, a column deprecated).
```

## Guidance

- Find the model from the source of truth: an ORM model, a schema file, a migration, or the database itself if only DDL exists. Prefer migrations for the real shape, because code models can drift.
- Name the purpose of each entity in one line. The domain becomes clear from the entities and their relationships more than from any prose.
- List the fields that matter: primary keys, foreign keys, unique constraints, status enums, and anything with business meaning. Skip the audit columns and the wide list of plain attributes.
- State cardinality for each relationship: one to one, one to many, or many to many. Draw it in the ER diagram.
- Add the access patterns. Knowing where an entity is written is what turns a schema into a working model of the system.
- Handle non-relational stores too. A document or key-value store still has an implied model. Record the document shapes and the key patterns.

## Common mistakes to avoid

- Listing every column of every table. Show the keys and the meaningful fields.
- Trusting an ORM model over the migrations when they disagree.
- Omitting cardinality. "User relates to Order" is not enough. One to many or many to many changes the design.
- Skipping the access patterns. A schema with no "where is this written" leaves the reader half-informed.
- Assuming a NoSQL store has no model. It has an implied one. Document it.
