import argparse
from ast import literal_eval
import json
import numpy as np
import ast

from sub_main import sub

def parse_orbitals(input_string):
    """Parse and remove track parameters, allowing input as' None' or integer list."""
    if input_string.lower() == 'none':
        return None
    return list(map(int, input_string.split(',')))

def parse_atoms(input_string):
    """Parses the atomic list, separated by commas."""
    return [atom.strip() for atom in input_string.split(',')]

def parse_coords(input_string):
    """List of security resolution coordinates."""
    try:
        return literal_eval(input_string)
    except SyntaxError as e:
        raise argparse.ArgumentTypeError(f"Invalid coordinate format: {input_string}") from e

def parse_args():
    """Set and parse command line parameters."""
    parser = argparse.ArgumentParser(description='Run quantum algorithms for specific problems with various settings.')

    parser.add_argument('--problem', type=str, choices=['Quantum Chemistry Ground State Energy Estimation', 'The Unweighted Max-Cut Problem','The Weighted Max-Cut Problem','Not-All-Equal 3-Satisfiability','Simulation of Arbitrary Quantum States'],
                        help='Choose either Quantum Chemistry Ground State Energy Estimation, The Unweighted Max-Cut Problem, The Weighted Max-Cut Problem or Simulation of Arbitrary Quantum States.')
    
    parser.add_argument('--freeze_core', type=str, default=None, choices=['Yes', 'No'],
                        help='Specify whether to freeze core electrons: Yes or No.')
    parser.add_argument('--mapper', type=str, default=None, choices=['Parity', 'JordanWigner'],
                        help='Specify the type of qubit mapper: Parity or JordanWigner.')
    parser.add_argument('--atoms', type=parse_atoms, default=None,
                        help='List of atom symbols, e.g., "H,O".')
    parser.add_argument('--coords', type=parse_coords, default=None,
                        help='List of tuples representing coordinates of atoms, e.g., "[(0.0, 0.0, 0.0), (0.0, 0.0, 1.595)]".')
    parser.add_argument('--charge', type=int, default=None, help='Charge of the molecule.')
    parser.add_argument('--multiplicity', type=int, default=None, help='Multiplicity of the molecule.')
    parser.add_argument('--remove_orbitals', type=parse_orbitals, default=None,
                        help='List of orbitals to remove, e.g., "0,4,5", or "None" if no orbitals should be removed.')
    
    parser.add_argument('--qubits', type=int, help='Number of qubits.')
    parser.add_argument('--depths', type=int, help='Number of circuit depths.')
    parser.add_argument('--internal_cycles', type=int, help='Number of internal optimization cycles.')
    parser.add_argument('--external_cycles', type=int, help='Number of external optimization cycles.')

    parser.add_argument("--graph_dict", type=str, default=None, help="Graph weights as a JSON string")

    parser.add_argument("--clause", type=str, default=None, help="Not-all-equal 3-satisfiability (e.g., [[1, 2, 3], [1, -2, 3], [1, 2, -3]])")

    args = parser.parse_args()
    return args


def main():
    """Main function, parsing parameters and displaying configuration."""
    args = parse_args()
    print("Running configuration:")
    print(args)

    problem=args.problem

    atoms=args.atoms
    coords=args.coords
    charge=args.charge
    multiplicity=args.multiplicity

    remove_orbitals=args.remove_orbitals
    FreezeCore=args.freeze_core
    Mapper=args.mapper

    qubits=args.qubits
    depths=args.depths

    Number_of_internal_cycles=args.internal_cycles
    Number_of_external_cycles=args.external_cycles

    # Parsing JSON dictionary
    if args.graph_dict:
        try:
            w = json.loads(args.graph_dict)
            print("Loaded graph weights:")
            print(w)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            w = None
    else:
        print("No graph weights provided, using default values or skipping.")
        w = None

    if args.clause is not None:
        clause = ast.literal_eval(args.clause)
    else:
        clause = None

    sub(problem, qubits,depths,FreezeCore, Mapper, atoms, coords, charge, multiplicity, remove_orbitals, Number_of_internal_cycles, Number_of_external_cycles, w, clause)

if __name__ == "__main__":
    main()
