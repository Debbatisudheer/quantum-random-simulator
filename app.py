import streamlit as st
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import circuit_drawer, plot_bloch_multivector
from quantum_random import quantum_coin_toss, quantum_dice

st.set_page_config(page_title="Quantum Random Simulator", layout="centered")

st.title("🎲 Quantum Random Simulator")

st.markdown("""
This app demonstrates basic **Quantum Randomness** using Qiskit:

- Quantum Coin Toss  
- Quantum Dice (1–6)  
- Statevector simulation  
- Circuit visualization  
- Bloch sphere  
- Probability distributions  
""")

# -------------------------------------------------------
# COIN TOSS
# -------------------------------------------------------

st.header("🪙 Quantum Coin Toss")

shots_coin = st.slider("Number of shots", 100, 5000, 1000, step=100)

if st.button("Run Quantum Coin Toss"):
    result = quantum_coin_toss(shots_coin)

    heads = result["Heads"]
    tails = result["Tails"]

    st.subheader("Result")
    st.write(result)

    # Mini Graph (Small & Mobile Friendly)
    labels = ["Heads", "Tails"]
    values = [heads, tails]

    fig, ax = plt.subplots(figsize=(3, 2))
    ax.bar(labels, values, width=0.5)
    ax.set_title("Coin Toss Distribution", fontsize=10)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)

    # Circuit + Bloch sphere
    qc = QuantumCircuit(1)
    qc.h(0)

    st.subheader("Quantum Circuit (small view)")
    fig = circuit_drawer(qc, output="mpl", scale=0.8)
    fig.set_size_inches(4, 2)
    st.pyplot(fig)

    st.subheader("Bloch Sphere (small view)")
    sv = Statevector.from_instruction(qc)
    fig2 = plot_bloch_multivector(sv)
    fig2.set_size_inches(3, 3)
    st.pyplot(fig2)

# -------------------------------------------------------
# DICE
# -------------------------------------------------------

st.header("🎲 Quantum Dice (1–6)")

shots_dice = st.slider("Dice shots", 100, 5000, 1000, step=100)

if st.button("Roll Quantum Dice"):
    result = quantum_dice(shots_dice)

    st.subheader("Result")
    st.write(result)

    labels = list(result.keys())
    values = list(result.values())

    # Small graph
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.bar(labels, values, width=0.6)
    ax.set_title("Dice Distribution", fontsize=10)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)

    # Circuit
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])

    st.subheader("Quantum Dice Circuit")
    fig = circuit_drawer(qc, output="mpl", scale=0.8)
    fig.set_size_inches(5, 2.2)
    st.pyplot(fig)

    # Bloch sphere (shows only aggregate)
    sv = Statevector.from_instruction(qc)
    st.subheader("Bloch Sphere (superposition)")
    fig2 = plot_bloch_multivector(sv)
    fig2.set_size_inches(3, 3)
    st.pyplot(fig2)

st.info("Quantum randomness uses **true superposition**, unlike classical random generators.")
