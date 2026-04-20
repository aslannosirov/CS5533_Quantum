import json
from src.client import build_request
from src.config import derive_session_key, get_master_secret
from src.server import QDelegateServer


def main() -> None:
    master_secret = get_master_secret()
    session_key = derive_session_key(master_secret)
    server = QDelegateServer(session_key)

    print("=== VALID REQUEST ===")
    req1 = build_request(session_key, "job-001", "H q0; X q1")
    print(json.dumps(server.submit_job(req1), indent=2))

    print("=== REPLAY SAME REQUEST ===")
    print(json.dumps(server.submit_job(req1), indent=2))

    print("=== TAMPERED PAYLOAD ===")
    req2 = build_request(session_key, "job-002", "Z q0")
    req2["payload"] = req2["payload"][:-4] + "AAAA"
    print(json.dumps(server.submit_job(req2), indent=2))

    print("=== UNSUPPORTED CIRCUIT ===")
    req3 = build_request(session_key, "job-003", "T q0", circuit_type="non_clifford")
    print(json.dumps(server.submit_job(req3), indent=2))


if __name__ == "__main__":
    main()
