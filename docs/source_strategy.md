# Source Strategy

## Source Hierarchy

Priority order:

1. Official company pricing, support, product, terms, and investor pages.
2. App-store listings and release notes.
3. Regulatory filings and public financial disclosures.
4. Analytics reports with transparent methodology.
5. Reputable technology and business journalism.
6. Specialist market blogs.
7. User anecdotes and social posts.

## Tool Requirement

Fresh market claims must be supported by tool calls, stored evidence, or manually supplied source files. The model's pre-trained knowledge is not acceptable evidence for current AI-to-C pricing, usage limits, rankings, revenue, retention, or product changes.

Use `docs/tools/tool_call_strategy.md` and `configs/source_connectors.json` to decide which retrieval path is appropriate.

## Current Seed Sources

Microsoft:

- Microsoft 365 Copilot pricing: https://www.microsoft.com/en-us/microsoft-365/copilot/pricing
- Microsoft Support on different Copilot experiences, last updated February 2026: https://support.microsoft.com/en-us/topic/understanding-the-different-microsoft-copilot-experiences-cfff4791-694a-4d90-9c9c-1eb3fb28e842
- Microsoft Copilot Studio Licensing Guide, May 2026: https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/bade/documents/products-and-services/en-us/bizapps/Microsoft-Copilot-Studio-Licensing-Guide-May-2026-PUB.pdf

Doubao:

- Reported Doubao paid tiers, May 2026: https://chaobro.com/posts/doubao-paid-subscription-tiers-2026/
- Secondary discussion of Doubao paid tier shift: https://www.100user.com/blog/doubao-strategic-shift-paid-tiers

Consumer AI monetization:

- TechCrunch summary of RevenueCat 2026 subscription-app report: https://techcrunch.com/2026/03/10/ai-powered-apps-can-make-money-but-struggle-with-long-term-retention-new-data-shows/
- Simon-Kucher 2026 paper on monetizing GenAI and AI agents: https://www.simon-kucher.com/sites/default/files/perspectives-files/2026_WP_Monetizing%20GenAI%20and%20AI%20Agents_Simon-Kucher.pdf

## Evidence Note Requirements

Every evidence note should include:

- `source_url`
- `retrieval_method`
- `source_title`
- `publisher`
- `published_date`
- `accessed_date`
- `claim`
- `claim_type`
- `confidence`
- `counterevidence`
- `research_implication`

Valid retrieval methods:

- `api`
- `browser`
- `search`
- `manual`
- `local`

## Claim Types

- `pricing`
- `packaging`
- `usage_limit`
- `retention`
- `revenue`
- `cost`
- `distribution`
- `strategy`
- `user_behavior`
- `competition`
