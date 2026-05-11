# ALGORITHMS

## bell
Produces 2-qubit Bell state circuit:
- H(0)
- CNOT(0,1)

Expected ideal probabilities: P(00)=0.5, P(11)=0.5.

## ghz
Produces GHZ circuit for n>=2:
- H(0)
- CNOT(0,1..n-1)

Expected ideal probabilities: half on all-zero and all-one states.

## deutsch_jozsa_small
Toy 2-qubit variant:
- Supports `kind=constant_zero` and `kind=balanced_x`.
- Intended for protocol and execution demonstration.
