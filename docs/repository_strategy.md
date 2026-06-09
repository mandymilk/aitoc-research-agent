# Long-Term Repository Strategy

Version: `v0.1`
Last updated: 2026-06-09

## Purpose

This repository should support a continuing research series, not a single report. It needs to preserve raw evidence, track evolving products, support repeated case studies, and make thesis changes auditable over months or years.

The central design rule:

> Separate evidence, durable knowledge, active interpretation, and published output.

Without this separation, every new product launch or pricing change will force the researcher to rewrite the whole project. With it, the project can accumulate knowledge while keeping conclusions current.

## Recommended Repository Layers

### 1. Control Layer: `docs/`

Use `docs/` for the research system itself:

- `docs/research_plan.md`: master plan and current phase.
- `docs/agent_design.md`: how the research agent should work.
- `docs/research_questions.md`: hypotheses and falsification tests.
- `docs/source_strategy.md`: evidence standards.
- `docs/repository_strategy.md`: long-term organization.
- `docs/operating_system/`: recurring cadence and update workflows.
- `docs/taxonomy/`: stable definitions.
- `docs/decision_records/`: why structural choices were made.
- `docs/case_studies/`: narrative case studies that are still being developed.

This layer answers: "How do we run the research?"

### 2. Evidence Layer: `data/`

Use `data/` for source-backed evidence and structured inputs:

- `data/raw/`: downloaded or manually captured raw source material.
- `data/evidence_index/`: normalized evidence notes, one claim per record where possible.
- `data/product_profiles/`: machine-readable product profiles.
- `data/processed/`: cleaned comparison tables and intermediate outputs.

This layer answers: "What do we know, and where did it come from?"

### 3. Knowledge Layer: `knowledge_base/`

Use `knowledge_base/` for durable, slowly changing notes:

- `knowledge_base/products/`: one product per file.
- `knowledge_base/companies/`: company strategy, assets, distribution, and subsidy capacity.
- `knowledge_base/categories/`: category economics such as companion AI, search AI, AI productivity, and creative AI.
- `knowledge_base/markets/`: geography-specific market structure, especially US, China, EU, Japan, India, and Southeast Asia.

This layer answers: "What is the stable context?"

### 4. Analysis Layer: `models/`

Use `models/` for reusable analytical machinery:

- `models/unit_economics/`: scenario templates for ARPU, gross margin, inference cost, CAC, and churn.
- `models/pricing/`: pricing and packaging comparisons.

This layer answers: "What does the evidence imply economically?"

### 5. Findings Layer: `findings/`

Use `findings/` for time-stamped interpretation:

- `findings/weekly/`: short market updates and new evidence.
- `findings/monthly/`: broader synthesis.
- `findings/thesis_updates/`: explicit changes to the main thesis.

This layer answers: "What changed, and how does it affect our view?"

### 6. Publication Layer: `reports/`

Use `reports/` for polished output:

- `reports/source/`: canonical Markdown memos before channel export.
- `reports/memos/`: written essays and research notes.
- `reports/decks/`: slide-ready narratives.
- `reports/archive/`: older versions retained for comparison.

This layer answers: "What do we publish or share?"

### 7. Output Layer: `outputs/`

Use `outputs/` for delivery-specific files:

- `outputs/kindle/`: Kindle-ready HTML, Markdown, EPUB, or DOCX.
- `outputs/notion/`: Notion-ready Markdown page packages.
- `outputs/web/`: optional web-readable versions.

This layer answers: "What file should be sent to a reading or knowledge-management tool?"

## File Naming Rules

Use stable lowercase slugs:

- Product: `chatgpt.md`, `microsoft-copilot.md`, `doubao.md`
- Company: `openai.md`, `microsoft.md`, `bytedance.md`
- Category: `general-assistants.md`, `ai-companions.md`
- Finding: `2026-06-09-doubao-paid-tiers.md`
- Thesis update: `2026-06-09-tiered-usage-strengthens-cost-control-thesis.md`
- Decision record: `0001-separate-evidence-knowledge-findings.md`

## When To Use Each Location

If the item is a source claim, put it in `data/evidence_index/`.

If the item is a product's current state, put it in `knowledge_base/products/`.

If the item is a developing narrative about why a product matters, put it in `docs/case_studies/`.

If the item is a reusable model or framework, put it in `models/`.

If the item is a time-stamped conclusion, put it in `findings/`.

If the item is polished for external reading, put it in `reports/`.

If the item is exported for a specific destination, put it in `outputs/`.

## Research Series Cadence

Recommended rhythm:

- Weekly: add new evidence notes and a short findings digest.
- Monthly: update product profiles, category notes, and thesis confidence.
- Quarterly: publish a deeper memo comparing product categories and business models.
- Event-driven: update immediately when a major product changes pricing, free limits, model access, ads, or bundling.

## Long-Term Research Questions

The repo should keep returning to these:

- Which consumer AI categories produce durable paid habits?
- Which pricing models protect margin from heavy users?
- Which products are truly AI-to-C businesses versus ecosystem defense?
- Which companies can survive without subsidy?
- Does the market move from subscription to usage tiers, ads, bundling, or marketplaces?
- What changes when inference cost falls, model quality commoditizes, or agents become more autonomous?

## Anti-Patterns To Avoid

- Do not mix raw source quotes with final interpretation in the same file.
- Do not overwrite old findings without a thesis update note.
- Do not compare products without normalizing their category and owner type.
- Do not treat MAU as proof of business-model strength.
- Do not let case studies become disconnected essays; every case should map back to schemas, evidence, and survival classification.
