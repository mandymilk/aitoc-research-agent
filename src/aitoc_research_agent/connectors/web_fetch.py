from __future__ import annotations

from dataclasses import dataclass
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: int
    content_type: str
    text: str


def fetch_url(url: str, timeout_seconds: int = 20) -> FetchResult:
    request = Request(url, headers={"User-Agent": "aitoc-research-agent/0.6.2"})
    with urlopen(request, timeout=timeout_seconds) as response:
        raw = response.read()
        content_type = response.headers.get("content-type", "")
        charset = response.headers.get_content_charset() or "utf-8"
        text = raw.decode(charset, errors="replace")
        return FetchResult(
            url=response.geturl(),
            status=response.status,
            content_type=content_type,
            text=text,
        )
