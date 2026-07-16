# AGENTS.md — Running This Research Agent Inside a Coding Agent

This file tells a coding agent (Codex, Claude Code, or any agent that reads
`AGENTS.md`) how to operate this repository. The goal is to run the AI-to-C
business-model research loop using the **runtime's own web search and page-fetch
tools** as the evidence-retrieval path, instead of a paid search API.

Read this file first, then `README.md`, then `docs/agent_design.md`.

## What This Repo Is

A living research system studying whether consumer AI products can be durable
standalone businesses or whether they depend on big-company subsidy, distribution,
and cross-subsidy. It separates evidence (`data/`), durable notes
(`knowledge_base/`), dated conclusions (`findings/`), and polished output
(`reports/`, `outputs/`). See `README.md` for the full map.

## Runtime Retrieval Mode (Important)

The design (`docs/tools/tool_call_strategy.md`, "Layer 2: Open Web Retrieval")
explicitly allows using "whatever web/search tool the runtime provides." When
running inside a coding agent, that runtime tool **is** the retrieval layer:

- Use the agent's built-in **web search** tool (Codex web search, Claude Code
  `WebSearch`) for discovery — finding candidate sources.
- Use the agent's built-in **page fetch/browse** tool (Claude Code `WebFetch`,
  or an equivalent fetch/open-URL tool) to open and read the actual source.
- The bundled `web-fetch` connector / `fetch_url` helper in
  `src/aitoc_research_agent/connectors/web_fetch.py` is a plain-`urllib`
  fallback for machine-readable pages. Prefer the runtime tools when a page
  needs JavaScript, blocks bots, or is region-specific.

Do **not** require `WEB_SEARCH_API_KEY`, `NEWS_API_KEY`, or any paid API to do
research. Those remain optional accelerators only. The `runtime_web_search`
connector in `configs/source_connectors.json` documents this no-API-key path.

## Non-Negotiable Evidence Rules

These come from `docs/agent_design.md` and `docs/tools/tool_call_strategy.md`:

1. **Never use model memory as the source of truth** for current pricing,
   packaging, usage limits, rankings, downloads, revenue, retention, funding,
   acquisitions, shutdowns, or launches. Every such claim must trace to a URL
   you actually opened this session.
2. The LLM may plan searches, summarize opened pages, classify claims, and draft
   findings — but it may not be cited as evidence.
3. If a source cannot be opened/verified, mark the claim `unknown`. Do not fill
   the gap.
4. Prefer official sources first (company pricing/docs/investor pages), then
   app-store listings, filings, transparent analytics, then reputable
   journalism. See `docs/source_strategy.md`.
5. Record tool/retrieval failures in the daily or weekly run note.

## Standard Research Loop (Per Session)

Run every CLI command with `PYTHONPATH=src python3 -m aitoc_research_agent ...`
(or `aitoc-research ...` if the package is installed). No third-party
dependencies are required — it is pure standard library.

0. **Pick or create a topic.** Everything is scoped to a research topic. List
   topics with `topics`; select one with `use-topic <slug>`; create a new one
   with `new-research "<topic title>"` (scaffolds a `topics/<slug>/` folder with
   a plan and hypotheses to fill in). The default topic is `aitoc` (AI-to-C
   business models). You can also pass `--topic <slug>` to individual commands.
   Active-topic resolution: `--topic` → `AITOC_TOPIC` env → `topics/active_topic`
   file → default `aitoc`. See `topics/README.md` and decision record 0002.
1. **Start a run note:** `daily-run` (or `weekly-run`). Read the printed path.
2. **Discover:** use the runtime web search tool for the trend-discovery targets
   listed in `docs/agent_design.md` (pricing changes, usage-limit changes, ads/
   commerce experiments, distribution shifts, retention signals, cost controls,
   strategy changes).
3. **Open & read sources:** use the runtime fetch/browse tool to open each
   candidate URL and extract the exact claim and its published date.
