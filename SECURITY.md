# SECURITY

## Implemented controls
- HMAC-SHA256 request signing.
- Constant-time auth-tag comparison.
- Replay protection via unique `job_id` and `nonce`.
- Timestamp freshness window to reject stale requests.
- Protocol version enforcement (`v0.5`).
- Circuit validation and limits (qubits/gates/shots).

## Threat coverage
- **Tampering** -> caught by auth-tag verification.
- **Replay** -> blocked by nonce + job-id tracking.
- **Downgrade/version confusion** -> blocked by strict `spec_version` check.
- **Malformed payload abuse** -> blocked by strict validation rules.

## Known limitations
- In-memory replay state (not persistent).
- Shared symmetric secret (no PKI/mTLS in this prototype).
- No HSM/KMS integration.
