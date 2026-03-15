from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# 1. LOGIN
MY_TOKEN = 'enter your token'

service = QiskitRuntimeService(channel="ibm_quantum_platform", token=MY_TOKEN)

# 2. CHOOSE BACKEND
backend = service.least_busy(simulator=False, operational=True)
print(f"Targeting: {backend.name}")

# 3. YOUR CIRCUIT (Modified for 4 Qubits)
qc = QuantumCircuit(4) # Initialize with 4 qubits
qc.h(0)                # Put the first qubit in superposition
qc.cx(0, 1)            # Entangle 0 and 1
qc.cx(1, 2)            # Entangle 1 and 2
qc.cx(2, 3)            # Entangle 2 and 3
qc.measure_all()       # Measure all 4 qubits

# 4. TRANSPILE
transpiled_qc = transpile(qc, backend=backend)

# 5. RUN
sampler = Sampler(backend)
job = sampler.run([transpiled_qc]) 
print(f"Job ID: {job.job_id()}")

# 6. RESULTS
result = job.result()
counts = result[0].data.meas.get_counts()
print(f"Results: {counts}")
plot_histogram(counts)
plt.show()
