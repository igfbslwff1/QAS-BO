from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.second_q.formats.molecule_info import MoleculeInfo
from qiskit_nature.second_q.transformers import FreezeCoreTransformer

def Chemical_molecule(FreezeCore, Mapper, atoms, coords, charge, multiplicity, remove_orbitals):
    if FreezeCore == 'No'  and Mapper == 'JordanWigner':
        # Define Hamiltonian of quantum system
        molecule = MoleculeInfo(atoms, coords, charge, multiplicity)
        driver = PySCFDriver.from_molecule(molecule, basis="sto3g")
        problem = driver.run()
        hamiltonian = problem.hamiltonian.second_q_op()
        mapper=JordanWignerMapper()
        qubit_op = mapper.map(hamiltonian)

    elif FreezeCore == 'No' and Mapper == 'Parity':
        # Define Hamiltonian of quantum system
        molecule = MoleculeInfo(atoms, coords, charge, multiplicity)
        driver = PySCFDriver.from_molecule(molecule, basis="sto3g")
        problem = driver.run()
        hamiltonian = problem.hamiltonian.second_q_op()
        mapper=ParityMapper(num_particles=problem.num_particles)
        qubit_op = mapper.map(hamiltonian)

    elif FreezeCore == 'Yes' and Mapper == 'Parity':
        # Define Hamiltonian of quantum system
        molecule = MoleculeInfo(atoms, coords, charge, multiplicity)
        driver = PySCFDriver.from_molecule(molecule, basis="sto3g")
        problem = driver.run()

        transformer = FreezeCoreTransformer(freeze_core=False, remove_orbitals=remove_orbitals)
        problem = transformer.transform(problem)

        hamiltonian = problem.hamiltonian.second_q_op()
        mapper=ParityMapper(num_particles=problem.num_particles)
        qubit_op = mapper.map(hamiltonian)

    elif FreezeCore == 'Yes' and Mapper == 'JordanWigner':
        # Define Hamiltonian of quantum system
        molecule = MoleculeInfo(atoms, coords, charge, multiplicity)
        driver = PySCFDriver.from_molecule(molecule, basis="sto3g")
        problem = driver.run()

        transformer = FreezeCoreTransformer(freeze_core=False, remove_orbitals=remove_orbitals)
        problem = transformer.transform(problem)

        hamiltonian = problem.hamiltonian.second_q_op()
        mapper=JordanWignerMapper()
        qubit_op = mapper.map(hamiltonian)

    return qubit_op
