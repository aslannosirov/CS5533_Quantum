# API Specification — Q-Delegate

## 1. Protocol Overview

The Q-Delegate protocol defines how a client securely submits quantum computation jobs to a server and retrieves results. All messages must follow the defined schema and pass validation checks before processing.

---

## 2. Protocol Version

All messages must include:

spec_version = "v0.5"

### Rules

- Messages missing `spec_version` are rejected
- Unknown or older versions are rejected

---

## 3. Endpoint: Submit Job

### Description

Allows a client to submit a quantum computation job to the server.

---

### Request Format

```json
{
  "spec_version": "v0.5",
  "job_id": "string",
  "client_id": "string",
  "nonce": "base64",
  "timestamp": "integer",
  "circuit_type": "string",
  "payload": "base64",
  "auth_tag": "base64"
}
