import numpy as np
from qiskit import QuantumCircuit
from scipy.stats import norm

# Sample the distribution of the quantum circuit
def samplee(qubits, depths, p1):
    gate_choices = []
    n_rotations = 0  # Count the number of rotation gates
    used_in_cnot = np.zeros((qubits, depths), dtype=bool)

    for i in range(qubits):
        gate_row = []
        for j in range(depths):
            if used_in_cnot[i][j]:
                gate_row.append(None)  # If this position is occupied by a CNOT gate, select no gate
                continue

            # Define the types of gates and their normal distribution parameters
            gate_types = {
                'rx': -7,
                'ry': -6,
                'rz': -5,
                'h': -4,
                's': -3,
                't': -2,
                'id': -1
            }
            for k in range(i + 1, qubits):
                gate_types[f'cx({i},{k})'] = k-i  # Dynamically define CNOT gates

            # Calculate the PDF value for each gate
            pdf_values = {}
            for gate, value in gate_types.items():
                mean = p1[depths*i+j]
                variance = 100
                pdf_values[gate] = norm.pdf(value, mean, np.sqrt(variance))

            # Exclude CNOT gates on the target qubit that are already occupied
            for gate in list(pdf_values.keys()):
                if 'cx' in gate:
                    _, target = map(int, gate.split('(')[1].split(')')[0].split(','))
                    if used_in_cnot[target][j]:
                        pdf_values[gate] = 0

            # Select the gate type with the highest PDF value
            selected_gate = max(pdf_values, key=pdf_values.get)
            gate_row.append(selected_gate)

            # Mark rotation gates and CNOT target as used
            if selected_gate in ['rx', 'ry', 'rz']:
                n_rotations += 1
            elif 'cx' in selected_gate:
                _, target = map(int, selected_gate.split('(')[1].split(')')[0].split(','))
                used_in_cnot[target][j] = True

        gate_choices.append(gate_row)

    return gate_choices, n_rotations


# Optimize the circuit
def preprocess_gates(qubits, depths, gate_choices):
    changes_made = True
    while changes_made:  # Continue optimizing until no more changes are made
        changes_made = False
        
        for i in range(qubits):
            
            # Reset all
            count_S = 0
            count_T = 0
            last_gate = None  # Track the last gate that is not 'XX'
            gate_positions = []  # Track positions of gates that are not 'XX'

            for j in range(depths):

                current_gate = gate_choices[i][j]

                if current_gate is None:  # For the control qubit of CNOT

                    # Reset S and T gate counts
                    count_S = 0
                    count_T = 0

                    last_gate = current_gate
                    gate_positions = []
                    continue  # Skip gates marked as None

                elif current_gate == 'XX':
                    continue  # Skip gates marked as XX

                # Eliminate identity gate 'id'
                elif current_gate == 'id':

                    # Reset S and T gate counts
                    count_S = 0
                    count_T = 0

                    gate_choices[i][j] = 'XX'
                    last_gate = current_gate
                    gate_positions = []
                    
                    changes_made = True
                    continue

                # Optimize the Hadamard gate 'h'
                elif current_gate == 'h':

                    # Reset S and T gate counts
                    count_S = 0
                    count_T = 0 

                    if last_gate == 'h':  # Two consecutive 'h' gates are equivalent to an identity gate 'id'
                        gate_choices[i][j] = 'XX'
                        gate_choices[i][gate_positions[-1]] = 'XX'
                        gate_positions = []
                        last_gate = None
                        changes_made = True
                        continue
                    else:
                        gate_positions = []
                        last_gate = current_gate
                        gate_positions.append(j)
                        continue

                # Optimize the 's' gate
                elif current_gate == 's':

                    # Reset T gate count
                    count_T = 0
                    
                    count_S += 1
                    if count_S == 4:  # Four consecutive 's' gates are equivalent to an identity gate 'id'
                        gate_positions.append(j)
                        for k in range(4):
                            gate_choices[i][gate_positions[-1-k]] = 'XX'
                        count_S = 0
                        gate_positions = []
                        last_gate = None
                        changes_made = True
                        continue
                    elif count_S == 1:
                        gate_positions = []
                        last_gate = current_gate
                        gate_positions.append(j)
                        continue
                    else:
                        last_gate = current_gate
                        gate_positions.append(j)
                        continue
                
                # Optimize the 't' gate
                elif current_gate == 't':

                    # Reset S gate count
                    count_S = 0

                    count_T += 1
                    if count_T == 8:  # Eight consecutive 't' gates are equivalent to an identity gate 'id'
                        gate_positions.append(j)
                        for k in range(8):
                            gate_choices[i][gate_positions[-1-k]] = 'XX'
                        count_T = 0
                        last_gate = None
                        gate_positions = []
                        changes_made = True
                        continue
                    elif count_T == 1:
                        gate_positions = []
                        last_gate = current_gate
                        gate_positions.append(j)
                        continue
                    else:
                        last_gate = current_gate
                        gate_positions.append(j)
                        continue   

                # Handle consecutive identical CNOT gates
                elif 'cx' in current_gate:

                    # Reset S and T gate counts
                    count_S = 0
                    count_T = 0

                    control, target = map(int, current_gate.split('(')[1].split(')')[0].split(','))
                    if (control, target) == last_gate:
                        gate_choices[i][j] = 'XX'
                        gate_choices[i][gate_positions[-1]] = 'XX'
                        gate_positions = []
                        last_gate = None
                        changes_made = True
                        continue
                    else:
                        gate_positions = []
                        last_gate = (control, target)
                        gate_positions.append(j)
                        continue

                # Do not process rotation gates rx, ry, rz
                else:

                    # Reset S and T gate counts
                    count_S = 0
                    count_T = 0

                    last_gate = current_gate
                    gate_positions = []

    # Final cleanup: Replace all 'XX' markers with None
    for i in range(qubits):
        for j in range(depths):
            if gate_choices[i][j] == 'XX':
                gate_choices[i][j] = None

    return gate_choices

# Define the quantum circuit
def get_var_form(qubits, depths, gate_choices, params):
    # Preprocess gates to optimize and finalize the gate choices
    gate_choices = preprocess_gates(qubits, depths, gate_choices)
    param_index = 0  # Initialize parameter index for parametric gates
    qc = QuantumCircuit(qubits)  # Create a new quantum circuit with the given number of qubits

    # Loop through each depth and each qubit to place gates
    for j in range(depths):
        for i in range(qubits):
            selected_gate = gate_choices[i][j]  # Get the gate selected for this position
            if selected_gate is None:
                continue  # Skip if no gate is selected

            # Check if the gate is one of the non-parametric gates
            if selected_gate in ['h', 's', 't', 'id']:
                getattr(qc, selected_gate)(i)  # Apply the gate to the circuit
            # Check if the gate is one of the parametric rotation gates
            elif selected_gate in ['rx', 'ry', 'rz']:
                getattr(qc, selected_gate)(params[param_index], i)  # Apply the gate with a parameter
                param_index += 1  # Increment parameter index
            # Handle controlled-X gates (CNOT)
            elif 'cx' in selected_gate:
                control, target = map(int, selected_gate.split('(')[1].split(')')[0].split(','))  # Parse the control and target qubits
                qc.cx(control, target)  # Apply the CNOT gate

    return qc  # Return the constructed quantum circuit
