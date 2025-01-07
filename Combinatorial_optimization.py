import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Auxiliary function, which is used to calculate tensor products of operators of all qubits.
def tensor_product(operators):
    result = operators[0]
    for op in operators[1:]:
        result = np.kron(result, op)
    return result

def get_maxcut_qubitops(example_graph_dict, num_qubits):
    # Define edges and weights from the graph dictionary
    edges = []
    for node, connections in example_graph_dict.items():
        node = int(node)  # Convert node index to integer
        for connected_node, attributes in connections.items():
            connected_node = int(connected_node)  # Convert node index to integer
            # Since the graph is undirected, each edge is added only once.
            if node < connected_node:
                edges.append((node, connected_node, attributes['weight']))

    # Defining Pauli Z Matrix and identity matrix
    pauli_z = np.array([[1, 0], [0, -1]])
    identity = np.eye(2)

    # The Hamiltonian matrix H_c is initialized to zero matrix.
    num_qubits = len(example_graph_dict)
    H_c_matrix = np.zeros((2**num_qubits, 2**num_qubits))
    
    # The Hamiltonian matrix is constructed by adding the contribution of each edge.
    for i, j, weight in edges:
        # Initializes the list of operators for the current term of Hamiltonian.
        operators = [identity] * num_qubits 
    
        # Setting Pauli z matrix for connected qubits
        operators[i] = pauli_z
        operators[j] = pauli_z
    
        # Calculate the tensor product of the current term and add it to the Hamiltonian matrix.
        H_c_matrix += -(np.eye(2**num_qubits)-tensor_product(operators))*weight /2

    return H_c_matrix

def get_NAE_3SAT_qubitops(easy_clauses, num_qubits):

    factor = 1 / len(easy_clauses) / 4

    # Create a NetworkX diagram
    easy_graph = nx.Graph()

    # Add edges and initialize weights.
    for i, j, k in easy_clauses:
        easy_graph.add_edge(abs(i), abs(j), weight=0)
        easy_graph.add_edge(abs(j), abs(k), weight=0)
        easy_graph.add_edge(abs(k), abs(i), weight=0)

    # Update edge weights
    for i, j, k in easy_clauses:
        if (i >= 0 and j >= 0) or (i <= 0 and j <= 0):
            easy_graph[abs(i)][abs(j)]["weight"] += 1
        else:
            easy_graph[abs(i)][abs(j)]["weight"] -= 1
        if (j >= 0 and k >= 0) or (j <= 0 and k <= 0):
            easy_graph[abs(j)][abs(k)]["weight"] += 1
        else:
            easy_graph[abs(j)][abs(k)]["weight"] -= 1
        if (k >= 0 and i >= 0) or (k <= 0 and i <= 0):
            easy_graph[abs(k)][abs(i)]["weight"] += 1
        else:
            easy_graph[abs(k)][abs(i)]["weight"] -= 1

     # Convert diagram to dictionary format
    graph_dict = nx.to_dict_of_dicts(easy_graph)

    # Define edges and weights from the graph dictionary
    edges = []
    for node, connections in graph_dict.items():
        node = int(node)  # Convert node index to integer
        for connected_node, attributes in connections.items():
            connected_node = int(connected_node)  # Convert node index to integer
            # Since the graph is undirected, each edge is added only once.
            if node < connected_node:
                edges.append((node, connected_node, attributes['weight']))

    # Defining Pauli Z Matrix and identity matrix
    pauli_z = np.array([[1, 0], [0, -1]])
    identity = np.eye(2)

    # The Hamiltonian matrix H_c is initialized to zero matrix.
    num_qubits = len(graph_dict)
    H_c_matrix = np.zeros((2**num_qubits, 2**num_qubits))
    
    # The Hamiltonian matrix is constructed by adding the contribution of each edge.
    for i, j, weight in edges:
        # Initializes the list of operators for the current term of Hamiltonian.
        operators = [identity] * num_qubits 
    
        # Setting Pauli z matrix for connected qubits
        operators[i-1] = pauli_z
        operators[j-1] = pauli_z
    
        # Calculate the tensor product of the current term and add it to the Hamiltonian matrix.
        H_c_matrix += -(np.eye(2**num_qubits)-tensor_product(operators))*weight /2

    return H_c_matrix, easy_graph