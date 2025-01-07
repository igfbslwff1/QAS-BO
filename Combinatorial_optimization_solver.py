import numpy as np
import networkx as nx
from qiskit.result import QuasiDistribution
import matplotlib.pyplot as plt
import itertools

#################################################################################################
# Extract probability distribution
def get_probability_distribution(state_vector):
    # Obtain the probability distribution of quantum states.
    if isinstance(state_vector, QuasiDistribution):
         state_dict = state_vector.binary_probabilities()
    else:
        state_vector = np.asarray(state_vector)
        state_dict = {np.binary_repr(i, width=int(np.log2(len(state_vector)))): abs(amplitude)**2
                    for i, amplitude in enumerate(state_vector)}

    return state_dict

def simulate_measurements(prob_dist, num_shots=1024):
    # According to the probability distribution, the measurement simulation is carried out.
    states, probabilities = zip(*prob_dist.items())
    measurements = np.random.choice(states, size=num_shots, p=probabilities)
    unique, counts = np.unique(measurements, return_counts=True)
    return dict(zip(unique, counts))

#################################################################################################
def objective_value(x, w):
    # Calculate the value of the cut.
    X = np.outer(x, (1 - x))
    return np.sum(w * X)

def find_UMC_solution(qubits,graph_dict):
    
    # Create a mapping of node labels to integer indexes
    node_indices = {node: int(node) for node in graph_dict}  # Convert a string key to an integer

    w = np.zeros((qubits, qubits))

    for node, edges in graph_dict.items():
        for adjacent, attr in edges.items():
            # Use mapping to access arrays.
            u = node_indices[node]
            v = node_indices[adjacent]
            w[u, v] = attr['weight']

    # Calculate the value of the cut.
    all_partitions = itertools.product([0, 1], repeat=qubits)

    max_cut_value = 0
    max_cuts = []

    for partition in all_partitions:
        partition = np.array(partition)
        cut_value = objective_value(partition, w)
        if cut_value > max_cut_value:
            max_cut_value = cut_value
            max_cuts = [partition]
        elif cut_value == max_cut_value:
            max_cuts.append(partition)

    print(f"The value of the Unweighted Max-Cut problem is: {max_cut_value}")
    print("The corresponding grouping scheme is as follows:")
    for cut in max_cuts:
        print(cut)

    # Use the from_numpy_array function of NetworkX to create an undirected graph from the weight matrix.
    G = nx.from_numpy_array(w)

    # Node color setting, assuming that one of the maximum cutting schemes is the grouping basis.
    example_partition = max_cuts[0]
    node_colors = ['lightblue' if example_partition[i] == 0 else 'plum' for i in range(qubits)]

    folder_path = 'Final_Data'

    # Draw an image
    plt.figure(figsize=(8, 6))
    pos = nx.circular_layout(G)  # Using spring layout algorithm
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2500)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray',width=3)
    nx.draw_networkx_labels(G, pos, font_size=35, font_color='black')  # Adjust the label font size and color.
    plt.axis('off')
    
    # Save the figure
    plt.savefig(f'{folder_path}/The_Unweighted_Max-Cut_Problem.png')

    # Optionally, if you want to close the plot after saving
    plt.close()

    return max_cuts

def find_WMC_solution(qubits,graph_dict):
    
    # Create a mapping of node labels to integer indexes
    node_indices = {str(node): int(node) for node in graph_dict}  # Convert a string key to an integer

    w = np.zeros((qubits, qubits))

    for node, edges in graph_dict.items():
        for adjacent, attr in edges.items():
            # Use mapping to access arrays.
            u = node_indices[str(node)]  # Use integer node index
            v = node_indices[str(adjacent)]
            w[u, v] = attr['weight']

    # Calculate all possible groups and find the maximum cut value.
    all_partitions = itertools.product([0, 1], repeat=qubits)

    max_cut_value = 0
    max_cuts = []

    for partition in all_partitions:
        partition = np.array(partition)
        cut_value = objective_value(partition, w)
        if cut_value > max_cut_value:
            max_cut_value = cut_value
            max_cuts = [partition]
        elif cut_value == max_cut_value:
            max_cuts.append(partition)

    print(f"The value of the Weighted Max-Cut problem is: {max_cut_value}")
    print("The corresponding grouping scheme is as follows:")
    for cut in max_cuts:
        print(cut)

    # Creating an undirected graph with NetworkX
    G = nx.Graph()
    for node, edges in graph_dict.items():
        for adjacent, attr in edges.items():
            G.add_edge(str(node), str(adjacent), weight=attr['weight'])

    # Node color setting
    example_partition = max_cuts[0]
    node_colors = ['lightblue' if example_partition[i] == 0 else 'plum' for i in range(qubits)]

    # Draw a graph
    plt.figure(figsize=(8, 6))
    pos = nx.circular_layout(G)  # Set seed to ensure consistency.
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2500)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray',width=2)
    nx.draw_networkx_labels(G, pos, font_size=35, font_color='black')

    # Generate edge weight labels, and add them only once.
    edge_labels = {}
    for node, edges in graph_dict.items():
        for adjacent, attr in edges.items():
            u, v = str(node), str(adjacent)  # Ensure that the node names are consistent.
            if (v, u) not in edge_labels:  # Make sure that the weight of each edge is added only once.
                edge_labels[(u, v)] = attr['weight']

    # Calculate the midpoint position of each edge.
    label_pos = {}
    for (u, v), label in edge_labels.items():
        label_pos[(u, v)] = ((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2)

    # Draw the weight label of the edge.
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=20, font_color='lightseagreen', label_pos=0.6)
    plt.axis('off')

    folder_path = 'Final_Data'
    # Save the figure
    plt.savefig(f'{folder_path}/The_Weighted_Max-Cut_Problem.png')

    # Optionally, if you want to close the plot after saving
    plt.close()

    return max_cuts

