# RESULTS

## Automated tests
Run:

```bash
python -m pytest -q
```

Current suite validates:
- Bell-state correctness.
- Replay nonce rejection.
- Tampered payload rejection.
- Duplicate job-id rejection.
- Unsupported version rejection.
- Unsupported gate rejection.
- Stale timestamp rejection.
- Named algorithm execution.
- Shot sampling behavior.

## Demo
Run:

```bash
python demo.py
```

Demo prints success and rejection scenarios in JSON.
