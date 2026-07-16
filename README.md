# AI-to-C Business Model Research Agent

This repository is a living research system for studying whether consumer AI products can become durable businesses, or whether the category remains dependent on large-company subsidy, cloud-scale distribution, and strategic spending.

The first research focus is the AI-to-C business model:

- Can consumer AI products support inference cost, acquisition cost, retention, and product development through direct user payment?
- Which models work best: subscription, usage tiers, freemium, ads, marketplace, bundling, enterprise cross-subsidy, or hardware/platform attachment?
- Why do large companies appear advantaged: compute discounts, distribution, identity/data, ecosystem bundling, and patience for losses?
- Are Microsoft Copilot and Doubao early signs of sustainable consumer monetization, or evidence that consumer AI still needs B2B/platform economics to survive?

## Repository Map

- `topics/`: the topic interests layer — the selectable research topics (`registry.json`, `active_topic`) and each scoped topic's folder. The default topic is `aitoc`.
- `docs/research_plan.md`: the evolving master plan (the `aitoc` topic plan). Start here.
- `docs/agent_design.md`: the dedicated research-agent architecture and workflow.
- `docs/research_questions.md`: hypotheses, decision questions, and falsification tests.
- `docs/source_strategy.md`: source hierarchy, evidence rules, and current seed sources.
- `docs/tools/`: tool-call strategy, API dependency matrix, and connector specs.
- `docs/output_strategy.md`: Kindle and Notion output strategy.
- `docs/repository_strategy.md`: long-term organization model for the research series.
- `docs/operating_system/`: recurring research cadence, update rules, and review workflow.
- `docs/taxonomy/`: durable definitions for business models, product categories, and survival classifications.
- `docs/decision_records/`: major research-structure decisions and why they were made.
- `docs/case_studies/`: living case-study files.
- `docs/templates/`: reusable templates for product profiles and evidence notes.
- `knowledge_base/`: durable product, company, category, and market notes.
- `findings/`: dated research findings, thesis updates, and recurring digests.
- `models/`: reusable business-model, pricing, and unit-economic analysis.
- `schemas/`: structured data schemas for evidence and product profiles.
- `src/aitoc_research_agent/`: lightweight local tooling for managing the research repo.
- `configs/`: connector registry, source-query seeds, and example environment variables.
- `connectors/`: future source connector implementations and docs.
- `data/`: raw and processed evidence, intentionally not populated in v0.
- `reports/`: final memos and synthesized outputs.
- `outputs/`: Kindle-ready and Notion-ready exports.

## Current Version

`v0.7.0` is a research-program repository. It does not claim a final answer yet. It defines how the agent should collect evidence, audit freshness, test hypotheses, compare products, model economics, publish findings, and keep the thesis alive as the AI-to-C market changes.

The authoritative project version is stored in `VERSION`.

## Quick Start

```bash
PYTHONPATH=src python3 -m aitoc_research_agent topics
PYTHONPATH=src python3 -m aitoc_research_agent new-research "Electric Vehicles"
PYTHONPATH=src python3 -m aitoc_research_agent use-topic electric-vehicles
PYTHONPATH=src python3 -m aitoc_research_agent plan
PYTHONPATH=src python3 -m aitoc_research_agent daily-run
PYTHONPATH=src python3 -m aitoc_research_agent weekly-run
PYTHONPATH=src python3 -m aitoc_research_agent new-signal "AI search app adds ads"
PYTHONPATH=src python3 -m aitoc_research_agent new-idea "Are ads becoming the default free-tier model?"
PYTHONPATH=src python3 -m aitoc_research_agent connectors
PYTHONPATH=src python3 -m aitoc_research_agent hypotheses
PYTHONPATH=src python3 -m aitoc_research_agent case-coverage
PYTHONPATH=src python3 -m aitoc_research_agent audit-freshness
PYTHONPATH=src python3 -m aitoc_research_agent audit-falsification
PYTHONPATH=src python3 -m aitoc_research_agent create-evidence --source-url "https://example.com" --retrieval-method browser --source-title "Example" --publisher "Example" --claim "Example claim." --claim-type pricing --confidence low --research-implication "Example implication."
PYTHONPATH=src python3 -m aitoc_research_agent new-memo "Why AI-to-C Monetization Is Hard"
PYTHONPATH=src python3 -m aitoc_research_agent export-kindle reports/source/example.md
PYTHONPATH=src python3 -m aitoc_research_agent export-notion reports/source/example.md
PYTHONPATH=src python3 -m aitoc_research_agent publish-kindle reports/source/example.md
PYTHONPATH=src python3 -m aitoc_research_agent publish-notion reports/source/example.md
PYTHONPATH=src python3 -m aitoc_research_agent new-case "Example Product"
PYTHONPATH=src python3 -m aitoc_research_agent validate-evidence docs/templates/evidence_note.example.json
```

