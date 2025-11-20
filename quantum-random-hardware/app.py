# app.py
import streamlit as st
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_vector
from quantum_random_hardware import (
    coin_circuit_measure, dice_circuit_measure,
    simulate_statevector_coin, simulate_statevector_dice,
    run_on_hardware
)

# Streamlit UI
st.title("⚛ Quantum Random — Hardware Edition")
st.write("""
Run quantum **coin toss** or **dice roll** on:

🖥 Local statevector simulator  
🧪 REAL IBM Quantum Hardware (free plan)  

If hardware fails → automatic fallback.
""")

from qiskit_ibm_runtime import QiskitRuntimeService

# Check IBM connection
try:
    service = QiskitRuntimeService()
    st.success("Connected to IBM Quantum Service ✓")
except:
    st.warning("⚠ Not connected to IBM Quantum service. Only local simulation will run.")


# USER INPUTS
experiment = st.radio("Experiment", ["Coin Toss", "Dice Roll"])
shots = st.slider("Shots", 100, 2000, 1000)


run_btn = st.button("Run Quantum Experiment")

if run_btn:
    st.header("🎯 Running Experiment...")

    if experiment == "Coin Toss":
        qc = coin_circuit_measure()
    else:
        qc = dice_circuit_measure()

    st.subheader("🔷 Quantum Circuit")
    fig = qc.draw(output="mpl")
    st.pyplot(fig)

    st.write("Submitting job…")

    hw = run_on_hardware(qc, shots)

    if hw["success"]:
        st.success(f"Hardware backend: {hw['backend']}")
        st.json(hw)
        counts = hw["counts"]
    else:
        st.error(f"Hardware error: {hw['error']}")
        st.info("Falling back to local simulation…")

        if experiment == "Coin Toss":
            sim = simulate_statevector_coin(shots)
        else:
            sim = simulate_statevector_dice(shots)

        st.json(sim)
        counts = sim["counts"]

    # GRAPH
    st.subheader("📊 Probability Distribution")
    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    st.pyplot(fig)
