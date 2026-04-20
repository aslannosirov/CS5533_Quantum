"""Tiny state-vector quantum simulator for educational use.

Supported gates: H, X, Z, CNOT.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath


@dataclass
class Circuit:
    n_qubits: int
    gates: list[tuple]


class QuantumSimulator:
    def __init__(self, n_qubits: int):
        if n_qubits <= 0:
            raise ValueError("n_qubits must be > 0")
        self.n_qubits = n_qubits
        self.dim = 1 << n_qubits
        self.state = [0j] * self.dim
        self.state[0] = 1 + 0j  # |00...0>

    def apply_gate(self, gate: tuple) -> None:
        name = gate[0].upper()
        if name == "H":
            self._apply_h(int(gate[1]))
        elif name == "X":
            self._apply_x(int(gate[1]))
        elif name == "Z":
            self._apply_z(int(gate[1]))
        elif name == "CNOT":
            self._apply_cnot(int(gate[1]), int(gate[2]))
        else:
            raise ValueError(f"Unsupported gate: {name}")

    def probabilities(self) -> list[float]:
        return [abs(a) ** 2 for a in self.state]

    def run(self, gates: list[tuple]) -> list[float]:
        for gate in gates:
            self.apply_gate(gate)
        return self.probabilities()

    def _apply_h(self, target: int) -> None:
        self._check_qubit(target)
        inv_sqrt2 = 1 / cmath.sqrt(2)
        step = 1 << target
        for base in range(0, self.dim, step << 1):
            for i in range(step):
                i0 = base + i
                i1 = i0 + step
                a0, a1 = self.state[i0], self.state[i1]
                self.state[i0] = (a0 + a1) * inv_sqrt2
                self.state[i1] = (a0 - a1) * inv_sqrt2

    def _apply_x(self, target: int) -> None:
        self._check_qubit(target)
        bit = 1 << target
        for i in range(self.dim):
            j = i ^ bit
            if i < j:
                self.state[i], self.state[j] = self.state[j], self.state[i]

    def _apply_z(self, target: int) -> None:
        self._check_qubit(target)
        bit = 1 << target
        for i in range(self.dim):
            if i & bit:
                self.state[i] = -self.state[i]

    def _apply_cnot(self, control: int, target: int) -> None:
        self._check_qubit(control)
        self._check_qubit(target)
        if control == target:
            raise ValueError("control and target must differ")
        c_bit = 1 << control
        t_bit = 1 << target
        for i in range(self.dim):
            if i & c_bit:
                j = i ^ t_bit
                if i < j:
                    self.state[i], self.state[j] = self.state[j], self.state[i]

    def _check_qubit(self, idx: int) -> None:
        if not (0 <= idx < self.n_qubits):
            raise ValueError(f"qubit index out of range: {idx}")
