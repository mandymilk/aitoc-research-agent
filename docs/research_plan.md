# AI-to-C Business Model Research Plan

Version: `v0.6.2`
Last updated: 2026-06-09
Owner: Research agent

## 1. Objective

Build a dedicated research agent that can investigate real consumer AI products and answer:

> Has AI-to-C found a sustainable business model, or is it still mainly a large-company money-spend game?

The research should not stop at pricing pages. It should connect product behavior, user segmentation, compute cost, retention, willingness to pay, distribution, and strategic subsidy.

The agent should operate as a recurring trend radar. Each daily or weekly run should start by identifying new AI-to-C trends, research ideas, and target business models before deciding whether any specific company deserves deeper case-study work.

The agent should be tool-grounded. For fresh market claims, it must use tool calls, local evidence files, or manually supplied source material rather than relying on LLM pre-trained data.

## 2. Scope

In scope:

- Consumer-facing AI assistants, companions, productivity tools, search tools, creative tools, education tools, and personal agents.
- Products that sell directly to individuals, even if they are owned by large B2B or platform companies.
- Hybrid products where consumer adoption supports enterprise, ads, developer APIs, hardware, or ecosystem retention.
- Case studies including, but not limited to, Microsoft Copilot, Doubao, ChatGPT, Claude, Gemini, Perplexity, Character.AI, Replika, Notion AI, Canva AI, and education/creator AI tools.
- Newly emerging AI-to-C products, pricing experiments, distribution models, app-store winners, regional products, and monetization patterns.

Out of scope for the first pass:

- Pure enterprise AI agents with no direct consumer product.
- Infrastructure-only model providers unless their consumer product affects the business model.
- Technical model benchmarking without business-model relevance.

## 3. Research Output

The agent should produce four layers of output:

1. Product profiles: one structured file per product.
2. Evidence notes: source-backed observations with confidence levels.
3. Unit-economic models: simplified revenue, cost, margin, and retention assumptions.
4. Synthesis reports: answer the research question with clear claims and caveats.
5. Trend signals: daily/weekly observations that may become research ideas.
6. Research-idea backlog: candidate questions, target models, and case-study candidates.
7. Kindle-ready long-form exports.
8. Notion-ready structured knowledge pages.

## 4. Core Hypotheses

H1: Standalone AI-to-C subscriptions are difficult because heavy users create variable inference costs while casual users churn.

H2: The strongest consumer AI businesses will be hybrid models: subscription plus bundling, ads, enterprise pull-through, marketplace, or ecosystem retention.

H3: Big companies are advantaged because they can subsidize consumer usage using cloud infrastructure, existing paid users, default distribution, identity/data, and strategic patience.

H4: Tiered usage plans, like Doubao's reported consumer tiers, are a natural response to margin pressure: they convert unlimited usage into segmented willingness-to-pay and cost control.

H5: Microsoft's consumer/business convergence is a sign that AI-to-C may survive inside broader productivity subscriptions more easily than as a standalone app.

These are hypotheses, not conclusions. Each should be weakened or revised when evidence from standalone challengers, non-US products, or alternative monetization models contradicts it.

## 5. Research Phases

### Phase 0: Research System Setup

Status: completed

- Create repository structure.
- Define schemas for product profiles and evidence notes.
- Define source quality rules.
- Seed Microsoft and Doubao as anchor cases.
- Build minimal local tooling for plan access, case creation, and evidence validation.
- Define long-term repository organization for a continuing research series.

### Phase 0.5: Long-Term Research Operating System

Status: completed

- Separate evidence, knowledge base, models, findings, and reports.
- Define weekly, monthly, quarterly, and event-driven update loops.
- Define when to create thesis updates.
- Define taxonomy files for business models and survival classifications.
- Add decision records for major research-structure choices.

### Phase 0.6: Trend Radar And Discovery Loop

Status: completed

- Add daily and weekly runbooks.
- Add watchlists for products, categories, business-model patterns, geographies, and source types.
- Add trend-signal and research-idea templates.
- Add scoring rules for whether signals should be promoted.
- Keep Microsoft and Doubao as anchor cases, not as scope boundaries.
- Make discovery the first step of each recurring run.

### Phase 0.7: Tool Calls And API Dependency Design

Status: completed

- Define which claims require tool-backed evidence.
- Define source connector contract.
- Define optional API dependencies and fallbacks.
- Add connector registry and query seeds.
- Add credential policy for API keys.
- Add CLI command for inspecting connector dependencies.

### Phase 0.8: Publishing And Output Design

Status: in progress

- Define canonical source memo format.
- Define Kindle-ready output format.
- Define Notion-ready output format.
- Add publishing runbook.
- Add output target config.
- Add local Kindle HTML export.
- Keep Notion API optional; use Markdown import as v0 fallback.

### Phase 0.9: Research Quality And Audit Controls

Status: in progress

- Add neutral hypothesis registry.
- Add freshness policy and freshness audit command.
- Add falsification policy and falsification audit command.
- Add case-study backlog with challenger coverage.
- Add explicit implementation-limit warning so scaffolding is not confused with live evidence collection.

### Phase 1: Market Map

Status: pending

Create a map of consumer AI product categories:

- General assistant
- Productivity assistant
- Search/answer engine
- Companion/roleplay
- Creative media generation
- Education/tutoring
- Coding assistant for individuals
- Personal finance/life admin
- Device/platform assistant

For each category, record:

- Primary user job
- Pricing shape
- Free-tier generosity
- Compute intensity
- Retention pattern
- Distribution channel
- Strategic owner type

### Phase 2: Anchor Case Studies

Status: pending

Start with anchor cases, but promote new cases from the trend radar:

