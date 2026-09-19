"""Signed GET URLs. Secrets stay in env; client only gets the URL."""

from __future__ import annotations

import hashlib
import hmac
import os
from datetime import datetime, timezone
from urllib.parse import quote


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def signed_get_url(
    object_key: str,
    *,
    endpoint: str,
    bucket: str,
    access_key: str,
    secret_key: str,
    expires: int = 300,
) -> str:
    host = endpoint.replace("https://", "").replace("http://", "").rstrip("/")
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = now.strftime("%Y%m%d")
    region = "auto"
    service = "s3"
    credential = f"{access_key}/{datestamp}/{region}/{service}/aws4_request"
    canonical_uri = f"/{bucket}/{quote(object_key, safe='/')}"
    qs = (
        f"X-Amz-Algorithm=AWS4-HMAC-SHA256"
        f"&X-Amz-Credential={quote(credential, safe='')}"
        f"&X-Amz-Date={amz_date}"
        f"&X-Amz-Expires={expires}"
        f"&X-Amz-SignedHeaders=host"
    )
    canonical = f"GET\n{canonical_uri}\n{qs}\nhost:{host}\n\nhost\nUNSIGNED-PAYLOAD"
    scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = (
        f"AWS4-HMAC-SHA256\n{amz_date}\n{scope}\n"
        f"{hashlib.sha256(canonical.encode()).hexdigest()}"
    )
    signing_key = _sign(
        _sign(_sign(_sign(f"AWS4{secret_key}".encode(), datestamp), region), service),
        "aws4_request",
    )
    sig = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()
    url = f"https://{host}{canonical_uri}?{qs}&X-Amz-Signature={sig}"
    if secret_key in url or access_key in url.split("X-Amz-Credential=")[0]:
        raise RuntimeError("secret leaked into URL host")
    if secret_key in url:
        raise RuntimeError("secret leaked into URL")
    return url


def signed_get_url_from_env(object_key: str) -> str:
    return signed_get_url(
        object_key,
        endpoint=os.environ.get("CLOUDFLARE_R2_ENDPOINT") or "",
        bucket=os.environ.get("CLOUDFLARE_R2_BUCKET") or "",
        access_key=os.environ.get("CLOUDFLARE_R2_ACCESS_KEY_ID") or "",
        secret_key=os.environ.get("CLOUDFLARE_R2_SECRET_ACCESS_KEY") or "",
    )
