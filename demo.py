# Threat Model — Q-Delegate

## 1. System Overview

The Q-Delegate system implements a secure delegated quantum computation workflow. A client submits a quantum job to a remote server, which evaluates the circuit and returns a result. All communication occurs over an untrusted network.

### Components

- **Client**
  - Constructs job requests
  - Generates job_id and nonce
  - Authenticates requests
  - Verifies server responses

- **Server**
  - Validates incoming requests
  - Enforces replay protection
  - Executes quantum circuit (simulated)
  - Returns signed results

- **Crypto Module**
  - Handles encryption and authentication (AEAD)
  - Verifies signatures
  - Performs key derivation (HKDF)

- **Storage / State**
  - Tracks used nonces
  - Tracks processed job_ids
  - Stores session metadata

---

## 2. Assets

The following assets must be protected:

- Integrity of job requests
- Integrity of job results
- Session keys
- Nonces
- Job identifiers (job_id)
- Protocol version and configuration
- Server identity (authenticity of responses)

---

## 3. Attackers

We assume a network-based adversary with the ability to:

- Intercept messages
- Modify messages in transit
- Replay previously valid messages
- Send malformed or malicious requests
- Attempt protocol downgrade attacks

We do not assume:

- Compromise of server private keys
- Full system compromise

---

## 4. Trust Boundaries

### Boundary 1 — Client ↔ Network ↔ Server
- This boundary is **untrusted**
- All messages must be authenticated and validated

### Boundary 2 — Server Internal State
- Trusted environment
- Must enforce:
  - replay protection
  - nonce uniqueness
  - job_id uniqueness

### Boundary 3 — Crypto Module
- Trusted abstraction layer
- Must not expose raw key material

---

## 5. Data Flow Description

### Flow 1 — Job Submission
Client → Server  
Fields:
- job_id
- nonce
- payload
- spec_version
- auth_tag

---

### Flow 2 — Validation
Server verifies:
- authentication tag (AEAD)
- schema correctness
- nonce uniqueness
- job_id uniqueness
- protocol version

---

### Flow 3 — Execution
Server executes the quantum circuit using a simulator.

---

### Flow 4 — Result Return
Server → Client  
Fields:
- job_id
- result_payload
- signature
- spec_version

---

### Flow 5 — Verification
Client verifies:
- server signature
- job_id match
- protocol version

---

## 6. Misuse Cases

### M1 — Replay Attack
An attacker resends a previously valid job request.

Impact:
- duplicate execution
- resource abuse

---

### M2 — Nonce Reuse
A nonce is reused under the same key.

Impact:
- breaks AEAD security guarantees

---

### M3 — Message Tampering
An attacker modifies the job payload in transit.

Impact:
- incorrect or malicious computation

---

### M4 — Downgrade Attack
An attacker forces use of an older protocol version.

Impact:
- weaker security protections

---

### M5 — Invalid Input Injection
An attacker sends malformed or oversized payloads.

Impact:
- crashes or undefined behavior

---

### M6 — Key Leakage via Logging
Sensitive keys are accidentally written to logs.

Impact:
- compromise of session security

---

### M7 — Job ID Replay / Collision
An attacker reuses or duplicates job_id values.

Impact:
- job confusion or overwrite

---

## 7. Security Requirements

1. The system shall authenticate all client requests using AEAD.
2. The system shall reject any message with an invalid authentication tag.
3. The system shall enforce nonce uniqueness per key context.
4. The system shall reject reused nonces.
5. The system shall enforce unique job_id values and reject duplicates.
6. The system shall include a protocol version in every request and validate it.
7. The system shall reject unsupported or downgraded protocol versions.
8. The system shall validate all required fields before processing a request.
9. The system shall limit payload size to a predefined maximum.
10. The system shall sign all server responses.
11. The system shall verify server signatures on the client side.
12. The system shall never log raw cryptographic keys or secrets.
13. The system shall derive session keys using a secure KDF.
14. The system shall bind job_id, nonce, and payload within authentication.

---

## 8. Threat to Requirement Mapping

| Threat | Requirements |
|--------|-------------|
| M1 — Replay Attack | 3, 4, 5 |
| M2 — Nonce Reuse | 3, 4 |
| M3 — Message Tampering | 1, 2, 14 |
| M4 — Downgrade Attack | 6, 7 |
| M5 — Invalid Input | 8, 9 |
| M6 — Key Leakage | 12, 13 |
| M7 — Job ID Replay | 5, 14 |

---

## 9. Summary

This threat model defines:

- System components and trust boundaries
- Realistic attacker capabilities
- Concrete misuse cases
- Testable security requirements
- Traceability between threats and mitigations

This provides a complete and defensible security foundation for the Q-Delegate protocol.
