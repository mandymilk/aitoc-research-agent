# Decision Record 0002: Topic Interests Layer

Date: 2026-07-14
Status: accepted

## Context

The repository was built around a single hardcoded research question: whether
AI-to-Consumer (AI-to-C) products can be durable standalone businesses. The
scope was spread implicitly across `docs/research_plan.md`, `hypotheses/registry.json`,
`configs/source_queries.json`, and the constants in `src/aitoc_research_agent/cli.py`
(claim vocabulary and freshness windows).

There was no way for a user to point the same research machinery — the daily/weekly
radar, evidence intake, freshness and falsification audits, and output layers — at a
different topic without editing code and config by hand.

## Decision

Introduce a **topic interests layer** that makes the research topic a first-class,
selectable object.

- Topics live in `topics/registry.json`, validated against `schemas/topic.schema.json`.
- The active topic is resolved as: `--topic` flag → `AITOC_TOPIC` env var →
  `topics/active_topic` file → default `aitoc`.
- The existing AI-to-C content is the first topic, `aitoc`, using a **legacy**
  layout that maps to the historical root paths (`data/`, `trend_radar/`, `audits/`,
  `docs/research_plan.md`, `hypotheses/registry.json`). No files were moved, so
  existing tooling and tests keep working.
- New topics use a **scoped** layout: a self-contained `topics/<slug>/` folder with
  its own plan, hypotheses, evidence, runs, signals, and audits.
- New CLI commands: `new-research`, `topics`, `use-topic`; existing daily/weekly/
  signal/idea/evidence/hypotheses/audit commands accept `--topic`.
- Claim vocabulary and freshness windows stay shared defaults, but a topic may
  extend claim types and override freshness windows.
- Evidence notes are stamped with `topic_id`.

### Alternatives considered

- **Flat folders + a `topic_id` filter** on every record (rejected: mixes topics in
  one directory and requires filtering everywhere).
- **Migrating AI-to-C files into `topics/aitoc/`** (rejected for now: unnecessary
  churn and risk; a legacy-layout shim achieves the same separation).
- **LLM auto-generation of the question, hypotheses, and queries** on topic creation
  (rejected: conflicts with the repo's evidence-first, human-in-loop discipline;
  `new-research` scaffolds TODOs instead).

## Consequences

- The master research plan becomes the plan for the `aitoc` topic; the reusable
  Phase 1–4 shape is a template new topics fill in.
- The system can host multiple independent research programs without cross-contamination.
- Two path-resolution code paths exist (legacy vs scoped), justified by zero-migration
  backward compatibility.
