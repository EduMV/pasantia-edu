from pylsl import StreamInlet, resolve_stream
import time
import numpy as np

# Resolve an available OpenSignals stream
print("# Looking for an available OpenSignals stream...")
os_stream = resolve_stream("name", "OpenSignals")

# Create an inlet to receive signal samples from the stream
inlet = StreamInlet(os_stream[0])

buffer = []
ts_buffer = []

start_time = time.time()
while (time.time() - start_time) < 5:  # Receive samples for 5 seconds
    samples, timestamps = inlet.pull_chunk()
    if samples:  # Verifica si la lista no está vacía
        samples_array = np.array(samples)  
        last_values = samples_array[:, -1] 
        buffer.extend(last_values.tolist()) 
        ts_buffer.extend(timestamps)
        print(f"Añadido {len(last_values)} muestras al buffer. Total muestras en buffer: {len(buffer)}")
    else:
        print("No hay datos nuevos.")

print(f"Total muestras recibidas en 5 segundos: {len(buffer)}")
print(ts_buffer)
print(len(ts_buffer))


