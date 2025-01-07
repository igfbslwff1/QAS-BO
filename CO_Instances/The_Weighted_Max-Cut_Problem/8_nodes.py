import json
import os

graph_dict ={
    0: {1: {'weight': 3}, 4: {'weight': 5}}, 
    1: {0: {'weight': 3}, 2: {'weight': 4}}, 
    2: {1: {'weight': 4}, 3: {'weight': 6}}, 
    3: {2: {'weight': 6}, 4: {'weight': 2}}, 
    4: {0: {'weight': 5}, 3: {'weight': 2}, 5: {'weight': 7}}, 
    5: {4: {'weight': 7}, 6: {'weight': 1}}, 
    6: {5: {'weight': 1}, 7: {'weight': 3}}, 
    7: {6: {'weight': 3}}
}

# Get the current working directory
directory = os.getcwd()

# Create folder path
filename = '8_nodes.json'
file_path = os.path.join(directory, filename)

# Convert dictionary to JSON string and save to file.
with open(file_path, 'w') as json_file:
    json.dump(graph_dict, json_file, indent=4)

print(f"JSON file '{filename}' has been created and saved in '{directory}' directory.")