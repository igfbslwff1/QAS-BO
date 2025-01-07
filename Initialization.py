import random

# Define global variables to store the optimal solutions
global_best_cost = float('inf')  # Initially set to infinity
global_best_params = None
global_best_qc = None
global_best_state = None
global_best_p1 = None

# Define a function to initialize normal distribution mean and variance
def def_initial_p1(qubits, depths):
    initial_p1 = []
    for i in range(0, qubits * depths):
        a = [random.randint(-8, qubits)]  # Mean value
        initial_p1.extend(a)
    return initial_p1
