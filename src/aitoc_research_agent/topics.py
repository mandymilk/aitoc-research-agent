"""Topic interests layer.

Turns the research scope from a single hardcoded AI-to-C thesis into a
selectable, user-defined "topic interest". Each topic owns its own plan,
hypotheses, evidence, runs, signals, and audits.

Design (per repo decision record 0002):
- The current AI-to-C content is the first topic, ``aitoc``. It uses the
  legacy repository layout (root ``data/``, ``trend_radar/``, ``audits/``,
  ``docs/`` paths) so existing files and tests keep working unchanged.
- New topics are self-contained under ``topics/<slug>/`` so they never
  collide with each other or with ``aitoc``.

This module has no dependency on ``cli`` to avoid a circular import; ``cli``
imports the default constants and helpers from here.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TOPICS_DIR = ROOT / "topics"
REGISTRY_PATH = TOPICS_DIR / "registry.json"
ACTIVE_TOPIC_PATH = TOPICS_DIR / "active_topic"
ACTIVE_TOPIC_ENV = "AITOC_TOPIC"
DEFAULT_TOPIC_SLUG = "aitoc"

# Default claim vocabulary and freshness windows. Topics may extend the claim
# vocabulary and override freshness windows, but these remain the base set.
DEFAULT_CLAIM_TYPES = {
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

DEFAULT_FRESHNESS_BY_CLAIM_TYPE = {
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

DEFAULT_FRESHNESS_FALLBACK_DAYS = 30


class TopicError(Exception):
    """Raised for unknown topics or malformed topic registries."""


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "topic"


@dataclass
class TopicContext:
    """Resolved, topic-scoped paths and claim configuration."""

    slug: str
    title: str
    layout: str
    plan_path: Path
    hypotheses_path: Path
    evidence_index_dir: Path
    product_profile_dir: Path
    daily_run_dir: Path
    weekly_run_dir: Path
    signal_dir: Path
    research_idea_dir: Path
    source_report_dir: Path
    raw_dir: Path
    case_dir: Path
    freshness_dir: Path
    falsification_dir: Path
    publish_log_dir: Path
    claim_types: set[str] = field(default_factory=set)
    freshness_by_claim_type: dict[str, int] = field(default_factory=dict)

    def max_age_for(self, claim_type: str) -> int:
        return self.freshness_by_claim_type.get(claim_type, DEFAULT_FRESHNESS_FALLBACK_DAYS)


def load_registry() -> list[dict]:
    if not REGISTRY_PATH.exists():
        return [_default_aitoc_entry()]
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TopicError(f"Topic registry must be a JSON array: {REGISTRY_PATH}")
    return data


def find_topic(slug: str, registry: list[dict] | None = None) -> dict:
    registry = registry if registry is not None else load_registry()
    for entry in registry:
        if entry.get("id") == slug:
            return entry
    raise TopicError(
        f"Unknown topic: {slug!r}. Known topics: "
        f"{', '.join(sorted(e.get('id', '?') for e in registry))}"
    )


def resolve_active_slug(cli_topic: str | None = None, env: dict | None = None) -> str:
    import os

    env = env if env is not None else os.environ
    if cli_topic:
        return cli_topic
    env_value = env.get(ACTIVE_TOPIC_ENV)
    if env_value:
        return env_value.strip()
    if ACTIVE_TOPIC_PATH.exists():
        pointer = ACTIVE_TOPIC_PATH.read_text(encoding="utf-8").strip()
        if pointer:
            return pointer
    return DEFAULT_TOPIC_SLUG


def set_active_slug(slug: str) -> None:
    find_topic(slug)  # validates existence
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVE_TOPIC_PATH.write_text(slug + "\n", encoding="utf-8")


def topic_context(slug: str, registry: list[dict] | None = None) -> TopicContext:
    entry = find_topic(slug, registry)
    layout = entry.get("layout", "scoped")

    claim_types = set(DEFAULT_CLAIM_TYPES) | set(entry.get("claim_types", []) or [])
    freshness = dict(DEFAULT_FRESHNESS_BY_CLAIM_TYPE)
    freshness.update(entry.get("freshness_overrides", {}) or {})

    if layout == "legacy":
        return TopicContext(
            slug=slug,
            title=entry.get("title", slug),
            layout=layout,
            plan_path=ROOT / "docs" / "research_plan.md",
            hypotheses_path=ROOT / "hypotheses" / "registry.json",
            evidence_index_dir=ROOT / "data" / "evidence_index",
            product_profile_dir=ROOT / "data" / "product_profiles",
            daily_run_dir=ROOT / "trend_radar" / "runs" / "daily",
            weekly_run_dir=ROOT / "trend_radar" / "runs" / "weekly",
            signal_dir=ROOT / "trend_radar" / "signals",
            research_idea_dir=ROOT / "trend_radar" / "research_ideas",
            source_report_dir=ROOT / "reports" / "source",
            raw_dir=ROOT / "data" / "raw",
            case_dir=ROOT / "docs" / "case_studies",
            freshness_dir=ROOT / "audits" / "freshness",
            falsification_dir=ROOT / "audits" / "falsification",
            publish_log_dir=ROOT / "outputs" / "publish_log",
            claim_types=claim_types,
            freshness_by_claim_type=freshness,
        )

    base = TOPICS_DIR / slug
    return TopicContext(
        slug=slug,
        title=entry.get("title", slug),
        layout=layout,
        plan_path=base / "research_plan.md",
        hypotheses_path=base / "hypotheses.json",
        evidence_index_dir=base / "evidence_index",
        product_profile_dir=base / "product_profiles",
        daily_run_dir=base / "runs" / "daily",
        weekly_run_dir=base / "runs" / "weekly",
        signal_dir=base / "signals",
        research_idea_dir=base / "research_ideas",
        source_report_dir=base / "reports" / "source",
        raw_dir=base / "raw",
        case_dir=base / "case_studies",
        freshness_dir=base / "audits" / "freshness",
        falsification_dir=base / "audits" / "falsification",
        publish_log_dir=base / "publish_log",
        claim_types=claim_types,
        freshness_by_claim_type=freshness,
    )


def _default_aitoc_entry() -> dict:
    return {
        "id": DEFAULT_TOPIC_SLUG,
        "title": "AI-to-Consumer business models",
        "status": "active",
        "layout": "legacy",
        "main_question": (
            "Can AI-to-C products become durable standalone businesses, or do they "
            "need large-company subsidy, bundled distribution, or non-consumer "
            "revenue to survive?"
        ),
        "claim_types": [],
        "freshness_overrides": {},
        "hypothesis_ids": ["H1", "H2", "H3", "H4", "H5"],
    }
