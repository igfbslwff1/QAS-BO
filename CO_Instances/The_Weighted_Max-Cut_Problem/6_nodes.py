import json
import os

graph_dict = {
    0: {1: {'weight': 3}, 2: {'weight': 2}, 3: {'weight': 6}, 4: {'weight': 1}, 5: {'weight': 4}}, 
    1: {0: {'weight': 3}, 2: {'weight': 5}, 3: {'weight': 7}, 4: {'weight': 2}, 5: {'weight': 1}}, 
    2: {0: {'weight': 2}, 1: {'weight': 5}, 3: {'weight': 4}, 4: {'weight': 3}, 5: {'weight': 6}}, 
    3: {0: {'weight': 6}, 1: {'weight': 7}, 2: {'weight': 4}, 4: {'weight': 5}, 5: {'weight': 2}}, 
    4: {0: {'weight': 1}, 1: {'weight': 2}, 2: {'weight': 3}, 3: {'weight': 5}, 5: {'weight': 8}}, 
    5: {0: {'weight': 4}, 1: {'weight': 1}, 2: {'weight': 6}, 3: {'weight': 2}, 4: {'weight': 8}}
}

# Get the current working directory
directory = os.getcwd()

# Create folder path
filename = '6_nodes.json'
file_path = os.path.join(directory, filename)

# Convert dictionary to JSON string and save to file.
with open(file_path, 'w') as json_file:
    json.dump(graph_dict, json_file, indent=4)

print(f"JSON file '{filename}' has been created and saved in '{directory}' directory.")