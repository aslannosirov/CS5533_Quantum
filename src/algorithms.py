"""Named algorithm circuit builders for Q-Delegate."""

from __future__ import annotations


def bell() -> dict:
    return {"n_qubits": 2, "gates": [("H", 0), ("CNOT", 0, 1)]}


def ghz(n_qubits: int = 3) -> dict:
    if n_qubits < 2:
        raise ValueError("ghz requires at least 2 qubits")
    gates = [("H", 0)] + [("CNOT", 0, i) for i in range(1, n_qubits)]
    return {"n_qubits": n_qubits, "gates": gates}


def deutsch_jozsa_small(kind: str = "constant_zero") -> dict:
    """2-qubit (1 input + 1 ancilla) toy variant."""
    if kind not in {"constant_zero", "balanced_x"}:
        raise ValueError("unsupported deutsch_jozsa_small kind")
    gates = [("X", 1), ("H", 0), ("H", 1)]
    if kind == "balanced_x":
        gates.append(("CNOT", 0, 1))
    gates.append(("H", 0))
    return {"n_qubits": 2, "gates": gates}


def build_algorithm(name: str, params: dict | None = None) -> dict:
    params = params or {}
    key = name.lower()
    if key == "bell":
        return bell()
    if key == "ghz":
        return ghz(int(params.get("n_qubits", 3)))
    if key == "deutsch_jozsa_small":
        return deutsch_jozsa_small(str(params.get("kind", "constant_zero")))
    raise ValueError(f"unsupported_algorithm:{name}")
