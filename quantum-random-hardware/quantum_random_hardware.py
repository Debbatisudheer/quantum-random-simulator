# quantum_random_hardware.py
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import numpy as np


# ---------------------------
#  1. COIN CIRCUITS
# ---------------------------

def coin_circuit():
    qc = QuantumCircuit(1)
    qc.h(0)
    return qc


def coin_circuit_measure():
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    return qc


# ---------------------------
#  2. DICE CIRCUITS (3 QUBITS)
# ---------------------------

def dice_circuit():
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])
    return qc


def dice_circuit_measure():
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])
    qc.measure_all()
    return qc


# ---------------------------
#  3. LOCAL STATEVECTOR SIMULATION
# ---------------------------

def simulate_statevector_coin(shots=1000):
    qc = coin_circuit()

    # Statevector
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities_dict()

    p0 = probs.get("0", 0.5)
    p1 = probs.get("1", 0.5)

    counts = {
        "0": int(p0 * shots),
        "1": int(p1 * shots)
    }

    return {
        "success": True,
        "backend": "local_simulator",
        "counts": counts
    }


def simulate_statevector_dice(shots=1000):
    qc = dice_circuit()

    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities_dict()

    mapping = {
        "000": 1, "001": 2, "010": 3,
        "011": 4, "100": 5, "101": 6
    }

    results = {i: 0 for i in range(1, 7)}

    for bitstring, prob in probs.items():
        if bitstring in mapping:
            results[mapping[bitstring]] += int(prob * shots)

    return {
        "success": True,
        "backend": "local_simulator",
        "counts": results
    }


# ---------------------------
#  4. RUN ON IBM REAL HARDWARE
# ---------------------------

def run_on_hardware(qc, shots=1000):
    try:
        service = QiskitRuntimeService()

        backend = service.least_busy(
            filters=lambda b: b.configuration().n_qubits >= qc.num_qubits
        )

        sampler = SamplerV2()

        result = sampler.run(qc, shots=shots, backend=backend).result()
        counts = result[0].data.meas.get("counts", {})

        return {
            "success": True,
            "backend": backend.name,
            "counts": counts
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
