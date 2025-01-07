import numpy as np
from qiskit.quantum_info import Statevector

# Define the randomly generated quantum state function
def generate_random_quantum_state(num_qubits):
    # Randomly generating complex state vectors
    dim = 2 ** num_qubits  # Dimension of quantum state
    random_vector = np.random.rand(dim) + 1j * np.random.rand(dim)  # Random complex number
    # Normalization processing
    normalized_vector = random_vector / np.linalg.norm(random_vector)
    print("Randomly Generated Quantum State:")
    print(Statevector(normalized_vector))

    return Statevector(normalized_vector)
