from qiskit_ibm_runtime import QiskitRuntimeService

try:
    service = QiskitRuntimeService()
    print("IBM Quantum Backends:")
    print(service.backends())
except Exception as e:
    print("ERROR:", e)
