import json
import matplotlib.pyplot as plt
import os
from scipy.sparse.linalg import eigsh
import numpy as np
from qiskit.result import QuasiDistribution

from Initialization import def_initial_p1
from Bayesian_optimization import optimize_p1
from Bayesian_optimization import fidelities, fidelities0, optimization_data
from Bayesian_optimization_random_state import optimize_p1_random_state
from Bayesian_optimization_random_state import fidelities_random_state, fidelities0_random_state, optimization_data_random_state
from Chemical_molecule import Chemical_molecule
from Combinatorial_optimization import get_maxcut_qubitops, get_NAE_3SAT_qubitops
from Combinatorial_optimization_solver import find_UMC_solution, find_WMC_solution, find_NAE_3SAT_solution,get_probability_distribution, simulate_measurements, draw_simulate_measurement
from Logic_expression import logic_expression
from Generate_random_quantum_state import generate_random_quantum_state

def sub(problem, qubits,depths,FreezeCore, Mapper, atoms, coords, charge, multiplicity, remove_orbitals, Number_of_internal_cycles, Number_of_external_cycles, w, clause):

    initial_p1=def_initial_p1(qubits,depths)
    ###############################################################################################################################################################################
    if problem == 'Quantum Chemistry Ground State Energy Estimation':
        print()
        qubit_op = Chemical_molecule(FreezeCore, Mapper, atoms, coords, charge, multiplicity, remove_orbitals)
        final_cost, updated_p1, final_qc, optimized_angles,final_state = optimize_p1(initial_p1, qubits, depths, Number_of_internal_cycles, Number_of_external_cycles, qubit_op)


        # Output optimization results
        print("\nUpdated p1 :", updated_p1)
        print("Optimal molecular ground state energy:", final_cost)
        print("Optimized angle parameters:", optimized_angles)

        folder_path = 'Final_Data'

        # Create and draw circuits
        figure = final_qc.draw('mpl')
        # Save the circuit diagram as a picture file
        figure.savefig(os.path.join(folder_path, 'final_qc.png'))

        print("Depth:", final_qc.depth())
        print("Final Statevector:\n", final_state)

        # Draw a graph of fidelity change
        plt.figure()
        plt.plot(fidelities, label='energy')
        plt.xlabel('Iteration')
        plt.ylabel('Energy')
        plt.title('Energy over Optimization Iterations')
        plt.legend()
        plt.savefig(os.path.join(folder_path, 'test.jpg'))

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities.json'), mode='w') as file:
            json.dump(fidelities, file)

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities0.json'), mode='w') as file:
            json.dump(fidelities0, file)

        # Save optimization data to JSON file
        with open(os.path.join(folder_path, 'optimization_data.json'), 'w') as file:
            json.dump(optimization_data, file, indent=4)
    
        # Convert SparsePauliOp into sparse matrix
        matrix = qubit_op.to_matrix(sparse=True)

        # Using SciPy to Calculate the Minimum Eigenvalue
        # Use' which="SA "'to find the smallest eigenvalue ('SA': smallest algebraic).
        values, vectors = eigsh(matrix, k=1, which='SA')  # Calculating the minimum eigenvalues and corresponding eigenvectors

        # Output minimum eigenvalue
        print("Standard:", values[0])
        print("Error:", final_cost-values[0])

    ###############################################################################################################################################################################
    elif problem == 'The Unweighted Max-Cut Problem':
        qubit_op = get_maxcut_qubitops(w, qubits)
        final_cost, updated_p1, final_qc, optimized_angles,final_state = optimize_p1(initial_p1, qubits, depths, Number_of_internal_cycles, Number_of_external_cycles, qubit_op)

        # Output optimization results
        print("\nUpdated p1 :", updated_p1)
        print("Optimal molecular ground state energy:", final_cost)
        print("Optimized angle parameters:", optimized_angles)

        folder_path = 'Final_Data'

        # Create and draw circuits
        figure = final_qc.draw('mpl')
        # Save the circuit diagram as a picture file
        figure.savefig(os.path.join(folder_path, 'final_qc.png'))

        print("Depth:", final_qc.depth())
        print("Final Statevector:\n", final_state)

        # Draw a graph of fidelity change
        plt.figure()
        plt.plot(fidelities, label='energy')
        plt.xlabel('Iteration')
        plt.ylabel('Energy')
        plt.title('Energy over Optimization Iterations')
        plt.legend()
        plt.savefig(os.path.join(folder_path, 'test.jpg'))

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities.json'), mode='w') as file:
            json.dump(fidelities, file)

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities0.json'), mode='w') as file:
            json.dump(fidelities0, file)

        # Save optimization data to JSON file
        with open(os.path.join(folder_path, 'optimization_data.json'), 'w') as file:
            json.dump(optimization_data, file, indent=4)

        # Using SciPy to Calculate the Minimum Eigenvalue
        # Use' which="SA "'to find the smallest eigenvalue ('SA': smallest algebraic).
        values, vectors = eigsh(qubit_op, k=1, which='SA')  # Calculating the minimum eigenvalues and corresponding eigenvectors

        # Output minimum eigenvalue
        print("Standard:", values[0])
        print("Error:", final_cost-values[0])
        print()

        max_cuts = find_UMC_solution(qubits,w)

        state_dict = get_probability_distribution(final_state)
        print("\nState dictionary:")
        print(state_dict)

        results = simulate_measurements(state_dict, num_shots=1024)
        print("Analog measurement results:")
        print(results)

        draw_simulate_measurement(results, max_cuts, qubits)

    ###############################################################################################################################################################################   
    elif problem == 'The Weighted Max-Cut Problem':
        qubit_op = get_maxcut_qubitops(w, qubits)
        final_cost, updated_p1, final_qc, optimized_angles,final_state = optimize_p1(initial_p1, qubits, depths, Number_of_internal_cycles, Number_of_external_cycles, qubit_op)

        # Output optimization results
        print("\nUpdated p1 :", updated_p1)
        print("Optimal molecular ground state energy:", final_cost)
        print("Optimized angle parameters:", optimized_angles)

        folder_path = 'Final_Data'

        # Create and draw circuits
        figure = final_qc.draw('mpl')
        # Save the circuit diagram as a picture file
        figure.savefig(os.path.join(folder_path, 'final_qc.png'))

        print("Depth:", final_qc.depth())
        print("Final Statevector:\n", final_state)

        # Draw a graph of fidelity change
        plt.figure()
        plt.plot(fidelities, label='energy')
        plt.xlabel('Iteration')
        plt.ylabel('Energy')
        plt.title('Energy over Optimization Iterations')
        plt.legend()
        plt.savefig(os.path.join(folder_path, 'test.jpg'))

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities.json'), mode='w') as file:
            json.dump(fidelities, file)

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities0.json'), mode='w') as file:
            json.dump(fidelities0, file)

        # Save optimization data to JSON file
        with open(os.path.join(folder_path, 'optimization_data.json'), 'w') as file:
            json.dump(optimization_data, file, indent=4)

        # Using SciPy to Calculate the Minimum Eigenvalue
        # Use' which="SA "'to find the smallest eigenvalue ('SA': smallest algebraic).
        values, vectors = eigsh(qubit_op, k=1, which='SA')  # Calculating the minimum eigenvalues and corresponding eigenvectors

        # Output minimum eigenvalue
        print("Standard:", values[0])
        print("Error:", final_cost-values[0])
        print()

        max_cuts = find_WMC_solution(qubits,w)

        state_dict = get_probability_distribution(final_state)
        print("\nState dictionary:")
        print(state_dict)

        results = simulate_measurements(state_dict, num_shots=1024)
        print("Analog measurement results:")
        print(results)

        draw_simulate_measurement(results, max_cuts, qubits)

    ###############################################################################################################################################################################
    elif problem == 'Not-All-Equal 3-Satisfiability':
        logic_expression(clause)
        qubit_op, graph_dict = get_NAE_3SAT_qubitops(clause, qubits)
        
        final_cost, updated_p1, final_qc, optimized_angles,final_state = optimize_p1(initial_p1, qubits, depths, Number_of_internal_cycles, Number_of_external_cycles, qubit_op)

        # Output optimization results
        print("\nUpdated p1 :", updated_p1)
        print("Optimal molecular ground state energy:", final_cost)
        print("Optimized angle parameters:", optimized_angles)

        folder_path = 'Final_Data'

        # Create and draw circuits
        figure = final_qc.draw('mpl')
        # Save the circuit diagram as a picture file
        figure.savefig(os.path.join(folder_path, 'final_qc.png'))

        print("Depth:", final_qc.depth())
        print("Final Statevector:\n", final_state)

        # Draw a graph of fidelity change
        plt.figure()
        plt.plot(fidelities, label='energy')
        plt.xlabel('Iteration')
        plt.ylabel('Energy')
        plt.title('Energy over Optimization Iterations')
        plt.legend()
        plt.savefig(os.path.join(folder_path, 'test.jpg'))

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities.json'), mode='w') as file:
            json.dump(fidelities, file)

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities0.json'), mode='w') as file:
            json.dump(fidelities0, file)
            
        # Save optimization data to JSON file
        with open(os.path.join(folder_path, 'optimization_data.json'), 'w') as file:
            json.dump(optimization_data, file, indent=4)

        # Using SciPy to Calculate the Minimum Eigenvalue
        # Use' which="SA "'to find the smallest eigenvalue ('SA': smallest algebraic).
        values, vectors = eigsh(qubit_op, k=1, which='SA')  # Calculating the minimum eigenvalues and corresponding eigenvectors

        # Output minimum eigenvalue
        print("Standard:", values[0])

        print("Error:", final_cost-values[0])
        print()

        max_cuts = find_NAE_3SAT_solution(qubits,graph_dict)

        state_dict = get_probability_distribution(final_state)
        print("State dictionary:")
        print(state_dict)

        results = simulate_measurements(state_dict, num_shots=1024)
        print("Analog measurement results:")
        print(results)

        draw_simulate_measurement(results, max_cuts, qubits)
        
