"""Swappable mouth client. Key from gitignored .env, never from source."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_env(path: Path = ENV_PATH) -> dict[str, str]:
    out: dict[str, str] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("HADES_MOUTH_API_URL", "HADES_MOUTH_API_KEY", "HADES_MOUTH_MODEL"):
        if os.environ.get(k):
            out[k] = os.environ[k]
    return out


def mouth_config() -> dict[str, str]:
    env = load_env()
    url = env.get("HADES_MOUTH_API_URL") or ""
    key = env.get("HADES_MOUTH_API_KEY") or ""
    model = env.get("HADES_MOUTH_MODEL") or ""
    if not url or not key or not model:
        raise RuntimeError("mouth env missing; copy .env.example to .env")
    return {"url": url.rstrip("/"), "key": key, "model": model}


def complete(messages: list[dict], timeout: int = 60) -> str:
    cfg = mouth_config()
    endpoint = cfg["url"] + "/chat/completions"
    body = json.dumps(
        {
            "model": cfg["model"],
            "messages": messages,
            "temperature": 0.7,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg['key']}",
            "User-Agent": "hades-product-mouth/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"mouth HTTP {exc.code}") from None
    choices = payload.get("choices") or []
    if not choices:
        raise RuntimeError("mouth empty")
    content = (choices[0].get("message") or {}).get("content") or ""
    return content