After installing the package locally, the shorter `aitoc-research` command is also available.

## Running Inside a Coding Agent (Codex / Claude Code)

The agent can run inside a coding agent and use that runtime's built-in web
search and page-fetch tools as the evidence-retrieval layer, with no paid search
API. See `AGENTS.md` (read by Codex and Claude Code) and `CLAUDE.md` for the full
operating guide. In short: use the runtime's web search for discovery, open each
source with the runtime's fetch/browse tool, then record verified claims with
`create-evidence` using `--retrieval-method search` or `browser`. The
`runtime_web_search` connector in `configs/source_connectors.json` documents this
no-API-key path.

## Working Hypothesis

The current starting hypothesis is intentionally provisional:

Consumer AI may have strong user demand but weak standalone economics unless at least one of these is true:

1. The product has exceptional retention and willingness to pay.
2. Usage is capped, shaped, or priced so heavy users do not destroy gross margin.
3. The product is bundled into a larger paid relationship.
4. The company owns distribution and can avoid high paid acquisition costs.
5. The product produces strategic value beyond direct subscription profit.

This is not a conclusion. The repository is designed to falsify it against standalone challengers, platform products, regional products, and hybrid monetization models.

## Current Implementation Limits

The repo now has audit controls and connector specs, but live data collection is still early:

- No production web scraper is implemented yet.
- No paid app-intelligence API is wired yet.
- Notion API publishing is wired, but requires your integration token and target page/database ID.
- Kindle email delivery is wired, but requires SMTP credentials and an approved sender email in Amazon settings.
- Daily/weekly runs create structured research files, but source collection still requires runtime web tools, future connectors, or manual evidence.

The system should therefore mark unsupported current claims as `unknown`, not fill gaps from model memory.

Publishing is wired but requires private credentials in environment variables. See `configs/env.example`.

## Long-Term Principle

The repo separates facts from interpretation:

- Evidence goes in `data/` and source-backed notes.
- Durable profiles go in `knowledge_base/`.
- Active case-study narratives go in `docs/case_studies/`.
- Time-stamped conclusions go in `findings/`.
- Polished essays and presentations go in `reports/`.

That separation matters because AI business models change quickly. A pricing change should update evidence and product profiles first; only then should it change the thesis.

The repo also separates LLM reasoning from evidence. Current market facts should come from source tools, APIs, local files, or manual captures, not from model memory.

The repo separates source writing from delivery output. Canonical memos live in `reports/source/`; Kindle exports live in `outputs/kindle/`; Notion-ready pages live in `outputs/notion/`.

## Long-Term Update Path

For any new discovery, use this path:

1. Add a trend signal.
2. Promote it to a research idea if it affects a business-model question.
3. Add evidence notes for source-backed claims.
4. Update the structured product profile.
5. Update the durable product or company note.
6. Add a weekly finding if the discovery matters.
7. Add a thesis update only if the main argument changes.
8. Update reports last.

## Recurring Discovery

Microsoft and Doubao are seed cases, not limits. The agent should start daily and weekly runs from `trend_radar/`, looking for new AI-to-C pricing, usage, retention, distribution, and monetization patterns across the market.
