from src.client import build_request
from src.server import QDelegateServer


def test_bell_state_probabilities():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {
        "n_qubits": 2,
        "gates": [
            ("H", 0),
            ("CNOT", 0, 1),
        ],
    }
    req = build_request(b"dev-secret", "job-1", "nonce-1", payload)
    res = server.submit_job(req)
    assert res["ok"] is True
    probs = res["result"]["probabilities"]
    assert abs(probs[0] - 0.5) < 1e-9
    assert abs(probs[3] - 0.5) < 1e-9


def test_replay_nonce_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("X", 0)]}
    req1 = build_request(b"dev-secret", "job-1", "same-nonce", payload)
    req2 = build_request(b"dev-secret", "job-2", "same-nonce", payload)
    assert server.submit_job(req1)["ok"] is True
    res2 = server.submit_job(req2)
    assert res2["ok"] is False
    assert res2["error"] == "reused_nonce"


def test_tampered_payload_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("X", 0)]}
    req = build_request(b"dev-secret", "job-1", "nonce-1", payload)
    req["payload"] = {"n_qubits": 1, "gates": [("Z", 0)]}  # tamper after sign
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["error"] == "bad_auth_tag"
