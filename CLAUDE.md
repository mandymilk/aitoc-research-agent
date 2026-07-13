# CLAUDE.md — Claude Code Entry Point

This project's full operating guide lives in `AGENTS.md`. Read it first.

@AGENTS.md

## Claude Code Specifics

- Use the **`WebSearch`** tool for discovery (finding candidate AI-to-C pricing,
  usage, retention, distribution, and monetization sources).
- Use the **`WebFetch`** tool to open each candidate URL and read the exact
  claim and its published date before recording it.
- These built-in tools are the evidence-retrieval layer. **No paid search API is
  required** — do not depend on `WEB_SEARCH_API_KEY` or similar.
- After verifying a claim on a page you actually opened, record it with
  `create-evidence` using `--retrieval-method search` (from `WebSearch`) or
  `--retrieval-method browser` (from a direct `WebFetch` of a known URL).
- Never cite Claude's own prior knowledge as evidence for a current market fact.
  If a page cannot be fetched, mark the claim `unknown`.
