from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

from aitoc_research_agent.connectors.web_fetch import fetch_url
from aitoc_research_agent.publishers.kindle_email import send_to_kindle
from aitoc_research_agent.publishers.notion_api import create_notion_page


ROOT = Path(__file__).resolve().parents[2]
PLAN_PATH = ROOT / "docs" / "research_plan.md"
CASE_DIR = ROOT / "docs" / "case_studies"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas" / "evidence_item.schema.json"
CONNECTOR_CONFIG_PATH = ROOT / "configs" / "source_connectors.json"
HYPOTHESIS_REGISTRY_PATH = ROOT / "hypotheses" / "registry.json"
CASE_BACKLOG_PATH = ROOT / "trend_radar" / "case_backlog" / "candidate_backlog.json"
EVIDENCE_INDEX_DIR = ROOT / "data" / "evidence_index"
RAW_DATA_DIR = ROOT / "data" / "raw"
FRESHNESS_AUDIT_DIR = ROOT / "audits" / "freshness"
FALSIFICATION_AUDIT_DIR = ROOT / "audits" / "falsification"
SOURCE_REPORT_DIR = ROOT / "reports" / "source"
KINDLE_OUTPUT_DIR = ROOT / "outputs" / "kindle"
NOTION_OUTPUT_DIR = ROOT / "outputs" / "notion"
DAILY_RUN_DIR = ROOT / "trend_radar" / "runs" / "daily"
WEEKLY_RUN_DIR = ROOT / "trend_radar" / "runs" / "weekly"
TREND_SIGNAL_DIR = ROOT / "trend_radar" / "signals"
RESEARCH_IDEA_DIR = ROOT / "trend_radar" / "research_ideas"


REQUIRED_EVIDENCE_FIELDS = {
    "id",
    "source_url",
    "retrieval_method",
    "source_title",
    "publisher",
    "accessed_date",
    "claim",
    "claim_type",
    "confidence",
    "research_implication",
}

VALID_CLAIM_TYPES = {
    "acquisition",
    "app_rank",
    "competition",
    "cost",
    "discovery",
    "distribution",
    "download_estimate",
    "funding",
    "packaging",
    "pricing",
    "revenue",
    "revenue_estimate",
    "retention",
    "shutdown",
    "strategy",
    "traffic_estimate",
    "usage_limit",
    "user_behavior",
}

