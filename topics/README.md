# Topics

This folder holds the **topic interests layer**: the set of research topics the
agent can work on. Each topic scopes its own plan, hypotheses, evidence, runs,
signals, and audits.

- `registry.json` — the list of topics. Validated against
  [`schemas/topic.schema.json`](../schemas/topic.schema.json).
- `active_topic` — a one-line pointer to the currently selected topic slug.
- `<slug>/` — a self-contained folder for each **scoped** topic (its own
  `research_plan.md`, `hypotheses.json`, `evidence_index/`, `runs/`, `signals/`,
  `research_ideas/`, `audits/`, `reports/`, `raw/`, `case_studies/`,
  `product_profiles/`).

## The `aitoc` topic is special

The seed topic `aitoc` (AI-to-Consumer business models) uses `layout: legacy`,
meaning it maps to the historical root paths (`data/`, `trend_radar/`,
`audits/`, `docs/research_plan.md`, `hypotheses/registry.json`). It has no
folder here so existing files and tooling keep working unchanged.

## Working with topics

```bash
PYTHONPATH=src python3 -m aitoc_research_agent topics             # list topics
PYTHONPATH=src python3 -m aitoc_research_agent new-research "Electric vehicles"
PYTHONPATH=src python3 -m aitoc_research_agent use-topic electric-vehicles
PYTHONPATH=src python3 -m aitoc_research_agent daily-run          # scoped to active topic
PYTHONPATH=src python3 -m aitoc_research_agent daily-run --topic aitoc
```

Resolution order for the active topic: `--topic` flag → `AITOC_TOPIC` env var →
`active_topic` file → default `aitoc`.
