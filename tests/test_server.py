import time

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
    req["payload"] = {"n_qubits": 1, "gates": [("Z", 0)]}
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["error"] == "bad_auth_tag"


def test_duplicate_job_id_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("X", 0)]}
    req1 = build_request(b"dev-secret", "job-same", "nonce-a", payload)
    req2 = build_request(b"dev-secret", "job-same", "nonce-b", payload)
    assert server.submit_job(req1)["ok"] is True
    res2 = server.submit_job(req2)
    assert res2["ok"] is False
    assert res2["error"] == "duplicate_job_id"


def test_unsupported_version_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("X", 0)]}
    req = build_request(b"dev-secret", "job-v", "nonce-v", payload)
    req["spec_version"] = "v0.4"
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["error"] == "unsupported_version"


def test_unsupported_gate_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("FOO", 0)]}
    req = build_request(b"dev-secret", "job-u", "nonce-u", payload)
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["code"] == "BAD_PAYLOAD"


def test_stale_timestamp_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("X", 0)]}
    stale = int(time.time()) - 1000
    req = build_request(b"dev-secret", "job-s", "nonce-s", payload, timestamp=stale)
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["error"] == "stale_request"


def test_named_algorithm_ghz_runs():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"algorithm": "ghz", "params": {"n_qubits": 3}}
    req = build_request(b"dev-secret", "job-ghz", "nonce-ghz", payload)
    res = server.submit_job(req)
    assert res["ok"] is True
    probs = res["result"]["probabilities"]
    assert abs(probs[0] - 0.5) < 1e-9
    assert abs(probs[7] - 0.5) < 1e-9


def test_shots_counts_returned():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("H", 0)], "shots": 200}
    req = build_request(b"dev-secret", "job-shots", "nonce-shots", payload)
    res = server.submit_job(req)
    assert res["ok"] is True
    counts = res["result"]["counts"]
    assert sum(counts.values()) == 200


def test_malformed_payload_not_dict_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    # payload should be dict; using string should fail server validation
    req = build_request(b"dev-secret", "job-mal-1", "nonce-mal-1", "not-a-dict")  # type: ignore[arg-type]
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["code"] == "BAD_PAYLOAD"


def test_out_of_range_qubit_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("X", 3)]}  # target out of range
    req = build_request(b"dev-secret", "job-range-1", "nonce-range-1", payload)
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["code"] == "BAD_PAYLOAD"


def test_bad_tuple_shape_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 2, "gates": [("CNOT", 0)]}  # missing target
    req = build_request(b"dev-secret", "job-shape-1", "nonce-shape-1", payload)
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["code"] == "BAD_PAYLOAD"


def test_missing_required_field_rejected():
    server = QDelegateServer(shared_secret=b"dev-secret")
    payload = {"n_qubits": 1, "gates": [("X", 0)]}
    req = build_request(b"dev-secret", "job-miss-1", "nonce-miss-1", payload)
    del req["auth_tag"]  # simulate malformed request envelope
    res = server.submit_job(req)
    assert res["ok"] is False
    assert res["code"] == "MISSING_FIELD"