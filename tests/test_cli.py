import unittest

from datetime import date

from aitoc_research_agent.cli import (
    MAX_AGE_DAYS_BY_CLAIM_TYPE,
    VALID_CLAIM_TYPES,
    load_json,
    markdown_to_simple_html,
    notion_export_content,
    parse_iso_date,
    title_from_markdown,
    today_string,
    slugify,
    validate_evidence_data,
    validate_product_profile_data,
    ROOT,
)
from aitoc_research_agent import __version__
from aitoc_research_agent import topics
from aitoc_research_agent.publishers.notion_api import markdown_to_notion_blocks


class CliTests(unittest.TestCase):
    def test_slugify_product_name(self) -> None:
        self.assertEqual(slugify("Microsoft Copilot"), "microsoft-copilot")
        self.assertEqual(slugify(" Doubao / 豆包 "), "doubao")

    def test_today_string_uses_explicit_date(self) -> None:
        self.assertEqual(today_string("2026-06-09"), "2026-06-09")

    def test_title_from_markdown(self) -> None:
        self.assertEqual(title_from_markdown("# Title\n\nBody", "fallback"), "Title")

    def test_markdown_to_simple_html(self) -> None:
        html = markdown_to_simple_html("# Title\n\n- item\n\n| A | B |\n| --- | --- |\n| [x](https://example.com) | **b** |", "Title")
        compact = html.replace("\n", "")
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<li>item</li>", compact)
        self.assertIn("<table>", html)
        self.assertEqual(html.count("<table>"), 1)
        self.assertIn('<a href="https://example.com">x</a>', html)
        self.assertIn("<strong>b</strong>", html)

    def test_markdown_to_simple_html_keeps_indented_claim_detail_in_bullet(self) -> None:
        html = markdown_to_simple_html("- Claim\n  Evidence: source\n  Confidence: high", "Title")
        compact = html.replace("\n", "")
        self.assertIn("<li>Claim<br>Evidence: source<br>Confidence: high</li>", compact)

    def test_parse_iso_date(self) -> None:
        self.assertEqual(parse_iso_date("2026-06-09"), date(2026, 6, 9))

    def test_pricing_freshness_window_is_short(self) -> None:
        self.assertEqual(MAX_AGE_DAYS_BY_CLAIM_TYPE["pricing"], 7)

    def test_freshness_types_are_valid_claim_types(self) -> None:
        self.assertFalse(set(MAX_AGE_DAYS_BY_CLAIM_TYPE) - VALID_CLAIM_TYPES)

    def test_validate_evidence_rejects_bad_url_and_extra_field(self) -> None:
        data = {
            "id": "e1",
            "source_url": "not-a-url",
            "retrieval_method": "browser",
            "source_title": "Title",
            "publisher": "Publisher",
            "accessed_date": "2026-06-09",
            "claim": "Claim.",
            "claim_type": "pricing",
            "confidence": "low",
            "research_implication": "Implication.",
            "typo": "bad",
        }
        errors = validate_evidence_data(data)
        self.assertTrue(any("Invalid source_url" in error for error in errors))
        self.assertTrue(any("Unexpected fields" in error for error in errors))

    def test_seed_registries_load(self) -> None:
        hypotheses = load_json(ROOT / "hypotheses" / "registry.json")
        backlog = load_json(ROOT / "trend_radar" / "case_backlog" / "candidate_backlog.json")
        self.assertGreaterEqual(len(hypotheses), 5)
        self.assertGreaterEqual(len(backlog), 6)

    def test_version_file_matches_package(self) -> None:
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), __version__)

    def test_seed_product_profile_validates(self) -> None:
        data = load_json(ROOT / "data" / "product_profiles" / "microsoft-copilot.json")
        self.assertEqual(validate_product_profile_data(data), [])

    def test_markdown_to_notion_blocks(self) -> None:
        blocks = markdown_to_notion_blocks("# Title\n\n- item\n\n- [ ] task\n\n```text\ncode\n```")
        self.assertEqual(blocks[0]["type"], "heading_1")
        self.assertEqual(blocks[1]["type"], "bulleted_list_item")
        self.assertEqual(blocks[2]["type"], "to_do")
        self.assertEqual(blocks[3]["type"], "code")

    def test_markdown_to_notion_table_and_inline_formatting(self) -> None:
        blocks = markdown_to_notion_blocks("| Source | Link |\n| --- | --- |\n| **OpenAI** | [Help](https://help.openai.com) and `code` |")
        self.assertEqual(blocks[0]["type"], "table")
        table = blocks[0]["table"]
        self.assertEqual(table["table_width"], 2)
        self.assertEqual(table["children"][1]["table_row"]["cells"][0][0]["annotations"]["bold"], True)
        rich = table["children"][1]["table_row"]["cells"][1]
        self.assertEqual(rich[0]["text"]["link"]["url"], "https://help.openai.com")
        self.assertTrue(any(chunk["annotations"]["code"] for chunk in rich))

    def test_notion_export_content_wraps_source_metadata(self) -> None:
        source = ROOT / "reports" / "source" / "example.md"
        content = notion_export_content(source, "# Example\n\nBody")
        self.assertIn("Export target: Notion", content)
        self.assertIn("reports/source/example.md", content)
        self.assertIn("# Example", content)


