from __future__ import annotations

import json

from src import QDelegateServer, build_request


def run_demo() -> None:
    secret = b"dev-secret"
    server = QDelegateServer(shared_secret=secret)

    print("=== VALID RAW CIRCUIT ===")
    payload = {"n_qubits": 2, "gates": [("H", 0), ("CNOT", 0, 1)], "shots": 500}
    req = build_request(secret, "job-raw-1", "nonce-raw-1", payload)
    print(json.dumps(server.submit_job(req), indent=2))

    print("=== VALID NAMED ALGORITHM (GHZ) ===")
    req2 = build_request(secret, "job-algo-1", "nonce-algo-1", {"algorithm": "ghz", "params": {"n_qubits": 3}})
    print(json.dumps(server.submit_job(req2), indent=2))

    print("=== REPLAY NONCE ===")
    req3 = build_request(secret, "job-replay-1", "nonce-same", {"n_qubits": 1, "gates": [("X", 0)]})
    req4 = build_request(secret, "job-replay-2", "nonce-same", {"n_qubits": 1, "gates": [("X", 0)]})
    print(json.dumps(server.submit_job(req3), indent=2))
    print(json.dumps(server.submit_job(req4), indent=2))

    print("=== TAMPERED PAYLOAD ===")
    req5 = build_request(secret, "job-tamper-1", "nonce-tamper-1", {"n_qubits": 1, "gates": [("X", 0)]})
    req5["payload"] = {"n_qubits": 1, "gates": [("Z", 0)]}
    print(json.dumps(server.submit_job(req5), indent=2))


if __name__ == "__main__":
    run_demo()
