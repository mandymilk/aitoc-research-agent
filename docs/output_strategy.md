# Output Strategy

Version: `v0.1`
Last updated: 2026-06-09

## Purpose

The research agent should produce outputs that are ready for two reading workflows:

- Kindle: focused long-form reading, low distraction, readable on e-ink.
- Notion: structured knowledge management, searchable pages, databases, backlinks, and future editing.

The same research should not be rewritten twice. The agent should create a canonical source memo, then export channel-specific versions.

## Output Layers

### 1. Canonical Source

Location: `reports/source/`

Format: Markdown.

Purpose: the source of truth for a memo, case study, monthly review, or thesis update.

Rules:

- Include title, date, version, status, and evidence references.
- Keep citations and source notes in a stable section.
- Use clear headings.
- Avoid layout tricks that do not transfer to Kindle or Notion.

### 2. Kindle Output

Location: `outputs/kindle/`

Preferred formats:

- `.html`: easiest local export without dependencies and accepted by Send to Kindle conversion workflows.
- `.md`: useful backup and easy to convert later.
- `.epub`: recommended future format if Pandoc, Calibre, or another ebook builder is added.
- `.docx`: useful if using Word-based workflows, but not required for v0.

Kindle reading requirements:

- Strong title.
- Short executive summary.
- Table of contents for long reports.
- Short sections.
- Few wide tables.
- Tables should be rewritten as bullets when possible.
- Full source list at the end.
- No dependence on color.
- No embedded web-only formatting.

### 3. Notion Output

Location: `outputs/notion/`

Preferred formats:

- Markdown page package for manual Notion import.
- Future: Notion API page creation.

Notion reading requirements:

- Metadata block at the top.
- Summary.
- Key claims.
- Evidence links.
- Open questions.
- Follow-up tasks.
- Tags for product, company, category, business model, geography, and confidence.

## Recommended Output Types

### Daily Trend Note

Use for quick operational review.

Primary destination: Notion.

Secondary destination: none unless important.

### Weekly Trend Review

Use for ongoing research tracking.

Primary destination: Notion.

Secondary destination: Kindle only if it contains narrative synthesis.

### Monthly Research Memo

Use for deeper thinking.

Primary destination: Kindle and Notion.

### Case Study

Use for product/company-specific research.

Primary destination: Notion.

Secondary destination: Kindle when long-form.

### Thesis Update

Use when the main view changes.

Primary destination: Notion.

Secondary destination: Kindle if it becomes essay-length.

## Publication Pipeline

1. Draft canonical Markdown in `reports/source/`.
2. Check that factual claims trace to evidence notes or source URLs.
3. Export Kindle version to `outputs/kindle/`.
4. Export Notion-ready version to `outputs/notion/`.
5. Archive old versions when conclusions change.

## Kindle-Specific Guidance

Send to Kindle support changes over time. As of current public guidance and recent support references, common accepted personal document formats include EPUB, PDF, DOC/DOCX, RTF, TXT, HTML/HTM, and common image formats. For this repo, HTML is the v0 export target because it can be generated locally without extra dependencies and keeps headings readable.

EPUB should be added later when the project has a stable external converter dependency.

## Notion-Specific Guidance

Use Markdown as the v0 export target because it can be imported manually into Notion and can also be transformed into Notion API blocks later.

Notion API publishing should:

- Create or update a page in a configured database.
- Map metadata to database properties.
- Convert headings, bullets, quotes, and links into Notion blocks.
- Attach source links and evidence IDs.
- Avoid pushing raw private notes unless explicitly marked publishable.

The v0.6.2 implementation creates a page and appends simple Markdown-derived blocks. It does not yet update existing pages or map rich database properties beyond title.
