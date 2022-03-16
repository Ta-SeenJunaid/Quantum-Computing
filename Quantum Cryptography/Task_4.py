from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, IBMQ, BasicAer, execute

alice_key = ''
bob_key = ''
eve_key   = ''

check_interval=10
key_length=100

eve_listening = 1

q = QuantumRegister(4, "q")
c = ClassicalRegister(6, "c")

circuit = QuantumCircuit(q, c)

circuit.h(q[0])
circuit.h(q[1])
circuit.measure(q[0], c[0])
circuit.measure(q[1], c[1])
circuit.ch(q[1], q[0])
circuit.barrier()

if eve_listening:
    circuit.h(q[3])
    circuit.measure(q[3], c[4])

    circuit.ch(q[3], q[0])
    circuit.measure(q[0], c[5])
    circuit.ch(q[3], q[0])

circuit.barrier()

circuit.h(q[2])
circuit.measure(q[2], c[2])
circuit.ch(q[2], q[0])

circuit.measure(q[0], c[3])

print(circuit)

backend = BasicAer.get_backend("qasm_simulator")

number_transmissions = 0
number_success = 0
number_failure = 0
unchecked_bits = 0

while len(alice_key) < key_length:
    job = execute(circuit, backend=backend, shots=1)
    number_transmissions += 1

    result = job.result()
    state = list(result.get_counts(circuit).keys())[0]

    b = int(state[3])
    a = int(state[0])
    ap = int(state[1])
    bp = int(state[2])
    eve = int(state[0])
    evep = int(state[1])

    if ap==bp:
        unchecked_bits += 1
        if unchecked_bits == check_interval and check_interval > 0:
            unchecked_bits = 0
            if(a!=b):
                number_failure +=1
            else:
                number_success +=1
        else:
            alice_key += str(a)
            bob_key += str(b)

            if evep == ap:
                eve_key += str(eve)
            else:
                eve_key += 'x'


print('Alice\'s key: ', alice_key)
print('Bob\'s   key: ', bob_key)
print('Eve\'s   key: ', eve_key)

if alice_key==bob_key and (alice_key == eve_key or eve_listening == 0):
    print('All keys are confirmed to be the same.')
else:
    print('Not all keys are identical. This should not happen unless somebody is listening to the communication!')

usage_rate = 100.0 * key_length / (number_transmissions)

print(str(usage_rate) + '% of the transmitted Qubits could be used for key creation.')

error_rate = 100 * number_failure / (number_failure + number_success)

print('The error rate of the channel is '+ str(error_rate) + '%')