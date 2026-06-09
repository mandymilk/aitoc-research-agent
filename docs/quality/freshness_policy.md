# Freshness Policy

Version: `v0.1`
Last updated: 2026-06-09

## Purpose

AI-to-C market facts decay quickly. The agent should mark stale claims before they contaminate product profiles, case studies, or reports.

## Maximum Age By Claim Type

| Claim Type | Maximum Age | Reason |
| --- | ---: | --- |
| pricing | 7 days | Plans and discounts change frequently. |
| packaging | 14 days | Feature bundles change often. |
| usage_limit | 7 days | Caps and throttles are active monetization levers. |
| app_rank | 1 day | Rankings are volatile. |
| download_estimate | 30 days | Estimates update monthly or weekly. |
| revenue | 90 days | Public evidence is less frequent, but decays. |
| retention | 90 days | Cohort/benchmark data changes slower. |
| cost | 30 days | Model pricing and inference cost change quickly. |
| distribution | 30 days | Default placement and partnerships can shift. |
| strategy | 60 days | Strategy claims need recent support. |
| user_behavior | 30 days | Qualitative signals decay unless historical. |
| competition | 30 days | Category maps change quickly. |

## Audit Output

Freshness audits should write to:

`audits/freshness/YYYY-MM-DD.md`

Each audit should list:

- Stale evidence notes.
- Stale product profiles.
- High-risk claims in reports.
- Required refresh actions.