4. **Record evidence** for each verified claim:
   ```
   PYTHONPATH=src python3 -m aitoc_research_agent create-evidence \
     --source-url "<url you opened>" \
     --retrieval-method search   # or: browser
     --source-title "<page title>" \
     --publisher "<owner>" \
     --published-date "YYYY-MM-DD" \
     --claim "<verbatim/tight paraphrase>" \
     --claim-type pricing \
     --confidence medium \
     --research-implication "<why it matters for the thesis>"
   ```
   Use `--retrieval-method search` when the runtime web-search tool surfaced and
   opened the page; use `browser` when you fetched a specific known URL.
5. **Validate:** `validate-evidence data/evidence_index/<id>.json`.
6. **Promote:** create `new-signal` for a fresh pattern; `new-idea` if it affects
   a business-model question.
7. **Update structure:** update the product profile in `data/product_profiles/`,
   then the durable note in `knowledge_base/`.
8. **Audit before concluding:** run `audit-freshness` and `audit-falsification`.
   Do not publish a strong claim with stale support (see freshness windows in
   `MAX_AGE_DAYS_BY_CLAIM_TYPE` in `src/aitoc_research_agent/cli.py`, e.g. pricing
   = 7 days, app_rank = 1 day).
9. **Synthesize:** add a `findings/weekly/` entry; a thesis update only if the
   main argument changes; update `reports/` last.
10. **Publish (mandatory, do not skip):** create a memo with `new-memo`, fill it
    from the evidence, then `export-kindle` and `export-notion`. Whenever the
    publishing env is configured, you MUST also `publish-kindle` (sends the
    Kindle email) and `publish-notion` (creates the page). Every run finishes the
    full pipeline including delivery — do not stop at drafts.
11. **Verify before calling it done:** run `verify-run --date <date>` for the
    topic, and `verify-run --all` to verify the whole project (every topic's
    latest run). It must print `RESULT: complete` / `PROJECT RESULT: complete`
    (exit 0). It checks the run note, evidence, hypotheses, both audits, the
    memo, and the Kindle/Notion publish receipts (required when the env is
    configured). If it reports `INCOMPLETE`, finish the missing stage and re-run
    before declaring the run done.

## Retrieval-Method Mapping

| How you got the source (in this runtime) | `--retrieval-method` |
| --- | --- |
| Runtime web search surfaced and you opened it | `search` |
| You fetched a specific known URL / official page | `browser` |
| Read from a file already in the repo | `local` |
| Screenshot / paywalled / region-locked, supplied by human | `manual` |
| Paid connector API (not required here) | `api` |

## Quality Gates (from `docs/agent_design.md`)

Before publishing a strong claim: freshness audit clean for that claim,
falsification audit reviewed, case sample includes credible standalone
challengers, and unsupported current facts marked `unknown`.

## Useful Commands

- `plan` — print the master research plan.
- `topics` — list research topics and show the active one.
- `use-topic <slug>` — set the active research topic.
- `new-research "<title>"` — scaffold a new topic (`topics/<slug>/`).
- `daily-run` / `weekly-run` — dated run notes.
- `new-signal "<title>"` / `new-idea "<title>"` — trend pipeline.
- `create-evidence ...` / `validate-evidence <path>` — evidence intake.
- `audit-freshness` / `audit-falsification` — quality audits.
- `verify-run` — end-to-end completion check (fails if publish receipts missing when env is set). Use `--all` for whole-project verification across every topic.
- `hypotheses` / `case-coverage` / `connectors` — status views.
- `new-memo` / `export-kindle` / `export-notion` — output (publishing needs
  private credentials in `.env`; see `configs/env.example`).

## Do Not

- Do not commit secrets. `.env` is gitignored; only `configs/env.example` is
  tracked.
- Do not invent numbers, prices, or rankings from memory.
- Do not treat user growth or revenue as proof of profitability.
- Do not create a full case study for every signal — triage first.
