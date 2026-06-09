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


if __name__ == "__main__":
    unittest.main()
