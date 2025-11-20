# quantum_random.py
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
import random


def quantum_coin_toss(shots=1000):
    """Quantum coin toss using statevector simulation."""

    qc = QuantumCircuit(1)
    qc.h(0)

    # get statevector
    sv = Statevector.from_instruction(qc)

    # Probabilities
    probs = sv.probabilities_dict()

    p0 = probs.get('0', 0)
    p1 = probs.get('1', 0)

    # Sample shots
    results = random.choices(["Heads", "Tails"], weights=[p0, p1], k=shots)

    return {
        "Heads": results.count("Heads"),
        "Tails": results.count("Tails"),
        "shots": shots,
        "p(Heads)": p0,
        "p(Tails)": p1
    }


def quantum_dice(shots=1000):
    """Quantum dice (1–6) using 3-qubit statevector."""
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])

    sv = Statevector.from_instruction(qc)

    probs = sv.probabilities_dict()

    # Mapping 3-bit states to dice numbers
    mapping = {
        "000": 1, "001": 2, "010": 3,
        "011": 4, "100": 5, "101": 6
    }

    # Create weighted choices
    outcomes = []
    weights = []

    for bitstring, prob in probs.items():
        if bitstring in mapping:
            outcomes.append(mapping[bitstring])
            weights.append(prob)

    # Sample shots
    results = random.choices(outcomes, weights=weights, k=shots)

    # Count final results 1–6
    final = {i: results.count(i) for i in range(1, 7)}

    return final
