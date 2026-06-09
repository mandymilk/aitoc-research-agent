# Research Quality Plan

Version: `v0.1`
Last updated: 2026-06-09

## Why This Exists

The research system can fail in six predictable ways:

- It says "tool-grounded" but does not actually ingest evidence.
- It creates templates instead of research.
- It lets product profiles go stale.
- It defines falsification tests but never checks them.
- It over-samples large-company products.
- It frames an early thesis as a conclusion.

This file turns those risks into operating controls.

## Control 1: Evidence Before Synthesis

No output should make fresh market claims unless they are backed by:

- Evidence note in `data/evidence_index/`.
- Raw source in `data/raw/`.
- Structured product profile in `data/product_profiles/`.
- Manual capture with date and source context.

If none exists, write `unknown`.

## Control 2: Freshness Audit

Every recurring run should check whether evidence has expired.

High-decay claims:

- Pricing.
- Usage limits.
- App rankings.
- Product launch/shutdown.
- Paid tier features.

Medium-decay claims:

- Revenue estimates.
- Download estimates.
- User counts.
- Retention estimates.
- Funding and partnerships.

Low-decay claims:

- Historical product background.
- Company founding facts.
- Older strategic context clearly marked as historical.

## Control 3: Falsification Review

Every weekly run should ask whether new evidence contradicts a hypothesis.

Contradiction does not automatically kill a hypothesis. It should create a falsification audit entry with:

- Hypothesis ID.
- Evidence ID.
- Direction: supports, weakens, contradicts, or ambiguous.
- Reasoning.
- Required follow-up.

## Control 4: Challenger Sampling

The case-study backlog must include credible standalone or hybrid challengers, not only platform-company products.

Minimum active sample:

- 3 platform/big-company products.
- 3 standalone or startup products.
- 2 China-market products.
- 2 companion/creator/education products.
- 2 products with ads, marketplace, commerce, or non-subscription monetization.

This is not a ranking. It is a bias-control sample.

## Control 5: Neutral Thesis Framing

The README should state a working hypothesis, not a conclusion.

Any claim like "AI-to-C cannot survive standalone" must be phrased as a hypothesis until enough evidence is collected across the sample.

## Control 6: Run Completeness

A daily run is incomplete unless it records:

- Sources or connectors attempted.
- Whether any tool/API failed.
- Signals found or explicit "no material signal found."
- Any stale evidence detected.

A weekly run is incomplete unless it records:

- Freshness audit summary.
- Falsification audit summary.
- Case-selection coverage.
- Hypotheses strengthened/weakened.