class TopicLayerTests(unittest.TestCase):
    def test_seed_registry_has_aitoc_as_legacy(self) -> None:
        registry = topics.load_registry()
        aitoc = topics.find_topic("aitoc", registry)
        self.assertEqual(aitoc["layout"], "legacy")

    def test_aitoc_context_uses_legacy_root_paths(self) -> None:
        ctx = topics.topic_context("aitoc")
        self.assertEqual(ctx.evidence_index_dir, topics.ROOT / "data" / "evidence_index")
        self.assertEqual(ctx.plan_path, topics.ROOT / "docs" / "research_plan.md")
        self.assertEqual(ctx.hypotheses_path, topics.ROOT / "hypotheses" / "registry.json")

    def test_scoped_topic_context_is_self_contained(self) -> None:
        registry = [
            {"id": "evs", "title": "Electric Vehicles", "status": "active", "layout": "scoped"}
        ]
        ctx = topics.topic_context("evs", registry)
        base = topics.TOPICS_DIR / "evs"
        self.assertEqual(ctx.evidence_index_dir, base / "evidence_index")
        self.assertEqual(ctx.plan_path, base / "research_plan.md")
        self.assertEqual(ctx.daily_run_dir, base / "runs" / "daily")

    def test_topic_extends_claim_types_and_overrides_freshness(self) -> None:
        registry = [
            {
                "id": "evs",
                "title": "EVs",
                "status": "active",
                "layout": "scoped",
                "claim_types": ["battery_cost"],
                "freshness_overrides": {"pricing": 1},
            }
        ]
        ctx = topics.topic_context("evs", registry)
        self.assertIn("battery_cost", ctx.claim_types)
        self.assertIn("pricing", ctx.claim_types)
        self.assertEqual(ctx.max_age_for("pricing"), 1)
        self.assertEqual(ctx.max_age_for("battery_cost"), topics.DEFAULT_FRESHNESS_FALLBACK_DAYS)

    def test_resolve_active_slug_precedence(self) -> None:
        self.assertEqual(topics.resolve_active_slug("cli-topic", env={}), "cli-topic")
        self.assertEqual(topics.resolve_active_slug(None, env={topics.ACTIVE_TOPIC_ENV: "env-topic"}), "env-topic")

    def test_unknown_topic_raises(self) -> None:
        with self.assertRaises(topics.TopicError):
            topics.topic_context("does-not-exist", [])


