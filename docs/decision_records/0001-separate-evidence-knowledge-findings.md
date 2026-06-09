# Decision Record 0001: Separate Evidence, Knowledge, Findings, And Reports

Date: 2026-06-09
Status: accepted

## Context

The project is intended to become a long-term research series on AI-to-C business models. The first repository version had a plan, case-study files, templates, and schemas. That was enough for starting research, but not enough for continuous tracking.

AI consumer products change quickly. Pricing tiers, free limits, model access, bundling, and ads can change within weeks. If the repository stores everything as narrative notes, old conclusions will become mixed with new facts.

## Decision

Use separate repository layers:

- `data/` for source-backed evidence and structured profiles.
- `knowledge_base/` for durable product, company, category, and market notes.
- `docs/case_studies/` for active narrative case studies.
- `models/` for reusable economic and pricing analysis.
- `findings/` for dated interpretations and thesis changes.
- `reports/` for polished external outputs.

## Consequences

This structure adds more folders, but it makes long-term research safer:

- New evidence can be added without rewriting conclusions.
- Old findings can remain historically visible.
- Case studies can be rebuilt from evidence.
- The main thesis can evolve through explicit updates instead of silent edits.