VALID_CONFIDENCE = {"low", "medium", "high"}
VALID_RETRIEVAL_METHODS = {"api", "browser", "search", "manual", "local"}
MAX_AGE_DAYS_BY_CLAIM_TYPE = {
    "pricing": 7,
    "packaging": 14,
    "usage_limit": 7,
    "app_rank": 1,
    "download_estimate": 30,
    "revenue": 90,
    "retention": 90,
    "cost": 30,
    "distribution": 30,
    "strategy": 60,
    "user_behavior": 30,
    "competition": 30,
    "discovery": 14,
    "funding": 60,
    "shutdown": 60,
    "acquisition": 60,
    "revenue_estimate": 30,
    "traffic_estimate": 30,
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "new-product"


def show_plan(_: argparse.Namespace) -> int:
    print(PLAN_PATH)
    print()
    print(PLAN_PATH.read_text(encoding="utf-8"))
    return 0


def new_case(args: argparse.Namespace) -> int:
    CASE_DIR.mkdir(parents=True, exist_ok=True)
    path = CASE_DIR / f"{slugify(args.product_name)}.md"
    if path.exists() and not args.force:
        print(f"Case study already exists: {path}", file=sys.stderr)
        return 1

    title = args.product_name.strip()
    content = f"""# Case Study: {title}

Status: draft
Last updated: 2026-06-09

## Why This Case Matters

TODO

## Starting Claims To Validate

- TODO

## Business Model Angles

- TODO

## Key Questions

- Who pays?
- What usage creates cost?
- What is free, capped, tiered, or bundled?
- What distribution advantage exists?
- Can this survive as a standalone business?

## Evidence Needed

- Official pricing and packaging.
- Usage limits.
- Retention and conversion signals.
- Distribution channel evidence.
- Strategic subsidy evidence.

## Provisional Classification

`unknown`

Confidence: low
"""
    path.write_text(content, encoding="utf-8")
    print(path)
    return 0


def write_if_allowed(path: Path, content: str, force: bool) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"File already exists: {path}", file=sys.stderr)
        return 1
    path.write_text(content, encoding="utf-8")
    print(path)
    return 0


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_dotenv(path: Path = ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def today_string(value: str | None) -> str:
    return value or date.today().isoformat()


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def is_valid_uri(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https", "file"} and bool(parsed.netloc or parsed.scheme == "file")


def validate_evidence_data(data: dict) -> list[str]:
    allowed_fields = {
        "id",
        "source_url",
        "retrieval_method",
        "source_title",
        "publisher",
        "published_date",
        "accessed_date",
        "claim",
        "claim_type",
        "confidence",
        "counterevidence",
        "research_implication",
    }
    errors: list[str] = []
    missing = sorted(REQUIRED_EVIDENCE_FIELDS - set(data))
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")

    extra = sorted(set(data) - allowed_fields)
    if extra:
        errors.append(f"Unexpected fields: {', '.join(extra)}")

    string_fields = allowed_fields - {"counterevidence", "published_date"}
    for field in sorted(string_fields & set(data)):
        if not isinstance(data[field], str):
            errors.append(f"{field} must be a string")
        elif field in REQUIRED_EVIDENCE_FIELDS and not data[field].strip():
            errors.append(f"{field} must not be empty")

    for field in ["counterevidence", "published_date"]:
        if field in data and not isinstance(data[field], str):
            errors.append(f"{field} must be a string")

    if isinstance(data.get("source_url"), str) and not is_valid_uri(data["source_url"]):
        errors.append(f"Invalid source_url: {data.get('source_url')}")

    if data.get("claim_type") not in VALID_CLAIM_TYPES:
        errors.append(f"Invalid claim_type: {data.get('claim_type')}")

    if data.get("confidence") not in VALID_CONFIDENCE:
        errors.append(f"Invalid confidence: {data.get('confidence')}")

    if data.get("retrieval_method") not in VALID_RETRIEVAL_METHODS:
        errors.append(f"Invalid retrieval_method: {data.get('retrieval_method')}")

    for field in ["accessed_date", "published_date"]:
        value = data.get(field)
        if isinstance(value, str) and value:
            try:
                parse_iso_date(value)
            except ValueError:
                errors.append(f"Invalid {field}: {value}")

    return errors


def validate_product_profile_data(data: dict) -> list[str]:
    required = {
        "product_name",
        "company",
        "geography",
        "category",
        "user_jobs",
        "pricing_model",
        "free_tier",
        "paid_tiers",
        "distribution_channels",
        "compute_intensity",
        "retention_assessment",
        "strategic_subsidy_sources",
        "survival_classification",
        "confidence",
        "evidence_ids",
        "open_questions",
    }
    allowed = required
    errors: list[str] = []
    missing = sorted(required - set(data))
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    extra = sorted(set(data) - allowed)
    if extra:
        errors.append(f"Unexpected fields: {', '.join(extra)}")
    if data.get("confidence") not in VALID_CONFIDENCE:
        errors.append(f"Invalid confidence: {data.get('confidence')}")
    if data.get("survival_classification") not in {
        "standalone_viable",
        "hybrid_viable",
        "strategic_subsidy",
        "not_yet_viable",
        "unknown",
    }:
        errors.append(f"Invalid survival_classification: {data.get('survival_classification')}")
    for field in ["geography", "user_jobs", "pricing_model", "paid_tiers", "distribution_channels", "strategic_subsidy_sources", "evidence_ids", "open_questions"]:
        if field in data and not isinstance(data[field], list):
            errors.append(f"{field} must be a list")
    return errors


def new_daily_run(args: argparse.Namespace) -> int:
    run_date = today_string(args.date)
    content = f"""# Daily AI-to-C Trend Run: {run_date}

## Scan Summary

TODO

## Signals Created

| Signal | Category | Score | Promotion |
| --- | --- | --- | --- |
|  |  |  |  |

## Research Ideas Created

- TODO

## Product Profiles Updated

- TODO

## Case-Study Candidates

- TODO

## Thesis Impact

- TODO

## Next Actions

- TODO
"""
    return write_if_allowed(DAILY_RUN_DIR / f"{run_date}.md", content, args.force)


def new_weekly_run(args: argparse.Namespace) -> int:
    run_date = today_string(args.date)
    content = f"""# Weekly AI-to-C Trend Review: {run_date}

## Executive Summary

TODO

## Repeated Patterns

- TODO

## Strongest Signals

| Signal | Category | Score | Action |
| --- | --- | --- | --- |
|  |  |  |  |

## New Research Ideas

- TODO

## Case-Study Backlog Changes

- TODO

## Hypothesis Impact

- H1:
- H2:
- H3:
- H4:
- H5:

## Next Week Agenda

- TODO
"""
    return write_if_allowed(WEEKLY_RUN_DIR / f"{run_date}.md", content, args.force)


def new_trend_signal(args: argparse.Namespace) -> int:
    signal_date = today_string(args.date)
    slug = slugify(args.title)
    content = f"""# Trend Signal: {args.title}

Date observed: {signal_date}
Status: draft
Score: {args.score}

## Signal

TODO

## Why It Matters

TODO

## Category

- TODO

## Products Or Companies Affected

- TODO

## Evidence

- Source:
- Evidence note:
- Confidence:

## Interpretation

TODO

## Promotion Decision

Choose one:

- Keep as signal.
- Promote to research idea.
- Promote to case-study candidate.
- Ignore after review.

## Follow-Up

- TODO
"""
    return write_if_allowed(TREND_SIGNAL_DIR / f"{signal_date}-{slug}.md", content, args.force)


def new_research_idea(args: argparse.Namespace) -> int:
    idea_date = today_string(args.date)
    slug = slugify(args.title)
    content = f"""# Research Idea: {args.title}

Date created: {idea_date}
Status: draft
Priority: {args.priority}

## Question

TODO

## Why Now

TODO

## Target Business Model

- TODO

## Candidate Products

- TODO

## Evidence Needed

- TODO

## Possible Thesis Impact

TODO
"""
    return write_if_allowed(RESEARCH_IDEA_DIR / f"{idea_date}-{slug}.md", content, args.force)


def new_memo(args: argparse.Namespace) -> int:
    memo_date = today_string(args.date)
    slug = slugify(args.title)
    content = f"""# {args.title}

Date: {memo_date}
Version: v0.1
Status: draft
Output targets: Kindle, Notion
Tags: ai-to-c, business-model

## Executive Summary

TODO

## Key Claims

- Claim:
  Evidence:
  Confidence:

## What Changed

TODO

## Analysis

TODO

## Unit Economics Implication

TODO

## Open Questions

- TODO

## Next Actions

- TODO

## Sources And Evidence

- Evidence ID:
- Source URL:
- Retrieval method:
"""
    return write_if_allowed(SOURCE_REPORT_DIR / f"{memo_date}-{slug}.md", content, args.force)


def markdown_to_simple_html(markdown: str, title: str) -> str:
    body: list[str] = []
    in_list = False
    in_code = False
    open_li = False
    in_table = False
    table_header_done = False
    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_list:
                if open_li:
                    body.append("</li>")
                    open_li = False
                body.append("</ul>")
                in_list = False
            if in_table:
                body.append("</table>")
                in_table = False
                table_header_done = False
            if in_code:
                body.append("</code></pre>")
                in_code = False
            else:
                body.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            body.append(html.escape(line))
            continue
        if not line:
            if in_list:
                if open_li:
                    body.append("</li>")
                    open_li = False
                body.append("</ul>")
                in_list = False
            if in_table:
                body.append("</table>")
                in_table = False
                table_header_done = False
            continue
        if line.startswith("#"):
            if in_list:
                if open_li:
                    body.append("</li>")
                    open_li = False
                body.append("</ul>")
                in_list = False
            if in_table:
                body.append("</table>")
                in_table = False
                table_header_done = False
            level = min(len(line) - len(line.lstrip("#")), 4)
            text = html.escape(line[level:].strip())
            body.append(f"<h{level}>{text}</h{level}>")
        elif line.startswith("- "):
            if in_table:
                body.append("</table>")
                in_table = False
                table_header_done = False
            if not in_list:
                body.append("<ul>")
                in_list = True
            if open_li:
                body.append("</li>")
            body.append(f"<li>{inline_markdown_to_html(line[2:].strip())}")
            open_li = True
        elif in_list and (line.startswith("  ") or line.startswith("\t")):
            body.append(f"<br>{inline_markdown_to_html(line.strip())}")
        elif line.startswith("|") and line.endswith("|"):
            if in_list:
                if open_li:
                    body.append("</li>")
                    open_li = False
                body.append("</ul>")
                in_list = False
            cells = [inline_markdown_to_html(cell.strip()) for cell in line.strip("|").split("|")]
            if all(set(cell.replace(":", "").replace("-", "").strip()) == set() for cell in cells):
                continue
            if not in_table:
                body.append("<table>")
                in_table = True
                table_header_done = False
            tag = "td" if table_header_done else "th"
            body.append("<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in cells) + "</tr>")
            table_header_done = True
        else:
            if in_list:
                if open_li:
                    body.append("</li>")
                    open_li = False
                body.append("</ul>")
                in_list = False
            if in_table:
                body.append("</table>")
                in_table = False
                table_header_done = False
            body.append(f"<p>{inline_markdown_to_html(line)}</p>")
    if in_list:
        if open_li:
            body.append("</li>")
        body.append("</ul>")
    if in_code:
        body.append("</code></pre>")
    if in_table:
        body.append("</table>")

    escaped_title = html.escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escaped_title}</title>
  <style>
    body {{
      font-family: Georgia, serif;
      line-height: 1.55;
      max-width: 720px;
      margin: 2rem auto;
      padding: 0 1rem;
      color: #111;
    }}
    h1, h2, h3, h4 {{
      line-height: 1.25;
      margin-top: 1.6em;
    }}
    p, li {{
      font-size: 1rem;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      font-size: 0.9rem;
    }}
    th, td {{
      border: 1px solid #999;
      padding: 0.35rem;
      vertical-align: top;
    }}
    code, pre {{
      font-family: monospace;
    }}
  </style>
</head>
<body>
{chr(10).join(body)}
</body>
</html>
"""


def inline_markdown_to_html(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def title_from_markdown(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def export_kindle(args: argparse.Namespace) -> int:
    source = resolve_repo_path(args.source)
    markdown = source.read_text(encoding="utf-8")
    title = title_from_markdown(markdown, source.stem)
    output = KINDLE_OUTPUT_DIR / f"{source.stem}.html"
    html_output = markdown_to_simple_html(markdown, title)
    return write_if_allowed(output, html_output, args.force)


def export_notion(args: argparse.Namespace) -> int:
    source = resolve_repo_path(args.source)
    markdown = source.read_text(encoding="utf-8")
    output = NOTION_OUTPUT_DIR / f"{source.stem}.md"
    return write_if_allowed(output, notion_export_content(source, markdown), args.force)


def notion_export_content(source: Path, markdown: str) -> str:
    title = title_from_markdown(markdown, source.stem)
    source_label = source.relative_to(ROOT) if source.is_relative_to(ROOT) else source
    return f"""# {title}

Source: {source_label}
Export target: Notion
Export format: Markdown

---

{markdown}
"""


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def publish_kindle(args: argparse.Namespace) -> int:
    source = resolve_repo_path(args.source)
    if source.suffix.lower() == ".md":
        markdown = source.read_text(encoding="utf-8")
        title = title_from_markdown(markdown, source.stem)
        attachment = KINDLE_OUTPUT_DIR / f"{source.stem}.html"
        if args.force_export or not attachment.exists():
            attachment.write_text(markdown_to_simple_html(markdown, title), encoding="utf-8")
    else:
        title = source.stem
        attachment = source

    try:
        send_to_kindle(
            smtp_host=require_env("KINDLE_SMTP_HOST"),
            smtp_port=int(os.environ.get("KINDLE_SMTP_PORT", "587")),
            smtp_username=require_env("KINDLE_SMTP_USERNAME"),
            smtp_password=require_env("KINDLE_SMTP_PASSWORD"),
            sender_email=os.environ.get("KINDLE_FROM_EMAIL") or require_env("KINDLE_SMTP_USERNAME"),
            kindle_email=require_env("KINDLE_TO_EMAIL"),
            attachment_path=attachment,
            subject=args.subject or title,
        )
    except Exception as exc:
        print(f"Kindle publish failed: {exc}", file=sys.stderr)
        return 1
    print(f"Sent to Kindle: {attachment}")
    return 0


def publish_notion(args: argparse.Namespace) -> int:
    source = resolve_repo_path(args.source)
    markdown = source.read_text(encoding="utf-8")
    title = args.title or title_from_markdown(markdown, source.stem)
    if args.use_export and source.parent != NOTION_OUTPUT_DIR:
        export_path = NOTION_OUTPUT_DIR / f"{source.stem}.md"
        export_path.write_text(notion_export_content(source, markdown), encoding="utf-8")
        source = export_path
        markdown = source.read_text(encoding="utf-8")
    parent_page_id = args.page_id or os.environ.get("NOTION_PAGE_ID")
    parent_database_id = args.database_id or os.environ.get("NOTION_DATABASE_ID")
    try:
        result = create_notion_page(
            token=require_env("NOTION_API_KEY"),
            title=title,
            markdown=markdown,
            parent_page_id=parent_page_id,
            parent_database_id=parent_database_id,
        )
    except Exception as exc:
        print(f"Notion publish failed: {exc}", file=sys.stderr)
        return 1
    print(f"Created Notion page: {result.page_id}")
    if result.url:
        print(result.url)
    return 0


def validate_evidence(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if not path.is_absolute():
        path = ROOT / path

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1

    errors = validate_evidence_data(data)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Evidence note looks valid: {path}")
    return 0


def validate_product_profile(args: argparse.Namespace) -> int:
    path = resolve_repo_path(args.path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("Product profile must be a JSON object", file=sys.stderr)
        return 1
    errors = validate_product_profile_data(data)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Product profile looks valid: {path}")
    return 0


def create_evidence(args: argparse.Namespace) -> int:
    evidence_date = today_string(args.accessed_date)
    evidence_id = args.id or f"evidence-{evidence_date}-{slugify(args.publisher)}-{slugify(args.claim[:48])}"
    data = {
        "id": evidence_id,
        "source_url": args.source_url,
        "retrieval_method": args.retrieval_method,
        "source_title": args.source_title,
        "publisher": args.publisher,
        "published_date": args.published_date or "",
        "accessed_date": evidence_date,
        "claim": args.claim,
        "claim_type": args.claim_type,
        "confidence": args.confidence,
        "counterevidence": args.counterevidence or "",
        "research_implication": args.research_implication,
    }
    path = EVIDENCE_INDEX_DIR / f"{evidence_id}.json"
    return write_if_allowed(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", args.force)


def fetch_url_command(args: argparse.Namespace) -> int:
    try:
        result = fetch_url(args.url, timeout_seconds=args.timeout)
    except Exception as exc:
        print(f"Fetch failed: {exc}", file=sys.stderr)
        return 1
    fetch_date = today_string(args.date)
    slug = slugify(args.slug or result.url)
    suffix = ".html" if "html" in result.content_type else ".txt"
    path = RAW_DATA_DIR / f"{fetch_date}-{slug}{suffix}"
    header = (
        f"URL: {result.url}\n"
        f"Status: {result.status}\n"
        f"Content-Type: {result.content_type}\n"
        f"Fetched-Date: {fetch_date}\n\n"
    )
    return write_if_allowed(path, header + result.text, args.force)


def show_connectors(_: argparse.Namespace) -> int:
    connectors = json.loads(CONNECTOR_CONFIG_PATH.read_text(encoding="utf-8"))
    for connector in connectors:
        api_key = connector["requires_api_key"]
        env_var = connector.get("env_var") or "none"
        claims = ", ".join(connector.get("supports_claims", []))
        print(f"{connector['id']}: {connector['name']}")
        print(f"  source_type: {connector['source_type']}")
        print(f"  requires_api_key: {api_key}")
        print(f"  env_var: {env_var}")
        print(f"  cost_risk: {connector['cost_risk']}")
        print(f"  supports: {claims}")
        print()
    return 0


def show_hypotheses(_: argparse.Namespace) -> int:
    hypotheses = load_json(HYPOTHESIS_REGISTRY_PATH)
    assert isinstance(hypotheses, list)
    for item in hypotheses:
        print(f"{item['id']}: {item['statement']}")
        print(f"  status: {item['status']}")
        print(f"  confidence: {item['confidence']}")
        print(f"  supporting: {len(item['supporting_evidence_ids'])}")
        print(f"  weakening: {len(item['weakening_evidence_ids'])}")
        print(f"  contradicting: {len(item['contradicting_evidence_ids'])}")
        print()
    return 0


def iter_evidence_notes() -> list[tuple[Path, dict]]:
    notes: list[tuple[Path, dict]] = []
    if not EVIDENCE_INDEX_DIR.exists():
        return notes
    for path in sorted(EVIDENCE_INDEX_DIR.glob("*.json")):
        try:
            data = load_json(path)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            notes.append((path, data))
    return notes


def stale_evidence(as_of: date) -> list[tuple[Path, dict, int, int]]:
    stale: list[tuple[Path, dict, int, int]] = []
    for path, data in iter_evidence_notes():
        claim_type = str(data.get("claim_type", ""))
        max_age = MAX_AGE_DAYS_BY_CLAIM_TYPE.get(claim_type, 30)
        accessed = data.get("accessed_date")
        if not isinstance(accessed, str):
            continue
        try:
            age = (as_of - parse_iso_date(accessed)).days
        except ValueError:
            continue
        if age > max_age:
            stale.append((path, data, age, max_age))
    return stale


def audit_freshness(args: argparse.Namespace) -> int:
    audit_date = parse_iso_date(today_string(args.date))
    stale = stale_evidence(audit_date)
    lines = [
        f"# Freshness Audit: {audit_date.isoformat()}",
        "",
        "## Summary",
        "",
        f"Stale evidence notes: {len(stale)}",
        "",
        "## Stale Evidence",
        "",
        "| Evidence ID | Claim Type | Accessed Date | Age | Max Age | File |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for path, data, age, max_age in stale:
        lines.append(
            f"| {data.get('id', path.stem)} | {data.get('claim_type', '')} | "
            f"{data.get('accessed_date', '')} | {age} | {max_age} | {path.relative_to(ROOT)} |"
        )
    lines.extend(["", "## Required Refresh Actions", "", "- TODO" if stale else "- None"])
    output = FRESHNESS_AUDIT_DIR / f"{audit_date.isoformat()}.md"
    return write_if_allowed(output, "\n".join(lines) + "\n", args.force)


def new_falsification_audit(args: argparse.Namespace) -> int:
    audit_date = today_string(args.date)
    hypotheses = load_json(HYPOTHESIS_REGISTRY_PATH)
    assert isinstance(hypotheses, list)
    rows = [
        "| Hypothesis | Direction | Evidence | Reasoning | Follow-Up |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in hypotheses:
        rows.append(f"| {item['id']} | ambiguous |  |  |  |")
    content = f"""# Falsification Audit: {audit_date}

## Summary

TODO

## Hypothesis Checks

{chr(10).join(rows)}

## Contradictions

- TODO

## Confidence Changes

- TODO

## Required Thesis Updates

- TODO
"""
    return write_if_allowed(FALSIFICATION_AUDIT_DIR / f"{audit_date}.md", content, args.force)


def show_case_coverage(_: argparse.Namespace) -> int:
    backlog = load_json(CASE_BACKLOG_PATH)
    assert isinstance(backlog, list)
    owner_counts: dict[str, int] = {}
    bias_counts: dict[str, int] = {}
    for item in backlog:
        owner_counts[item["owner_type"]] = owner_counts.get(item["owner_type"], 0) + 1
        bias_counts[item["bias_role"]] = bias_counts.get(item["bias_role"], 0) + 1

    print("Owner type coverage:")
    for key, value in sorted(owner_counts.items()):
        print(f"  {key}: {value}")
    print()
    print("Bias-control role coverage:")
    for key, value in sorted(bias_counts.items()):
        print(f"  {key}: {value}")
    print()
    print("Candidates:")
    for item in backlog:
        print(f"  - {item['product']} ({item['owner_type']}): {item['reason_to_study']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aitoc-research",
        description="Maintain the AI-to-C business model research repository.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Print the evolving master research plan.")
    plan.set_defaults(func=show_plan)

    new_case_parser = subparsers.add_parser("new-case", help="Create a new case-study stub.")
    new_case_parser.add_argument("product_name")
    new_case_parser.add_argument("--force", action="store_true")
    new_case_parser.set_defaults(func=new_case)

    daily = subparsers.add_parser("daily-run", help="Create a dated daily trend-run note.")
    daily.add_argument("--date", help="Run date in YYYY-MM-DD format.")
    daily.add_argument("--force", action="store_true")
    daily.set_defaults(func=new_daily_run)

    weekly = subparsers.add_parser("weekly-run", help="Create a dated weekly trend-review note.")
    weekly.add_argument("--date", help="Run date in YYYY-MM-DD format.")
    weekly.add_argument("--force", action="store_true")
    weekly.set_defaults(func=new_weekly_run)

    signal = subparsers.add_parser("new-signal", help="Create a trend-signal note.")
    signal.add_argument("title")
    signal.add_argument("--date", help="Signal date in YYYY-MM-DD format.")
    signal.add_argument("--score", type=int, default=1, choices=range(1, 6))
    signal.add_argument("--force", action="store_true")
    signal.set_defaults(func=new_trend_signal)

    idea = subparsers.add_parser("new-idea", help="Create a research-idea note.")
    idea.add_argument("title")
    idea.add_argument("--date", help="Idea date in YYYY-MM-DD format.")
    idea.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    idea.add_argument("--force", action="store_true")
    idea.set_defaults(func=new_research_idea)

    memo = subparsers.add_parser("new-memo", help="Create a canonical source memo.")
    memo.add_argument("title")
    memo.add_argument("--date", help="Memo date in YYYY-MM-DD format.")
    memo.add_argument("--force", action="store_true")
    memo.set_defaults(func=new_memo)

    kindle = subparsers.add_parser("export-kindle", help="Export a source memo to Kindle-friendly HTML.")
    kindle.add_argument("source")
    kindle.add_argument("--force", action="store_true")
    kindle.set_defaults(func=export_kindle)

    notion = subparsers.add_parser("export-notion", help="Export a source memo to Notion-ready Markdown.")
    notion.add_argument("source")
    notion.add_argument("--force", action="store_true")
    notion.set_defaults(func=export_notion)

    publish_to_kindle = subparsers.add_parser("publish-kindle", help="Email a memo/export to your Kindle address.")
    publish_to_kindle.add_argument("source")
    publish_to_kindle.add_argument("--subject")
    publish_to_kindle.add_argument("--force-export", action="store_true")
    publish_to_kindle.set_defaults(func=publish_kindle)

    publish_to_notion = subparsers.add_parser("publish-notion", help="Create a Notion page from a source memo.")
    publish_to_notion.add_argument("source")
    publish_to_notion.add_argument("--title")
    publish_to_notion.add_argument("--page-id", help="Notion parent page ID. Overrides NOTION_PAGE_ID.")
    publish_to_notion.add_argument("--database-id", help="Notion parent database/data-source ID. Overrides NOTION_DATABASE_ID.")
    publish_to_notion.add_argument("--use-export", action="store_true", help="Publish the Notion export artifact instead of raw source Markdown.")
    publish_to_notion.set_defaults(func=publish_notion)

    connectors = subparsers.add_parser("connectors", help="Show configured source connectors and API dependencies.")
    connectors.set_defaults(func=show_connectors)

    hypotheses = subparsers.add_parser("hypotheses", help="Show active hypotheses and evidence counts.")
    hypotheses.set_defaults(func=show_hypotheses)

    freshness = subparsers.add_parser("audit-freshness", help="Create a freshness audit for evidence notes.")
    freshness.add_argument("--date", help="Audit date in YYYY-MM-DD format.")
    freshness.add_argument("--force", action="store_true")
    freshness.set_defaults(func=audit_freshness)

    falsification = subparsers.add_parser("audit-falsification", help="Create a falsification audit skeleton.")
    falsification.add_argument("--date", help="Audit date in YYYY-MM-DD format.")
    falsification.add_argument("--force", action="store_true")
    falsification.set_defaults(func=new_falsification_audit)

    coverage = subparsers.add_parser("case-coverage", help="Show case backlog coverage and bias-control roles.")
    coverage.set_defaults(func=show_case_coverage)

    evidence = subparsers.add_parser("validate-evidence", help="Validate an evidence note.")
    evidence.add_argument("path")
    evidence.set_defaults(func=validate_evidence)

    profile = subparsers.add_parser("validate-profile", help="Validate a product profile.")
    profile.add_argument("path")
    profile.set_defaults(func=validate_product_profile)

    create_evidence_parser = subparsers.add_parser("create-evidence", help="Create a structured evidence note from a sourced claim.")
    create_evidence_parser.add_argument("--id")
    create_evidence_parser.add_argument("--source-url", required=True)
    create_evidence_parser.add_argument("--retrieval-method", required=True, choices=sorted(VALID_RETRIEVAL_METHODS))
    create_evidence_parser.add_argument("--source-title", required=True)
    create_evidence_parser.add_argument("--publisher", required=True)
    create_evidence_parser.add_argument("--published-date")
    create_evidence_parser.add_argument("--accessed-date")
    create_evidence_parser.add_argument("--claim", required=True)
    create_evidence_parser.add_argument("--claim-type", required=True, choices=sorted(VALID_CLAIM_TYPES))
    create_evidence_parser.add_argument("--confidence", required=True, choices=sorted(VALID_CONFIDENCE))
    create_evidence_parser.add_argument("--counterevidence")
    create_evidence_parser.add_argument("--research-implication", required=True)
    create_evidence_parser.add_argument("--force", action="store_true")
    create_evidence_parser.set_defaults(func=create_evidence)

    fetch = subparsers.add_parser("fetch-url", help="Fetch a public URL into data/raw using the local web connector.")
    fetch.add_argument("url")
    fetch.add_argument("--date", help="Fetch date in YYYY-MM-DD format.")
    fetch.add_argument("--slug", help="Output filename slug.")
    fetch.add_argument("--timeout", type=int, default=20)
    fetch.add_argument("--force", action="store_true")
    fetch.set_defaults(func=fetch_url_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
