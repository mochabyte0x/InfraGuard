"""Mythic HTTP C2 profile parser.

Parses the Mythic HTTP C2 container's config.json format into the
normalized C2Profile model. The HTTP profile uses:
  - GET  /get_uri?query_param=<message>
  - POST /post_uri  (body = message)

Reference: https://github.com/MythicC2Profiles/http
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from infraguard.profiles.models import (
    C2Profile,
    ClientConfig,
    HttpTransaction,
    MessageConfig,
    ServerConfig,
)


class MythicHTTPProfileParser:
    """Parse Mythic HTTP config.json into a normalized C2Profile."""

    def parse(self, content: str) -> C2Profile:
        data = json.loads(content)
        return self._parse_dict(data)

    def parse_file(self, path: str | Path) -> C2Profile:
        with open(path, encoding="utf-8") as f:
            return self.parse(f.read())

    def _parse_dict(self, data: dict[str, Any]) -> C2Profile:
        name = data.get("name", "Mythic HTTP Profile")

        # Support both the raw container config.json (instances[]) and a
        # single-instance flat dict for operator convenience.
        if "instances" in data:
            inst = data["instances"][0] if data["instances"] else {}
        else:
            inst = data

        get_uri = "/" + inst.get("get_uri", "index").lstrip("/")
        post_uri = "/" + inst.get("post_uri", "data").lstrip("/")
        query_param = inst.get("query_path_name", inst.get("query_param", "q"))

        req_headers: dict[str, str] = inst.get("headers", {})
        server_headers: dict[str, str] = inst.get("ServerHeaders", inst.get("server_headers", {}))

        useragent = req_headers.get("User-Agent") or req_headers.get("user-agent")

        http_get = HttpTransaction(
            verb="GET",
            uris=[get_uri],
            client=ClientConfig(
                headers=req_headers,
                message=MessageConfig(location="parameter", name=query_param),
                transforms=[],
            ),
            server=ServerConfig(headers=server_headers, transforms=[]),
        )

        http_post = HttpTransaction(
            verb="POST",
            uris=[post_uri],
            client=ClientConfig(
                headers=req_headers,
                message=MessageConfig(location="body", name=""),
                transforms=[],
            ),
            server=ServerConfig(headers=server_headers, transforms=[]),
        )

        return C2Profile(
            name=name,
            http_get=http_get,
            http_post=http_post,
            useragent=useragent,
        )


def parse_mythic_http_profile(content: str, name: str | None = None) -> C2Profile:
    """Parse a Mythic HTTP config.json string into a C2Profile."""
    parser = MythicHTTPProfileParser()
    profile = parser.parse(content)
    if name:
        profile.name = name
    return profile


def parse_mythic_http_file(path: str | Path, name: str | None = None) -> C2Profile:
    """Parse a Mythic HTTP config.json file into a C2Profile."""
    content = Path(path).read_text(encoding="utf-8")
    return parse_mythic_http_profile(content, name)
