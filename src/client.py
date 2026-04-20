from __future__ import annotations

from .protocol import SPEC_VERSION, sign_request


def build_request(secret: bytes, job_id: str, nonce: str, payload: dict) -> dict:
    signed_payload = {
        "spec_version": SPEC_VERSION,
        "job_id": job_id,
        "nonce": nonce,
        "payload": payload,
    }
    return {
        **signed_payload,
        "auth_tag": sign_request(secret, signed_payload),
    }
