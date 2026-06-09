# Publishing Setup

Version: `v0.1`
Last updated: 2026-06-09

## Kindle Delivery

The repo can send a Kindle-ready export by email attachment.

Required environment variables:

- `KINDLE_TO_EMAIL`: your Send-to-Kindle email address.
- `KINDLE_SMTP_HOST`: SMTP server host.
- `KINDLE_SMTP_USERNAME`: SMTP username.
- `KINDLE_SMTP_PASSWORD`: SMTP password or app password.

Optional:

- `KINDLE_FROM_EMAIL`: sender email. Defaults to `KINDLE_SMTP_USERNAME`.
- `KINDLE_SMTP_PORT`: defaults to `587`.

Important setup outside this repo:

- Add `KINDLE_FROM_EMAIL` to Amazon's approved personal document sender list.
- Use an app password if your email provider requires one.

Command:

```bash
PYTHONPATH=src python3 -m aitoc_research_agent publish-kindle reports/source/example.md
```

If the source is Markdown, the command exports a Kindle-friendly HTML file first, then emails it as an attachment.

## Notion Publishing

The repo can create a Notion page through the Notion API.

Required environment variables:

- `NOTION_API_KEY`: your Notion integration token.
- One of:
  - `NOTION_PAGE_ID`: create the research doc under a parent page.
  - `NOTION_DATABASE_ID`: create the research doc as a database item.

Important setup outside this repo:

- Create a Notion integration.
- Give the integration access to the target page or database.
- Ensure the integration has insert-content capability.

Command:

```bash
PYTHONPATH=src python3 -m aitoc_research_agent publish-notion reports/source/example.md
```

The implementation uses Notion API version `2026-03-11`.

## Security

Do not commit real credentials.

Use shell environment variables, a local untracked `.env`, a password manager, or your automation platform's secret store.

