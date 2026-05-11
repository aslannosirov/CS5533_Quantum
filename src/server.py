from __future__ import annotations

import time
from dataclasses import dataclass, field

from .algorithms import build_algorithm
from .protocol import SPEC_VERSION, ServerState, verify_request
from .quantum_sim import QuantumSimulator

MAX_QUBITS = 12
MAX_GATES = 2000
MAX_SHOTS = 20000
MAX_AGE_SECONDS = 300


@dataclass
class QDelegateServer:
    shared_secret: bytes
    state: ServerState = field(default_factory=ServerState)

    def submit_job(self, request: dict) -> dict:
        start = time.perf_counter()
        required = ("spec_version", "job_id", "nonce", "payload", "auth_tag", "timestamp")
        for key in required:
            if key not in request:
                return {"ok": False, "error": f"missing_{key}", "code": "MISSING_FIELD"}

        if request["spec_version"] != SPEC_VERSION:
            return {"ok": False, "error": "unsupported_version", "code": "UNSUPPORTED_VERSION"}

        now = int(time.time())
        timestamp = request["timestamp"]
        if not isinstance(timestamp, int):
            return {"ok": False, "error": "bad_timestamp", "code": "BAD_TIMESTAMP"}
        if abs(now - timestamp) > MAX_AGE_SECONDS:
            return {"ok": False, "error": "stale_request", "code": "STALE_REQUEST"}

        job_id = request["job_id"]
        nonce = request["nonce"]
        if job_id in self.state.seen_job_ids:
            return {"ok": False, "error": "duplicate_job_id", "code": "DUPLICATE_JOB_ID"}
        if nonce in self.state.seen_nonces:
            return {"ok": False, "error": "reused_nonce", "code": "REUSED_NONCE"}

        signed_payload = {
            "spec_version": request["spec_version"],
            "job_id": job_id,
            "nonce": nonce,
            "payload": request["payload"],
            "timestamp": timestamp,
        }
        if not verify_request(self.shared_secret, signed_payload, request["auth_tag"]):
            return {"ok": False, "error": "bad_auth_tag", "code": "BAD_AUTH_TAG"}

        try:
            circuit_payload = self._resolve_circuit_payload(request["payload"])
            n_qubits, gates, shots = self._validate_circuit_payload(circuit_payload)
            sim = QuantumSimulator(n_qubits)
            probs = sim.run(gates)
            counts = sim.sample_counts(shots) if shots is not None else None
        except Exception as exc:
            return {"ok": False, "error": f"bad_payload:{exc}", "code": "BAD_PAYLOAD"}

        self.state.seen_job_ids.add(job_id)
        self.state.seen_nonces.add(nonce)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
        result = {
            "probabilities": probs,
            "n_qubits": n_qubits,
            "num_gates": len(gates),
        }
        if counts is not None:
            result["counts"] = counts
        return {
            "ok": True,
            "spec_version": SPEC_VERSION,
            "job_id": job_id,
            "execution_ms": elapsed_ms,
            "result": result,
        }

    def _resolve_circuit_payload(self, payload: dict) -> dict:
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dict")
        if "algorithm" in payload:
            name = payload["algorithm"]
            params = payload.get("params", {})
            return build_algorithm(name, params)
        return payload

    def _validate_circuit_payload(self, payload: dict) -> tuple[int, list[tuple], int | None]:
        if not isinstance(payload, dict):
            raise ValueError("payload must be dict")
        n_qubits = payload.get("n_qubits")
        gates = payload.get("gates")
        shots = payload.get("shots")

        if not isinstance(n_qubits, int):
            raise ValueError("n_qubits must be int")
        if not (1 <= n_qubits <= MAX_QUBITS):
            raise ValueError(f"n_qubits out of range 1..{MAX_QUBITS}")
        if not isinstance(gates, list):
            raise ValueError("gates must be list")
        if len(gates) > MAX_GATES:
            raise ValueError(f"too many gates (max {MAX_GATES})")

        normalized: list[tuple] = []
        for gate in gates:
            if not isinstance(gate, (list, tuple)) or len(gate) < 2:
                raise ValueError("gate must be tuple/list with at least 2 items")
            name = str(gate[0]).upper()
            if name in {"H", "X", "Y", "Z", "S", "T"}:
                if len(gate) != 2:
                    raise ValueError(f"{name} gate requires (name, target)")
                target = int(gate[1])
                if not (0 <= target < n_qubits):
                    raise ValueError("target out of range")
                normalized.append((name, target))
            elif name in {"RX", "RZ"}:
                if len(gate) != 3:
                    raise ValueError(f"{name} gate requires (name, target, theta)")
                target = int(gate[1])
                theta = float(gate[2])
                if not (0 <= target < n_qubits):
                    raise ValueError("target out of range")
                normalized.append((name, target, theta))
            elif name == "CNOT":
                if len(gate) != 3:
                    raise ValueError("CNOT requires (name, control, target)")
                control = int(gate[1])
                target = int(gate[2])
                if not (0 <= control < n_qubits and 0 <= target < n_qubits):
                    raise ValueError("control/target out of range")
                if control == target:
                    raise ValueError("control and target must differ")
                normalized.append((name, control, target))
            else:
                raise ValueError(f"unsupported_gate:{name}")

        if shots is not None:
            if not isinstance(shots, int):
                raise ValueError("shots must be int")
            if not (1 <= shots <= MAX_SHOTS):
                raise ValueError(f"shots out of range 1..{MAX_SHOTS}")

        return n_qubits, normalized, shots