#################################################################################################
# Auxiliary function: converting from Boolean value to spin value
def b2s(bit):
    return 1 - 2 * int(bit)  # 0 -> +1, 1 -> -1

# Energy calculation function
def energy(cfg, graph, normalize=True):
    factor = 1 / len(graph) / 4
    E = 0.25
    for a, b in graph.edges:
        E += cfg[a - 1] * cfg[b - 1] * graph[a][b]["weight"] * factor
    return E if normalize else E / factor

# Violent solution
def brutal_force(graph):
    num_nodes = graph.number_of_nodes()
    min_cost, best_case = 1.0, []
    for i in range(2**num_nodes):
        # Generate a binary bit string
        case = f"{bin(i)[2:]:0>{num_nodes}}"
        
        # Mapping a bit string to a spin configuration
        cfg = [b2s(bit) for bit in case]

        # Calculated energy
        cost = energy(cfg, graph)

        # Update the optimal solution
        gap = min_cost - cost
        if gap > 1e-6:
            min_cost = cost
            best_case = [case]
        elif abs(gap) < 1e-6:
            best_case.append(case)

    return best_case, min_cost

def find_NAE_3SAT_solution(qubits,easy_graph):
    # Print the result of violent solution
    bf_best_cases, bf_best = brutal_force(easy_graph)
    print(f"Bit strings: {bf_best_cases}")

    # Traverse all the best solutions and show them.
    print("Node status for all best solutions (node number: spin value):")
    for solution_idx, bit_string in enumerate(bf_best_cases):
        print(f"Solution {solution_idx + 1}:")
        node_states = {node: b2s(bit) for node, bit in zip(sorted(easy_graph.nodes), bit_string)}
        for node, spin in node_states.items():
            print(f"Node x{node}: Spin Value {spin}({'-> 0' if spin == +1 else '-> 1'})") # 0 -> +1, 1 -> -1
    print()

    return bf_best_cases

#################################################################################################
def draw_simulate_measurement(results, max_cuts, num_qubits):

    folder_path = 'Final_Data'

    # Convert max_cuts from binary arrays to binary strings
    max_cut_states = [''.join(str(bit) for bit in cut) for cut in max_cuts]

    # Ensure all possible states are represented in results
    full_results = {format(i, f'0{num_qubits}b'): 0 for i in range(2 ** num_qubits)}
    full_results.update(results)  # Update with actual results, overwriting zeros where applicable
    print("Full_results:")
    print(full_results)

    # Plotting the histogram of results
    plt.figure(figsize=(5*num_qubits, 6))
    bars = plt.bar(full_results.keys(), full_results.values(), color='skyblue')
    plt.xlabel('State')
    plt.ylabel('Counts')
    plt.title('Measurement Results Histogram')
    
    # Add labels above bars
    ax = plt.gca()  # Get current axis
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', color='black')

    # Color the x-axis labels based on max_cut_states
    labels = ax.get_xticklabels()  # Get x-axis labels (ticks)
    for label in labels:
        label.set_rotation(90)  # Rotate labels to vertical
        # If the label's text is in max_cut_states, color it red
        if label.get_text() in max_cut_states:
            label.set_color('coral')
        else:
            label.set_color('black')

    # Save the plot instead of showing it
    plt.savefig(f'{folder_path}/Measurement_Results_Histogram.png')
    plt.close()
