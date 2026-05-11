"""Tiny state-vector quantum simulator for educational use.

Supported gates: H, X, Y, Z, S, T, RX(theta), RZ(theta), CNOT.
"""

from __future__ import annotations

import cmath
import math
import random


class QuantumSimulator:
    def __init__(self, n_qubits: int):
        if n_qubits <= 0:
            raise ValueError("n_qubits must be > 0")
        self.n_qubits = n_qubits
        self.dim = 1 << n_qubits
        self.state = [0j] * self.dim
        self.state[0] = 1 + 0j

    def apply_gate(self, gate: tuple) -> None:
        name = gate[0].upper()
        if name == "H":
            self._apply_h(int(gate[1]))
        elif name == "X":
            self._apply_x(int(gate[1]))
        elif name == "Y":
            self._apply_y(int(gate[1]))
        elif name == "Z":
            self._apply_z(int(gate[1]))
        elif name == "S":
            self._apply_phase(int(gate[1]), 1j)
        elif name == "T":
            self._apply_phase(int(gate[1]), cmath.exp(1j * math.pi / 4))
        elif name == "RX":
            self._apply_rx(int(gate[1]), float(gate[2]))
        elif name == "RZ":
            self._apply_rz(int(gate[1]), float(gate[2]))
        elif name == "CNOT":
            self._apply_cnot(int(gate[1]), int(gate[2]))
        else:
            raise ValueError(f"unsupported_gate:{name}")

    def probabilities(self) -> list[float]:
        return [abs(a) ** 2 for a in self.state]

    def run(self, gates: list[tuple]) -> list[float]:
        for gate in gates:
            self.apply_gate(gate)
        return self.probabilities()

    def sample_counts(self, shots: int) -> dict[str, int]:
        if shots <= 0:
            raise ValueError("shots must be > 0")
        probs = self.probabilities()
        outcomes = list(range(self.dim))
        draws = random.choices(outcomes, weights=probs, k=shots)
        counts: dict[str, int] = {}
        for idx in draws:
            b = format(idx, f"0{self.n_qubits}b")
            counts[b] = counts.get(b, 0) + 1
        return counts

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

    def _apply_y(self, target: int) -> None:
        self._check_qubit(target)
        bit = 1 << target
        for i in range(self.dim):
            if i & bit:
                continue
            j = i | bit
            a0, a1 = self.state[i], self.state[j]
            self.state[i] = -1j * a1
            self.state[j] = 1j * a0

    def _apply_z(self, target: int) -> None:
        self._check_qubit(target)
        bit = 1 << target
        for i in range(self.dim):
            if i & bit:
                self.state[i] = -self.state[i]

    def _apply_phase(self, target: int, phase: complex) -> None:
        self._check_qubit(target)
        bit = 1 << target
        for i in range(self.dim):
            if i & bit:
                self.state[i] *= phase

    def _apply_rx(self, target: int, theta: float) -> None:
        self._check_qubit(target)
        bit = 1 << target
        c = math.cos(theta / 2)
        s = -1j * math.sin(theta / 2)
        for i in range(self.dim):
            if i & bit:
                continue
            j = i | bit
            a0, a1 = self.state[i], self.state[j]
            self.state[i] = c * a0 + s * a1
            self.state[j] = s * a0 + c * a1

    def _apply_rz(self, target: int, theta: float) -> None:
        self._check_qubit(target)
        p0 = cmath.exp(-1j * theta / 2)
        p1 = cmath.exp(1j * theta / 2)
        bit = 1 << target
        for i in range(self.dim):
            self.state[i] *= p1 if (i & bit) else p0

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
            raise ValueError(f"qubit_index_out_of_range:{idx}")