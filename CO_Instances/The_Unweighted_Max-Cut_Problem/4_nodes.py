import json
import os

graph_dict = {
    0: {1: {'weight': 1.0}, 2: {'weight': 1.0}}, 
    1: {0: {'weight': 1.0}, 2: {'weight': 1.0}, 3: {'weight': 1.0}}, 
    2: {0: {'weight': 1.0}, 1: {'weight': 1.0}, 3: {'weight': 1.0}}, 
    3: {1: {'weight': 1.0}, 2: {'weight': 1.0}}}

# Get the current working directory
directory = os.getcwd()

# Create folder path
filename = '4_nodes.json'
file_path = os.path.join(directory, filename)

# Convert dictionary to JSON string and save to file.
with open(file_path, 'w') as json_file:
    json.dump(graph_dict, json_file, indent=4)

print(f"JSON file '{filename}' has been created and saved in '{directory}' directory.")