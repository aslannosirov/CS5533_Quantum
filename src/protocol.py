"""Protocol helpers for Q-Delegate style requests."""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, field

SPEC_VERSION = "v0.5"


@dataclass
class ServerState:
    seen_job_ids: set[str] = field(default_factory=set)
    seen_nonces: set[str] = field(default_factory=set)


def sign_request(secret: bytes, payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret, canonical, hashlib.sha256).hexdigest()


def verify_request(secret: bytes, payload: dict, auth_tag: str) -> bool:
    expected = sign_request(secret, payload)
    return hmac.compare_digest(expected, auth_tag)
