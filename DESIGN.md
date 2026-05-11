# DESIGN

## End-to-end flow
1. Client builds signed request (`build_request`).
2. Server verifies required fields + protocol version + timestamp freshness.
3. Server checks replay state (`job_id`, `nonce`).
4. Server verifies HMAC tag.
5. Server resolves payload:
   - raw gates, or
   - named algorithm -> generated circuit.
6. Server validates circuit schema.
7. Server executes on local simulator.
8. Server returns probabilities (+ optional sampled counts).

## Why this design
- Keeps protocol and execution separated.
- Allows secure delegation semantics even with local simulator backend.
- Enables future backend swap (e.g., Qiskit/hardware adapter) with stable protocol layer.