###############################################################################################################################################################################
    elif problem == 'Simulation of Arbitrary Quantum States':
        print()
        target_state = generate_random_quantum_state(qubits)
        print()
        final_cost, updated_p1, final_qc, optimized_angles,final_state = optimize_p1_random_state(initial_p1, qubits, depths, Number_of_internal_cycles, Number_of_external_cycles, target_state)


        # Output optimization results
        print("\nUpdated p1 :", updated_p1)
        print("Optimal molecular ground state energy:", final_cost)
        print("Optimized angle parameters:", optimized_angles)

        folder_path = 'Final_Data'

        # Create and draw circuits
        figure = final_qc.draw('mpl')
        # Save the circuit diagram as a picture file
        figure.savefig(os.path.join(folder_path, 'final_qc.png'))

        print("Depth:", final_qc.depth())
        print("Final Statevector:\n", final_state)

        # Output minimum eigenvalue
        print("Error:", final_cost)

        # Draw a graph of fidelity change
        plt.figure()
        plt.plot(fidelities, label='energy')
        plt.xlabel('Iteration')
        plt.ylabel('Energy')
        plt.title('Energy over Optimization Iterations')
        plt.legend()
        plt.savefig(os.path.join(folder_path, 'test.jpg'))

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities.json'), mode='w') as file:
            json.dump(fidelities_random_state, file)

        # Save fidelity data to JSON file
        with open(os.path.join(folder_path, 'fidelities0.json'), mode='w') as file:
            json.dump(fidelities0_random_state, file)

        # Save optimization data to JSON file
        with open(os.path.join(folder_path, 'optimization_data.json'), 'w') as file:
            json.dump(optimization_data_random_state, file, indent=4)
