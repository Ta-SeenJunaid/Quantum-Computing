from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, BasicAer, execute

q = QuantumRegister(1, "q")
c = ClassicalRegister(1, "c")

circuit = QuantumCircuit(q, c, name="random_numbers")
circuit.h(q[0])
circuit.measure(q[0], c[0])
print(circuit)

backend = BasicAer.get_backend("qasm_simulator")
job = execute(circuit, backend=backend, shots=1024)

result = job.result()
print(result.get_counts(circuit))
