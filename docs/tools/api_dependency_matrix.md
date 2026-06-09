# API Dependency Matrix

Version: `v0.1`
Last updated: 2026-06-09

## Summary

The agent should be useful without paid APIs, but better with them.

Minimum viable mode:

- Local repo tools.
- Runtime web search/browser access.
- Manual source entry.

Production research mode:

- Search/news monitoring.
- App intelligence.
- Public company filings.
- Page-change monitoring.
- Optional traffic and social data.

## Dependency Tiers

| Capability | Needed For | Required? | API Needed? | Fallback |
| --- | --- | --- | --- | --- |
| Local file operations | Plans, notes, schemas, reports | Yes | No | None |
| Web search | Discovery and source finding | Yes for live research | Runtime dependent | Manual source list |
| Browser/page fetch | Official pricing and docs | Yes for verification | Runtime dependent | Manual evidence |
| News monitoring | Daily/weekly trend discovery | Recommended | Usually yes | Search queries |
| App intelligence | Downloads, revenue estimates, rankings | Recommended | Usually yes | App-store pages and secondary reports |
| Filing/company data | Public-company strategy and financials | Recommended | Sometimes | Investor relations pages |
| Page-change monitoring | Pricing/free-tier changes | Recommended | Sometimes | Scheduled page fetch + diff |
| Traffic analytics | Web adoption signals | Optional | Usually yes | Public ranking estimates |
| Social listening | User behavior and complaints | Optional | Usually yes | Manual qualitative scan |
| LLM/model pricing monitor | Cost-model inputs | Recommended | Sometimes | Official pricing pages |
| Notion publishing | Create or update Notion pages | Optional | Yes | Markdown import |
| Kindle export | Reader-friendly long-form files | Recommended | No for HTML, yes only for cloud delivery automation | Manual Send to Kindle |

## Recommended Environment Variables

Do not commit secrets.

Potential variables:

- `WEB_SEARCH_API_KEY`
- `NEWS_API_KEY`
- `APP_INTELLIGENCE_API_KEY`
- `FILING_API_KEY`
- `TRAFFIC_ANALYTICS_API_KEY`
- `SOCIAL_LISTENING_API_KEY`
- `PAGE_MONITOR_API_KEY`
- `MODEL_PRICING_API_KEY`
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`

## What Must Be Source-Backed

Always require a fresh source or stored evidence:

- Product price.
- Paid tier features.
- Free-tier limits.
- App ranking.
- Download estimate.
- Revenue estimate.
- User count.
- Retention/churn.
- Company launch, shutdown, acquisition, or partnership.
- Public financial claim.
- Regulation or policy change.

## What Can Be LLM-Assisted

LLM assistance is acceptable for:

- Suggesting search queries.
- Grouping signals.
- Drafting hypotheses.
- Comparing business-model patterns.
- Generating checklists.
- Writing memos from cited evidence.

But the LLM should cite stored evidence or retrieved sources for factual claims.
