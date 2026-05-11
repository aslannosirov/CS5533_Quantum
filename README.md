# Q-Delegate (Submission Build)

A secure delegated quantum-job prototype with:
- authenticated request envelopes,
- replay protection,
- circuit schema validation,
- a local state-vector execution backend,
- named algorithm mode,
- and automated tests.

## Features

- **Protocol security**: HMAC request signing, spec-version enforcement, nonce + job-id replay prevention, timestamp freshness checks.
- **Validation**: strict payload checks (`n_qubits`, gate tuple shape, ranges, shot limits).
- **Quantum execution**: gates `H/X/Y/Z/S/T/RX/RZ/CNOT` with probabilities and optional shot sampling.
- **Algorithms**: `bell`, `ghz`, `deutsch_jozsa_small` (via payload algorithm mode).

## Quickstart

```bash
python -m pytest -q
python demo.py
```

## Request modes

### Raw-circuit mode
```python
payload = {
  "n_qubits": 2,
  "gates": [("H", 0), ("CNOT", 0, 1)],
  "shots": 1024,
}
```

### Named-algorithm mode
```python
payload = {
  "algorithm": "ghz",
  "params": {"n_qubits": 3}
}
```

## Security model summary

Server rejects requests for:
- missing required fields,
- unsupported protocol version,
- stale timestamps,
- duplicate `job_id`,
- reused `nonce`,
- invalid auth tags,
- malformed/unsafe payloads.

## Project structure

```text
src/
  client.py
  protocol.py
  server.py
  quantum_sim.py
  algorithms.py
tests/
  test_server.py
demo.py
pytest.ini
```