- Microsoft Copilot: convergence of consumer and business AI inside Microsoft 365, Windows, Edge, Bing, and work subscriptions.
- Doubao: mass-market consumer assistant moving toward reported three-tier paid subscriptions.
- ChatGPT: direct subscription, enterprise/API adjacency, app-store-like GPT ecosystem, and high brand demand.
- Perplexity: consumer search plus subscription, ads, and publisher/data licensing questions.
- Character.AI/Replika: companion retention, emotional use cases, safety constraints, and monetization pressure.

New case studies should be added when a signal or research idea can test the thesis better than the existing anchors.

### Phase 3: Business Model Taxonomy

Status: pending

Classify each product into one or more models:

- Freemium subscription
- Tiered usage subscription
- Credit/compute pack
- Ads-supported free tier
- Marketplace revenue share
- Bundled productivity subscription
- Enterprise cross-sell
- API/developer cross-subsidy
- Hardware or OS attachment
- Data/licensing partnership

### Phase 4: Unit Economics

Status: pending

For each product, estimate:

- Monthly active users
- Paid conversion rate
- ARPPU and blended ARPU
- Gross margin after inference cost
- Retention/churn
- CAC or distribution advantage
- Support, safety, moderation, and compliance costs
- Strategic value outside direct user revenue

Output should be scenario-based, not fake precision:

- Bear case
- Base case
- Bull case

### Phase 5: Survival Test

Status: pending

Evaluate whether each product can survive under three ownership scenarios:

1. Standalone startup paying market cloud/model costs.
2. Large platform with owned distribution and negotiated compute.
3. Ecosystem company using AI to defend or expand an existing paid product.

The key research question is not only "is revenue growing?" but "could this product survive without subsidy or strategic support?"

### Phase 6: Synthesis

Status: pending

Deliver:

- One-page executive answer.
- Product comparison table.
- Business-model taxonomy.
- Evidence-backed explanation of why AI-to-C has or has not found durable economics.
- Watchlist of signals that would change the answer.

## 6. Anchor Observations To Validate

These are not final conclusions. They are starting claims requiring stronger evidence:

- Microsoft has separate but increasingly connected Copilot experiences for consumers, work users, and businesses. The research should test whether this convergence makes AI-to-C economics easier by attaching AI to existing Microsoft 365 revenue.
- Doubao has reportedly introduced consumer subscription tiers in China. The research should test whether tiering is mainly revenue expansion, inference-cost control, or positioning against rivals.
- Consumer AI apps may monetize quickly but struggle with long-term retention. This needs category-by-category evidence.
- Pure unlimited subscription is likely fragile when top users consume disproportionate compute.

## 6.1 Trend Discovery Mandate

Microsoft and Doubao are seed cases, not the target universe.

Every recurring run should first ask:

- What new AI-to-C trend appeared?
- Which business-model lever changed: pricing, usage limits, ads, bundling, marketplace, distribution, retention, cost, or strategic subsidy?
- Does this reveal a new research idea?
- Does this suggest a new target model?
- Does any product deserve promotion into a case study?

The agent should maintain a case-study backlog based on evidence, not on the original examples.

## 7. Evidence Standards

Use this hierarchy:

1. Company pricing pages, terms, investor materials, regulatory filings, official blogs.
2. App-store pages, product documentation, support pages.
3. Third-party analytics with methodology disclosure.
4. Credible news reporting.
5. Expert commentary and market blogs.
6. Forum/user anecdotes, only as weak qualitative signals.

Every major claim should have:

- Source URL
- Retrieval method
- Date accessed
- Claim type
- Confidence level
- Counterevidence field

The agent must not cite LLM memory as evidence. If no tool-backed or stored evidence exists, the claim should remain `unknown`.

## 8. Plan Evolution Rules

This plan is intentionally living.

When new evidence changes the research direction:

- Add an entry to `docs/plan_changelog.md`.
- Update hypotheses rather than silently replacing them.
- Preserve falsified hypotheses with a note explaining why.
- Add new product categories only when they change the research answer.
- Keep product profiles structured so later analysis can compare them.
- Store time-stamped interpretation in `findings/` instead of overwriting the current answer.
- Keep durable product/company/category context in `knowledge_base/`.
- Use `docs/decision_records/` for major process or structure decisions.
- Add trend signals to `trend_radar/signals/` before turning them into case studies.
- Promote research ideas based on score, evidence quality, and thesis impact.
- Record tool/API failures in daily or weekly run notes.
- Treat APIs as optional enhancements unless a task explicitly requires metrics that cannot be obtained from public pages.

## 9. First Milestones

- M1: Complete Microsoft and Doubao product profiles in `data/product_profiles/` and `knowledge_base/products/`.
- M2: Build 10-product comparison table.
- M3: Build first unit-economic model template.
- M4: Write initial memo: "Why AI-to-C monetization is hard."
- M5: Revise thesis based on evidence.
- M6: Publish first monthly review and first thesis update.
- M7: Run the first daily trend scan and create initial trend signals.
- M8: Run the first weekly trend review and promote at least three research ideas.
- M9: Implement first live source connector or define manual evidence workflow for sources without API access.
- M10: Produce first monthly memo as both Kindle-ready HTML and Notion-ready Markdown.
- M11: Run the first freshness audit.
- M12: Run the first falsification audit.
- M13: Complete at least three standalone challenger profiles before publishing the first strong conclusion.

## 10. Long-Term Organization Principle

The research program should preserve four different kinds of material:

- Evidence: source-backed claims, stored as structured notes.
- Knowledge: durable context about products, companies, categories, and markets.
- Findings: dated interpretation of what changed and why it matters.
- Reports: polished outputs for readers.

This separation is necessary because AI-to-C business models change quickly. A product can change free limits, pricing, or bundling without immediately changing the whole thesis. The repo should make that update path explicit.
