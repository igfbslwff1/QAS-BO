import numpy as np
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from skopt import gp_minimize
from skopt.space import Real
import matplotlib.pyplot as plt
from skopt.learning import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import RBF
import os
from qiskit_algorithms.optimizers import COBYLA

from Sampling_Optimization import get_var_form 
from Sampling_Optimization import samplee
from Initialization import global_best_cost, global_best_params, global_best_qc, global_best_state, global_best_p1

# Used to store fidelity at each step
fidelities = []
fidelities0 = []

# Objective function
def objective_function(params, qubits, gate_choices, batch_fidelities, qubit_op, depths):
    global global_best_cost, global_best_params, global_best_qc, global_best_state
    qc = get_var_form(qubits, depths, gate_choices, params)
    # Calculate fidelity using AerSimulator to simulate the circuit
    simulator = AerSimulator()  # Updated to use AerSimulator
    qc.save_statevector()  # Command to append at the end of the circuit to save the state vector
    result = simulator.run(qc).result()  # Execute the circuit and get the result
    # statevector = Statevector.from_instruction(circuit) # This is the theoretical tensor
    statevector = result.get_statevector()
    # Calculate the expectation value of the Hamiltonian
    expectation_value = Statevector(statevector).expectation_value(qubit_op).real

    batch_fidelities.append(expectation_value)  # Record the current fidelity of each batch
    fidelities0.append(expectation_value)  # Record global fidelity

    # Check and update the global best solution
    if expectation_value < global_best_cost:
        global_best_cost = expectation_value
        global_best_params = params.copy()
        global_best_qc = qc
        global_best_state = statevector

    fidelities.append(global_best_cost)  # Record global fidelity

    return expectation_value, qc, statevector, batch_fidelities

# Inner optimization: Gaussian Process Regression optimizer to adjust angle parameters
def Optimization_for_angles(qubits, gate_choices, n2, Number_of_internal_cycles, qubit_op, depths):
    batch_fidelities = []  # Initialize the list of fidelities

    optimizer = COBYLA(maxiter=Number_of_internal_cycles, tol=0.0001)
    initial_point = np.random.rand(n2) * 2 * np.pi  # Adjust the length of parameters based on n2
    result = optimizer.minimize(fun=lambda x: objective_function(x, qubits, gate_choices, batch_fidelities, qubit_op, depths)[0], x0=initial_point)
    final_cost, final_qc, final_state, batch_fidelities = objective_function(result.x, qubits, gate_choices, batch_fidelities, qubit_op, depths)
    
    # Plot and save the fidelity graph
    plt.figure()
    plt.plot(batch_fidelities, label='energy')
    plt.xlabel('Iteration')
    plt.ylabel('energy')
    plt.title(f'The {iteration_index}_th angle optimization process')
    plt.legend()
    folder_path = 'Process'  # Folder path
    file_path = os.path.join(folder_path, f'The {iteration_index}_th angle optimization process.png')  # Construct file save path
    plt.savefig(file_path)
    plt.close()

    return final_cost, final_qc, result.x, final_state

# Define global data structure
optimization_data = []

iteration_index = 1  # Initialize iteration index

# Create a Gaussian Process Regression model using the default RBF kernel
kernel = 1.0 * RBF(length_scale=0.05)  # Smaller length scale
gpr = GaussianProcessRegressor(kernel=kernel, alpha=1e-10, n_restarts_optimizer=5, normalize_y=False)

# Outer optimization to adjust the multinomial distribution parameters p1
def optimize_p1(initial_p1, qubits, depths, Number_of_internal_cycles, Number_of_external_cycles, qubit_op):
    def outer_objective(p1, qubits, depths, Number_of_internal_cycles, qubit_op):
        global iteration_index  # Declare global variable
        global global_best_p1

        gate_choices, n_rotation = samplee(qubits, depths, p1)
        if n_rotation > 0:
            # Rotation gates are present, parameter optimization is required
            print(f"------------The {iteration_index} th architecture optimization------------")  # Print start of optimization info
            final_cost, final_qc, optimized_angles, final_state = Optimization_for_angles(qubits, gate_choices, n_rotation, Number_of_internal_cycles, qubit_op, depths)
            print("Current optimal ground state energy", global_best_cost)
        else:
            # No rotation gates, no parameter optimization required
            print(f"------------The {iteration_index} th architecture optimization------------")  # Print start of optimization info
            final_cost, final_qc, final_state, batch_fidelities = objective_function([], qubits, gate_choices, [], qubit_op, depths)
            print("Current optimal ground state energy", global_best_cost)
            optimized_angles = []

        # Save current p1, actual and predicted fidelities, parameters, and depths to optimization_data
        optimization_data.append({
            "p1": list(p1),
            "actual_fidelity": final_cost,
            "parameters": list(optimized_angles) if optimized_angles is not None else [],
            "depths": final_qc.depth()
        })

        # Update global best value
        if global_best_cost == final_cost:
            global_best_p1 = p1.copy()  # Save the normalized p1
        iteration_index += 1  # Increment global variable
        return final_cost, p1, final_qc, optimized_angles, final_state

    dimensions = [Real(-8, qubits) for _ in range(len(initial_p1))]  # Optimization space for p1
    result = gp_minimize(lambda x: outer_objective(x, qubits, depths, Number_of_internal_cycles, qubit_op)[0],  # Pass x to the outer objective function and get the first return value
                         dimensions,  # Parameter space
                         base_estimator=gpr,  # Use custom Gaussian Process Regression model
                         n_calls=Number_of_external_cycles,  # Number of function calls
                         n_initial_points=10,  # Number of initial random search points
                         acq_func="gp_hedge",  # Acquisition function: automatically selects the best strategy
                         acq_optimizer="lbfgs",  # Acquisition function optimizer: lbfgs
                         x0=None,  # List of initial points, no initial points
                         y0=None,  # Initial objective function values, no initial values
                         random_state=2,  # Random seed
                         verbose=False,  # Control whether to print detailed output
                         callback=None,  # List of callback functions
                         n_points=10000,  # "sampling" acquisition optimizer evaluates acquisition function at this number of points (invalid parameter)
                         n_restarts_optimizer=5,  # Number of restarts for the acquisition function optimizer
                         kappa=2,  # Exploration parameter for "LCB" acquisition function
                         xi=0.05,  # Exploration parameter for "EI" and "PI" acquisition functions
                         noise="gaussian",  # Assumed noise model
                         n_jobs=-1,  # Number of jobs to run in parallel
                         model_queue_size=None)  # Length of the list of models to keep is only for given parameter values. If None, there is no fixed upper limit to the list length.
    final_cost, updated_p1, final_qc, optimized_angles, final_state = outer_objective(result.x, qubits, depths, Number_of_internal_cycles, qubit_op)
    return global_best_cost, global_best_p1, global_best_qc, global_best_params, global_best_state
