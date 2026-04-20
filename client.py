# Q-Delegate

Minimal secure delegated quantum computation protocol prototype.

## What this repo demonstrates

- Client builds authenticated requests
- Server validates schema, version, nonce uniqueness, and job ID uniqueness
- Server decrypts payload with AES-256-GCM
- Server returns a signed response placeholder using SHA-256 over the result payload
- Unit tests run in CI on push and pull request

## Project structure

```text
src/
  crypto_utils.py
  server.py
  client.py
  config.py
tests/
  test_server.py
demo.py
requirements.txt
.github/workflows/ci.yml
```

## Setup

```bash
pip install -r requirements.txt
```

## Run tests

```bash
pytest
```

## Run demo

```bash
python demo.py
```

## Security notes

- No key material is hardcoded in source code
- The demo uses an environment variable if present, otherwise it generates a fresh session key at runtime
- AES-256-GCM is used for authenticated encryption