class VerifyRunTests(unittest.TestCase):
    def _make_ctx(self, base):
        from pathlib import Path

        base = Path(base)
        return topics.TopicContext(
            slug="t",
            title="T",
            layout="scoped",
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
            claim_types=set(topics.DEFAULT_CLAIM_TYPES),
            freshness_by_claim_type=dict(topics.DEFAULT_FRESHNESS_BY_CLAIM_TYPE),
        )

    def _populate(self, ctx, run_date):
        import json as _json

        for directory in [
            ctx.daily_run_dir,
            ctx.evidence_index_dir,
            ctx.freshness_dir,
            ctx.falsification_dir,
            ctx.source_report_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
        (ctx.daily_run_dir / f"{run_date}.md").write_text("run", encoding="utf-8")
        (ctx.evidence_index_dir / "e1.json").write_text("{}", encoding="utf-8")
        ctx.hypotheses_path.write_text(_json.dumps([{"id": "H1"}]), encoding="utf-8")
        (ctx.freshness_dir / f"{run_date}.md").write_text("fresh", encoding="utf-8")
        (ctx.falsification_dir / f"{run_date}.md").write_text("fals", encoding="utf-8")
        (ctx.source_report_dir / f"{run_date}-memo.md").write_text("# Memo", encoding="utf-8")

    def test_complete_run_passes_when_publish_env_absent(self) -> None:
        import os
        import tempfile
        from unittest import mock

        from aitoc_research_agent.cli import verify_run_checks

        cleared = {
            "KINDLE_SMTP_HOST": "",
            "KINDLE_SMTP_USERNAME": "",
            "KINDLE_SMTP_PASSWORD": "",
            "KINDLE_TO_EMAIL": "",
            "NOTION_API_KEY": "",
        }
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, cleared, clear=False):
            ctx = self._make_ctx(tmp)
            self._populate(ctx, "2026-07-14")
            checks = verify_run_checks(ctx, "2026-07-14")
            failing = [c for c in checks if c["required"] and not c["ok"]]
            self.assertEqual(failing, [])

    def test_missing_evidence_fails(self) -> None:
        import os
        import tempfile
        from unittest import mock

        from aitoc_research_agent.cli import verify_run_checks

        cleared = {"KINDLE_SMTP_HOST": "", "NOTION_API_KEY": ""}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, cleared, clear=False):
            ctx = self._make_ctx(tmp)
            self._populate(ctx, "2026-07-14")
            for note in ctx.evidence_index_dir.glob("*.json"):
                note.unlink()
            checks = verify_run_checks(ctx, "2026-07-14")
            evidence_check = next(c for c in checks if c["name"] == "evidence")
            self.assertFalse(evidence_check["ok"])

    def test_publish_required_when_env_configured(self) -> None:
        import os
        import tempfile
        from unittest import mock

        from aitoc_research_agent.cli import verify_run_checks

        configured = {
            "KINDLE_SMTP_HOST": "smtp.example.com",
            "KINDLE_SMTP_USERNAME": "u",
            "KINDLE_SMTP_PASSWORD": "p",
            "KINDLE_TO_EMAIL": "k@example.com",
            "NOTION_API_KEY": "secret",
            "NOTION_PAGE_ID": "page",
        }
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, configured, clear=False):
            ctx = self._make_ctx(tmp)
            self._populate(ctx, "2026-07-14")
            checks = verify_run_checks(ctx, "2026-07-14")
            kindle = next(c for c in checks if c["name"] == "kindle_publish")
            notion = next(c for c in checks if c["name"] == "notion_publish")
            self.assertTrue(kindle["required"])
            self.assertFalse(kindle["ok"])
            self.assertTrue(notion["required"])
            self.assertFalse(notion["ok"])

    def test_topic_run_dates_and_latest(self) -> None:
        import tempfile

        from aitoc_research_agent.cli import latest_run_date, topic_run_dates

        with tempfile.TemporaryDirectory() as tmp:
            ctx = self._make_ctx(tmp)
            self.assertEqual(topic_run_dates(ctx), [])
            self.assertIsNone(latest_run_date(ctx))
            ctx.daily_run_dir.mkdir(parents=True, exist_ok=True)
            ctx.weekly_run_dir.mkdir(parents=True, exist_ok=True)
            (ctx.daily_run_dir / "2026-07-10.md").write_text("a", encoding="utf-8")
            (ctx.daily_run_dir / "2026-07-14.md").write_text("b", encoding="utf-8")
            (ctx.weekly_run_dir / "2026-07-12.md").write_text("c", encoding="utf-8")
            self.assertEqual(topic_run_dates(ctx), ["2026-07-10", "2026-07-12", "2026-07-14"])
            self.assertEqual(latest_run_date(ctx), "2026-07-14")


if __name__ == "__main__":
    unittest.main()
