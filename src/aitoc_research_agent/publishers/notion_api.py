from __future__ import annotations

import json
import re
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.request import Request, urlopen


NOTION_VERSION = "2026-03-11"
NOTION_API_BASE = "https://api.notion.com/v1"


@dataclass(frozen=True)
class NotionPageResult:
    page_id: str
    url: str


def notion_request(token: str, method: str, path: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        f"{NOTION_API_BASE}{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API error {exc.code}: {detail}") from exc


def create_notion_page(
    *,
    token: str,
    title: str,
    markdown: str,
    parent_page_id: str | None = None,
    parent_database_id: str | None = None,
) -> NotionPageResult:
    if bool(parent_page_id) == bool(parent_database_id):
        raise ValueError("Provide exactly one Notion parent: page_id or database_id")

    if parent_page_id:
        parent = {"type": "page_id", "page_id": parent_page_id}
        properties = {"title": {"title": [{"text": {"content": title[:2000]}}]}}
    else:
        parent = {"type": "database_id", "database_id": parent_database_id}
        properties = {"Name": {"title": [{"text": {"content": title[:2000]}}]}}

    page = notion_request(
        token,
        "POST",
        "/pages",
        {"parent": parent, "properties": properties},
    )
    page_id = page["id"]
    blocks = markdown_to_notion_blocks(markdown)
    for chunk in chunked(blocks, 100):
        notion_request(token, "PATCH", f"/blocks/{page_id}/children", {"children": chunk})
    return NotionPageResult(page_id=page_id, url=page.get("url", ""))


def chunked(items: list[dict], size: int) -> list[list[dict]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def markdown_to_notion_blocks(markdown: str) -> list[dict]:
    blocks: list[dict] = []
    in_code = False
    code_lines: list[str] = []
    code_language = "plain text"
    table_rows: list[list[str]] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            flush_table(blocks, table_rows)
            if in_code:
                blocks.append(code_block("\n".join(code_lines), code_language))
                code_lines = []
                code_language = "plain text"
                in_code = False
            else:
                code_language = line[3:].strip() or "plain text"
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if is_table_line(line):
            cells = parse_table_cells(line)
            if not is_table_separator(cells):
                table_rows.append(cells)
            continue
        flush_table(blocks, table_rows)
        if not line:
            continue
        if line.startswith("# "):
            blocks.append(text_block("heading_1", line[2:].strip()))
        elif line.startswith("## "):
            blocks.append(text_block("heading_2", line[3:].strip()))
        elif line.startswith("### "):
            blocks.append(text_block("heading_3", line[4:].strip()))
        elif line.startswith("- [ ] "):
            blocks.append(to_do_block(line[6:].strip(), checked=False))
        elif line.startswith("- [x] ") or line.startswith("- [X] "):
            blocks.append(to_do_block(line[6:].strip(), checked=True))
        elif line.startswith("- "):
            blocks.append(text_block("bulleted_list_item", line[2:].strip()))
        elif re.match(r"^\d+\. ", line):
            blocks.append(text_block("numbered_list_item", re.sub(r"^\d+\. ", "", line).strip()))
        elif line.startswith("> "):
            blocks.append(text_block("quote", line[2:].strip()))
        else:
            blocks.append(text_block("paragraph", line))

    if in_code:
        blocks.append(code_block("\n".join(code_lines), code_language))
    flush_table(blocks, table_rows)
    return blocks or [text_block("paragraph", "")]


def text_block(block_type: str, text: str) -> dict:
    return {
        "object": "block",
        "type": block_type,
        block_type: {"rich_text": markdown_inline_to_rich_text(text)},
    }


def to_do_block(text: str, checked: bool) -> dict:
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": markdown_inline_to_rich_text(text),
            "checked": checked,
        },
    }


def code_block(text: str, language: str) -> dict:
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
            "language": language,
        },
    }


def markdown_inline_to_rich_text(text: str) -> list[dict]:
    chunks: list[dict] = []
    pattern = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")
    position = 0
    for match in pattern.finditer(text):
        if match.start() > position:
            chunks.append(rich_text(text[position : match.start()]))
        token = match.group(0)
        if token.startswith("**") and token.endswith("**"):
            chunks.append(rich_text(token[2:-2], bold=True))
        elif token.startswith("`") and token.endswith("`"):
            chunks.append(rich_text(token[1:-1], code=True))
        else:
            link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token)
            if link_match:
                chunks.append(rich_text(link_match.group(1), href=link_match.group(2)))
            else:
                chunks.append(rich_text(token))
        position = match.end()
    if position < len(text):
        chunks.append(rich_text(text[position:]))
    return chunks or [rich_text("")]


def rich_text(text: str, *, bold: bool = False, code: bool = False, href: str | None = None) -> dict:
    item = {
        "type": "text",
        "text": {"content": text[:2000]},
        "annotations": {
            "bold": bold,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": code,
            "color": "default",
        },
    }
    if href:
        item["text"]["link"] = {"url": href}
    return item


def is_table_line(line: str) -> bool:
    return line.startswith("|") and line.endswith("|") and line.count("|") >= 2


def parse_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip("|").split("|")]


def is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def flush_table(blocks: list[dict], table_rows: list[list[str]]) -> None:
    if not table_rows:
        return
    width = max(len(row) for row in table_rows)
    normalized = [row + [""] * (width - len(row)) for row in table_rows]
    blocks.append(
        {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": width,
                "has_column_header": len(normalized) > 1,
                "has_row_header": False,
                "children": [
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [markdown_inline_to_rich_text(cell) for cell in row]
                        },
                    }
                    for row in normalized
                ],
            },
        }
    )
    table_rows.clear()
