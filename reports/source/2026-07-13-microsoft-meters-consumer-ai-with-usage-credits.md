# Microsoft Meters Consumer AI With Usage Credits

Date: 2026-07-13
Version: v0.1
Status: draft
Output targets: Kindle, Notion
Tags: ai-to-c, business-model

## Executive Summary

Microsoft's own Copilot support page (last updated April 2026) confirms that Microsoft meters consumer and business AI usage through an "AI Credits" system rather than offering flat, unlimited access. A company with hyperscale infrastructure still caps and shapes usage — a structural signal about AI-to-C economics, not a one-off pricing tweak. This memo is an early, single-source finding and is intentionally caveated.

## Key Claims

- Claim: Copilot in individual Microsoft 365 plans (Personal, Family, Premium) is subject to AI usage limits governed by "AI Credits"; Microsoft 365 Premium adds advanced AI features, agents (Tasks, Analyst, Researcher, Photos Agent in preview), and an extended usage allowance, while business Copilot Chat offers pay-as-you-go agents.
  Evidence: evidence-2026-07-13-microsoft-per-microsoft-s-copilot-support-page-last-updat
  Confidence: high (source verified) / low (market-wide generalization)
- Claim: Microsoft structures Copilot as three tiers — Microsoft Copilot (free, no sign-in) at copilot.microsoft.com; Copilot Chat included for organizations with an eligible Microsoft 365 license; and Microsoft 365 Copilot as a paid add-on grounded on work data with reasoning agents.
  Evidence: evidence-2026-07-13-microsoft-microsoft-s-copilot-support-page-last-updated-a
  Confidence: high

## What Changed

The 2026-07-05 freshness audit flagged the June 9 Microsoft evidence as stale. Refetching the official support page confirmed the packaging still holds and surfaced the explicit "AI Credits" metering language plus Microsoft 365 Premium's agent lineup.

## Analysis

Even a hyperscaler that can absorb inference cost meters consumer AI. This supports:

- H4 (tiered usage plans as a margin-control response): heavy usage is gated by credits; richer agents are reserved for higher tiers.
- H3 / H5 (platform subsidy and consumer/business convergence): Copilot is layered on existing Microsoft 365 relationships, not sold as a standalone consumer subscription.

It does not resolve H1 (standalone viability). Microsoft is a platform incumbent; its choices do not tell us whether an independent consumer AI app can survive.

## Unit Economics Implication

Usage credits let a provider segment willingness to pay and protect gross margin from heavy users. If credit metering becomes the category default, it implies operators do not believe flat-rate unlimited consumer AI is margin-safe at current prices.

## Open Questions

- What are the exact AI Credit allowances per Microsoft 365 plan? (unknown; official limits page not verified this session)
- What is the current per-user Copilot price? (unknown; pricing page behind a login wall this session)
- Do standalone challengers (ChatGPT, Claude, Gemini) and regional players (Doubao) meter with credits, message caps, or unlimited access?

## Next Actions

- Verify exact AI Credit amounts on the official "AI credits and limits" page.
- Add a standalone-challenger comparison before promoting this to a strong claim.
- Retry the RevenueCat/Simon-Kucher retention and willingness-to-pay sources.

## Sources And Evidence

- Evidence ID: evidence-2026-07-13-microsoft-per-microsoft-s-copilot-support-page-last-updat
- Evidence ID: evidence-2026-07-13-microsoft-microsoft-s-copilot-support-page-last-updated-a
- Source URL: https://support.microsoft.com/en-us/topic/understanding-the-different-microsoft-copilot-experiences-cfff4791-694a-4d90-9c9c-1eb3fb28e842
- Retrieval method: browser (opened 2026-07-13; page last updated April 2026)
