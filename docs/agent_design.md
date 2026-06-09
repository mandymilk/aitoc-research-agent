# Dedicated Research Agent Design

## Agent Mission

The agent researches AI-to-C products as businesses, not just technologies. Its job is to determine which consumer AI products can survive economically and why.

The agent is also a recurring trend radar. It should identify new AI-to-C monetization patterns before deciding which companies or products deserve deeper case-study work.

The agent must be tool-grounded. It should never use LLM pre-trained memory as the source of truth for current market facts.

The agent must also be falsification-oriented. It should look for evidence that weakens the starting thesis, especially from standalone challengers and non-platform products.

## Agent Roles

The research system can be run by one agent, but it should behave as five specialist roles:

- Trend scout: scans for new AI-to-C pricing, distribution, retention, cost, and monetization signals.
- Market mapper: identifies categories, products, geographies, and user jobs.
- Product analyst: records features, pricing, packaging, distribution, and usage limits.
- Evidence auditor: ranks sources, stores claims, and flags weak evidence.
- Freshness auditor: flags evidence and product profiles whose claims have decayed.
- Falsification auditor: maps new evidence to hypotheses and identifies contradictions.
- Unit-economics analyst: builds scenarios for revenue, cost, retention, and margin.
- Synthesis writer: converts evidence into an answer with caveats and decision implications.

## Workflow

1. Run trend discovery.
2. Create and score trend signals.
3. Promote strong signals into research ideas or target business models.
4. Select product, company, category, or model for deeper research.
5. Use tool calls or stored local evidence to collect official sources first.
6. Add credible secondary sources through tool calls or manually supplied files.
7. Extract claims into evidence notes with source provenance.
8. Fill product profile.
9. Estimate business-model mechanics.
10. Run survival test across ownership scenarios.
11. Compare against prior products.
12. Update findings, synthesis, and plan changelog.

## Quality Gates

Before publishing a strong claim:

- Freshness audit must not show stale support for that claim.
- Falsification audit must review contradictory evidence.
- Case sample must include credible standalone challengers.
- Unsupported current facts must be marked `unknown`.

## Tool-Grounded Research Rules

- Current pricing, packaging, usage limits, app rankings, downloads, revenue, retention, partnerships, shutdowns, and acquisitions require tool-backed evidence.
- The LLM may suggest search queries and summarize retrieved sources, but it cannot be cited as evidence.
- If a source cannot be reached, the claim remains `unknown`.
- When a tool/API fails, record the failure in the daily or weekly run note.
- Every factual claim in a finding should trace back to an evidence note, product profile, source URL, or manually captured file.

## Trend Discovery Loop

Each daily or weekly run should scan for:

- Pricing changes.
- Usage-limit changes.
- Ads, commerce, marketplace, or other monetization experiments.
- Distribution shifts through OS, browser, app store, device, or super-app placement.
- Retention or churn signals.
- Cost and heavy-user control signals.
- New product behaviors such as agents, companions, tutors, creator tools, or personal operating systems.
- Company strategy changes such as acquisition, shutdown, bundling, enterprise pull-through, or ecosystem defense.

The agent should not create a full case study for every signal. It should first decide whether the signal is isolated noise, an early pattern, or a thesis-changing trend.

## Research Loop

For each product, ask:

- Who is the paying user?
- What is the repeated job to be done?
- What behavior creates cost?
- What usage is free, capped, throttled, or tiered?
- What feature is paywalled?
- What makes users stay after novelty fades?
- What distribution channel lowers acquisition cost?
- What strategic owner benefits even if direct margin is weak?
- What evidence would prove this model is sustainable?

## Survival Test

The agent should mark each product as one of:

- `standalone_viable`: likely viable as an independent consumer business.
- `hybrid_viable`: viable only with ads, B2B, marketplace, API, or platform economics.
- `strategic_subsidy`: valuable mainly as part of a larger company strategy.
- `not_yet_viable`: user demand exists, but business-model evidence is weak.
- `unknown`: not enough evidence.

## Non-Goals

- Do not rank products by model quality.
- Do not write generic AI hype summaries.
- Do not assume revenue equals profitability.
- Do not treat user growth as sustainability.
- Do not ignore compute cost just because model prices are falling.
- Do not fill missing current facts from LLM memory.
