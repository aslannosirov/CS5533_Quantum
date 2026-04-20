# Key Lifecycle — Q-Delegate

## 1. Overview

This document defines how cryptographic keys are generated, stored, used, rotated, and revoked within the Q-Delegate protocol. Proper key management is critical to maintaining system security.

---

## 2. Key Types

| Key Type | Purpose |
|----------|--------|
| Master Key | Root secret used for deriving session keys |
| Session Key | Used for AEAD encryption (AES-GCM) |
| Server Signing Key | Used to sign responses (Ed25519) |

---

## 3. Key Generation

- Master key is generated using a secure random number generator
- Session keys are derived using HKDF-SHA256 from the master key
- Signing key pair (Ed25519) is generated once for the server

---

## 4. Key Storage

- Keys are never stored in source code
- Local development uses environment variables (`.env`)
- Server signing key is stored securely and not exposed
- Session keys exist only in memory during execution

---

## 5. Key Usage

- Session keys are used only for AEAD encryption/decryption
- Signing keys are used only for generating/verifying signatures
- Keys are not reused across different purposes

---

## 6. Key Rotation

- Session keys are rotated per job or session
- Each job uses a fresh derived key
- Master key is not rotated in the MVP but is documented for future improvement

---

## 7. Key Revocation

If a key is suspected to be compromised:

1. Mark the associated key context as revoked
2. Reject all requests using that key
3. Generate new session keys
4. Log the event for auditing
5. Restart affected sessions

---

## 8. Compromise Handling

In the event of compromise:

- All active sessions are invalidated
- New keys are derived
- Old keys are no longer accepted
- System logs the incident

---

## 9. Security Requirements

- Keys shall be generated using secure randomness
- Keys shall never be logged or exposed
- Keys shall be separated by purpose
- Session keys shall be short-lived
- Compromised keys shall be revoked immediately

---

## 10. Summary

The Q-Delegate system enforces:

- Secure key generation
- Safe key storage practices
- Controlled key usage
- Session-based key rotation
- Defined compromise response procedures

This ensures that cryptographic keys remain protected throughout their lifecycle.
