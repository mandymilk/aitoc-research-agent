from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-09"
SLUG = "2026-06-09-live-e2e-ai-to-c-pricing-smoke-test"
SOURCE = ROOT / "reports" / "source" / f"{SLUG}.md"
KINDLE = ROOT / "outputs" / "kindle" / f"{SLUG}.html"
NOTION = ROOT / "outputs" / "notion" / f"{SLUG}.md"
FETCH_MANIFEST = ROOT / "data" / "raw" / f"{TODAY}-e2e-fetch-manifest.md"
SOURCE_URLS = [
    (
        "openai-chatgpt-plus",
        "https://help.openai.com/en/articles/6950777-what%20-is-chatgpt-plus",
    ),
    (
        "openai-chatgpt-go",
        "https://openai.com/index/introducing-chatgpt-go/",
    ),
    (
        "microsoft-copilot-support",
        "https://support.microsoft.com/en-US/Microsoft-365-Copilot/what-s-the-difference-between-microsoft-copilot-free-and-copilot-in-microsoft-365",
    ),
    (
        "microsoft-copilot-pricing",
        "https://www.microsoft.com/en-us/microsoft-365-copilot/pricing",
    ),
]


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    return subprocess.run([sys.executable, "-m", "aitoc_research_agent", *args], cwd=ROOT, env=env, check=check)


def write_source() -> None:
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    SOURCE.write_text(
        f"""# Live E2E AI-to-C Pricing Smoke Test

Date: {TODAY}
Version: v0.1
Status: smoke-test
Output targets: Kindle, Notion
Tags: ai-to-c, pricing, smoke-test

## Executive Summary

This is a live end-to-end delivery test for the AI-to-C research agent. It uses current, source-backed observations gathered on {TODAY}, then exports and publishes the result to Kindle and Notion.

The test observation is narrow: consumer AI pricing is visibly tiered across current official OpenAI materials, while Microsoft Copilot is positioned through Microsoft 365 subscription and business packaging. This is not a full research conclusion.

## Key Claims

- OpenAI Help says ChatGPT Plus is $20/month and may include usage limits such as message caps during high demand.
  Evidence: OpenAI Help Center, accessed {TODAY}.
  Confidence: high.

- OpenAI's January 16, 2026 announcement says ChatGPT Go is available globally, with US pricing at $8/month, Plus at $20/month, and Pro at $200/month; it also says OpenAI plans to test ads in the free tier and ChatGPT Go in the US.
  Evidence: OpenAI announcement, accessed {TODAY}.
  Confidence: high.

- Microsoft pricing and support pages distinguish free, individual, and business Copilot experiences and connect Copilot to Microsoft 365 packaging.
  Evidence: Microsoft official pages, accessed {TODAY}.
  Confidence: high.

## Research Implication

Today's smoke test supports the agent workflow rather than a market conclusion. It shows the pipeline can take current source-backed claims, create a readable memo, export Kindle/Notion artifacts, and attempt live delivery.

## Sources And Evidence

- OpenAI Help Center: https://help.openai.com/en/articles/6950777-what%20-is-chatgpt-plus
- OpenAI announcement: https://openai.com/index/introducing-chatgpt-go/
- Microsoft Copilot support: https://support.microsoft.com/en-US/Microsoft-365-Copilot/what-s-the-difference-between-microsoft-copilot-free-and-copilot-in-microsoft-365
- Microsoft Copilot pricing: https://www.microsoft.com/en-us/microsoft-365-copilot/pricing
""",
        encoding="utf-8",
    )
    print(SOURCE)


def fetch_live_sources() -> None:
    FETCH_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    manifest_lines = [f"# E2E Fetch Manifest: {TODAY}", ""]
    failures: list[str] = []
    for slug, url in SOURCE_URLS:
        result = run(["fetch-url", url, "--date", TODAY, "--slug", f"e2e-{slug}", "--force"], check=False)
        status = "ok" if result.returncode == 0 else "failed"
        manifest_lines.append(f"- {status}: {slug} {url}")
        if result.returncode != 0:
            failures.append(slug)
    missing = [
        slug
        for slug, _ in SOURCE_URLS
        if not list((ROOT / "data" / "raw").glob(f"{TODAY}-e2e-{slug}.*"))
    ]
    if missing:
        manifest_lines.append("")
        manifest_lines.append(f"Missing raw files: {', '.join(missing)}")
    FETCH_MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    if failures or missing:
        raise RuntimeError(
            "Live source fetch failed; not publishing because tool-grounded source collection was incomplete. "
            f"See {FETCH_MANIFEST}"
        )


def main() -> int:
    fetch_live_sources()
    write_source()
    run(["export-kindle", str(SOURCE), "--force"])
    run(["export-notion", str(SOURCE), "--force"])
    if not KINDLE.exists():
        raise RuntimeError(f"Missing Kindle export: {KINDLE}")
    if not NOTION.exists():
        raise RuntimeError(f"Missing Notion export: {NOTION}")
    notion = run(["publish-notion", str(NOTION), "--title", "Live E2E AI-to-C Pricing Smoke Test"], check=False)
    kindle = run(["publish-kindle", str(SOURCE), "--subject", "Live E2E AI-to-C Pricing Smoke Test", "--force-export"], check=False)
    if notion.returncode != 0 or kindle.returncode != 0:
        print("E2E delivery result:")
        print(f"  notion: {'ok' if notion.returncode == 0 else 'failed'}")
        print(f"  kindle: {'ok' if kindle.returncode == 0 else 'failed'}")
        return 1
    print("E2E delivery result: notion ok, kindle ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
