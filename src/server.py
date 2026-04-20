from __future__ import annotations

from dataclasses import dataclass, field

from .protocol import SPEC_VERSION, ServerState, verify_request
from .quantum_sim import QuantumSimulator


@dataclass
class QDelegateServer:
    shared_secret: bytes
    state: ServerState = field(default_factory=ServerState)

    def submit_job(self, request: dict) -> dict:
        for key in ("spec_version", "job_id", "nonce", "payload", "auth_tag"):
            if key not in request:
                return {"ok": False, "error": f"missing_{key}"}

        if request["spec_version"] != SPEC_VERSION:
            return {"ok": False, "error": "unsupported_version"}

        job_id = request["job_id"]
        nonce = request["nonce"]
        if job_id in self.state.seen_job_ids:
            return {"ok": False, "error": "duplicate_job_id"}
        if nonce in self.state.seen_nonces:
            return {"ok": False, "error": "reused_nonce"}

        signed_payload = {
            "spec_version": request["spec_version"],
            "job_id": job_id,
            "nonce": nonce,
            "payload": request["payload"],
        }
        if not verify_request(self.shared_secret, signed_payload, request["auth_tag"]):
            return {"ok": False, "error": "bad_auth_tag"}

        try:
            circuit = request["payload"]
            sim = QuantumSimulator(circuit["n_qubits"])
            probs = sim.run(circuit["gates"])
        except Exception as exc:  # runtime safety boundary
            return {"ok": False, "error": f"bad_payload:{exc}"}

        self.state.seen_job_ids.add(job_id)
        self.state.seen_nonces.add(nonce)
        return {
            "ok": True,
            "job_id": job_id,
            "result": {
                "probabilities": probs,
            },
        }
