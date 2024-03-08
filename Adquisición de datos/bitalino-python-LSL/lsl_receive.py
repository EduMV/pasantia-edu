# Imports
from pylsl import StreamInlet, resolve_stream

# Resolve an available OpenSignals stream
print("# Looking for an available OpenSignals stream...")
os_stream = resolve_stream("name", "OpenSignals")

# Create an inlet to receive signal samples from the stream
inlet = StreamInlet(os_stream[0])


while True: # Receive samples
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)
    print("a")
