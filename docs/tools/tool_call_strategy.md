# Tool Call Strategy

Version: `v0.1`
Last updated: 2026-06-09

## Core Principle

The research agent must not depend on LLM pre-trained memory for market facts.

The LLM can help with:

- Planning searches.
- Extracting claims from gathered sources.
- Classifying evidence.
- Comparing business models.
- Drafting findings and reports.

The LLM must not be the source of truth for:

- Current prices.
- Current product features.
- User numbers.
- Revenue.
- Retention.
- App rankings.
- Funding, acquisitions, shutdowns, or launches.
- Any claim that could have changed recently.

Those must come from tool calls, local evidence files, or explicitly cited sources.

## Tool-Call Layers

### Layer 1: Local Repository Tools

Purpose: read and write the research system.

Examples:

- Create daily and weekly run notes.
- Create trend signals.
- Create research ideas.
- Validate evidence notes.
- Update product profiles.

Dependency: no external API.

Reliability: high.

### Layer 2: Open Web Retrieval

Purpose: discover and verify public sources.

Examples:

- Search official pricing pages.
- Fetch company blogs and documentation.
- Read app-store web listings when accessible.
- Find credible reporting.

Dependency: browser/search access.

Reliability: medium. Pages can change, block automation, or require geography-specific access.

### Layer 3: Structured Public/Commercial APIs

Purpose: track data that cannot be reliably gathered from web pages.

Potential APIs:

- Search API for web discovery.
- News API for media monitoring.
- App-store intelligence API for rankings, downloads, revenue estimates, and category movement.
- Company/filing API for public-company disclosures.
- Website traffic API.
- Pricing-page monitor or diff service.
- Social/listening API for user behavior signals.

Dependency: API keys, budget, and usage limits.

Reliability: medium to high depending on provider.

### Layer 4: Manual Or Semi-Manual Evidence

Purpose: handle sources that are hard to automate.

Examples:

- Screenshots of mobile app pricing screens.
- Region-locked Chinese app-store pages.
- Paywalled reports.
- Analyst PDFs.
- User interviews.

Dependency: human collection or manually supplied files.

Reliability: varies. Must be labeled clearly.

## API Dependency Policy

The agent should be designed with optional APIs, not hard dependencies.

Required for v0:

- None beyond local filesystem and whatever web/search tool the runtime provides.

Recommended for production daily/weekly runs:

- Web search API.
- News/search alert API.
- App intelligence API.
- Public filing/company data API.
- Page-change monitoring API.

Optional advanced dependencies:

- Social listening API.
- Traffic analytics API.
- Subscription benchmark data provider.
- LLM/model pricing API or scraped pricing monitor.

## Source Connector Contract

Each connector should declare:

- Source name.
- Source type.
- Whether it needs an API key.
- Environment variable name for the key.
- Rate limit or cost risk.
- Output format.
- Claims it is allowed to support.
- Fallback source if unavailable.

Example:

```yaml
id: app_intelligence
name: App intelligence provider
requires_api_key: true
env_var: APP_INTELLIGENCE_API_KEY
supports_claims:
  - app_rank
  - download_estimate
  - revenue_estimate
fallback:
  - app_store_web_listing
  - manual_screenshot
```

## Claim Freshness Rules

Use evidence freshness rules by claim type:

- Pricing: verify same day for reports, within 7 days for internal notes.
- Packaging and usage limits: verify within 7 days.
- App ranking: verify same day.
- Revenue/user estimates: verify source publication date and methodology.
- Company strategy: verify against latest official announcement or credible reporting.
- Historical background: older sources are acceptable when clearly historical.

## Fallback Rules

If an API fails:

1. Record the failure in the daily run note.
2. Try an official web source.
3. Try credible reporting.
4. Use manual evidence if available.
5. Mark the claim as `unknown` if evidence is insufficient.

Do not fill gaps from model memory.

## Evidence Provenance

Every gathered claim should preserve:

- Source URL or file path.
- Retrieval date.
- Retrieval method: `api`, `browser`, `search`, `manual`, or `local`.
- Publisher/source owner.
- Raw excerpt or structured payload path when allowed.
- Confidence and limitations.

## Long-Term Direction

The repo should eventually support a connector-based runner:

1. Load source config.
2. Run discovery queries.
3. Store raw outputs.
4. Extract candidate claims.
5. Create evidence notes.
6. Create trend signals.
7. Score and promote signals.

This architecture keeps the agent grounded in observable data while still using the LLM for judgment.

## Current Practical Mode

Until live connectors are implemented, use `create-evidence` to turn manually retrieved or runtime-tool retrieved sources into structured evidence notes.

This is not a substitute for live APIs, but it prevents the research from silently relying on model memory.
