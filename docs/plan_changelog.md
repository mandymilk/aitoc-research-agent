# Plan Changelog

## 2026-07-14: v0.7.0

- Added the topic interests layer: research topics are now selectable, user-defined objects in `topics/registry.json` (schema `schemas/topic.schema.json`).
- Kept the AI-to-C content as the first topic, `aitoc`, on the legacy root layout so existing files and tests are unchanged.
- Added self-contained `topics/<slug>/` folders for new scoped topics.
- Added `new-research`, `topics`, and `use-topic` commands, plus a `--topic` flag on the daily/weekly/signal/idea/evidence/hypotheses/audit commands.
- Stamped evidence notes with `topic_id`; let topics extend claim types and override freshness windows.
- Added decision record 0002 and Phase 0.10 to the research plan.

## 2026-06-09: v0.6.2

- Added SMTP-based Kindle publishing through `publish-kindle`.
- Added Notion API page creation through `publish-notion`.
- Added publisher modules for Kindle email and Notion API.
- Added publishing setup documentation and credential environment variables.
- Updated output target config from manual-only exports to real delivery commands.

## 2026-06-09: v0.6.1

- Unified project version across `VERSION`, `pyproject.toml`, package metadata, README, and research plan.
- Made evidence validation enforce schema-like constraints without external dependencies.
- Unified claim-type vocabulary across schema, CLI, freshness policy, and connector registry.
- Seeded initial evidence notes and product profiles for Microsoft Copilot and Doubao with explicit confidence limits.
- Added tests for validation, command data loading, and freshness logic.

## 2026-06-09: v0.6

- Added research quality plan covering scaffolding risk, recency decay, falsification, selection bias, and thesis framing.
- Added hypothesis registry with explicit strengthen/weaken/contradict criteria.
- Added freshness policy and freshness audit command.
- Added falsification policy and falsification audit command.
- Added case-study backlog with standalone challenger coverage.
- Reframed README thesis as a working hypothesis and documented current implementation limits.

## 2026-06-09: v0.5

- Added output strategy for Kindle and Notion.
- Added canonical source memo format in `reports/source/`.
- Added `outputs/kindle/` and `outputs/notion/` as delivery-specific export folders.
- Added publishing runbook and output templates.
- Added output target config with Notion API as optional and Markdown import as v0 fallback.

## 2026-06-09: v0.4

- Added tool-call strategy so the agent does not depend on LLM pre-trained data for fresh market claims.
- Added API dependency matrix and connector specification.
- Added connector registry, query seed config, and environment variable example.
- Updated agent design, source strategy, and research plan with tool-grounded evidence rules.

## 2026-06-09: v0.3

- Added trend radar as the default entry point for daily and weekly research runs.
- Added runbooks for daily and weekly AI-to-C trend discovery.
- Added watchlists for AI-to-C companies, categories, business-model changes, geographies, and source types.
- Added trend signal, research idea, daily run, and weekly run templates.
- Added a trend-signal schema.
- Updated the master plan and agent design so Microsoft and Doubao are anchor examples, not scope limits.

## 2026-06-09: v0.2

- Expanded the repository from a one-off research plan into a long-term research-program structure.
- Added `knowledge_base/`, `findings/`, and `models/` layers.
- Added operating-system docs for weekly, monthly, quarterly, and event-driven updates.
- Added taxonomy docs for business models and survival classifications.
- Added decision record 0001 explaining the evidence/knowledge/findings/report separation.
- Updated the master plan with Phase 0.5 and long-term organization rules.

## 2026-06-09: v0.1

- Created repository-first research system.
- Defined research objective, hypotheses, phases, evidence standards, and survival test.
- Seeded Microsoft Copilot and Doubao as anchor cases.
- Added schemas and lightweight local tooling.
