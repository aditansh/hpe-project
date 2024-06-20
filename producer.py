import os
import errno
import time
from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

# Capture packets and save to a variable
def capture_packets(interface, count):
    packets = sniff(iface=interface, count=count, prn=packet_callback)
    return packets


fifo_path = '/tmp/my_fifo'

# Create the FIFO if it doesn't exist
try:
    os.mkfifo(fifo_path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Function to write to the FIFO
def write_fifo(text: str):
    with os.fdopen(os.open(fifo_path, os.O_WRONLY), 'w') as fifo:
        fifo.write(f'{text}\n')
        print("Message written to FIFO")

# Example usage
if __name__ == "__main__":
    # Writing to the FIFO

    interface = "wlo1"  # Replace with your network interface
    count = 10  # Number of packets to capture
    
    captured_packets = capture_packets(interface, count)

    print("Captured all packets. Sleeping for 5 seconds.")

    time.sleep(5)
    
    # Do something with the captured packets
    # For example, print the summary of all captured packets
    for packet in captured_packets:
        write_fifo(packet.summary())
    print("All packets written to FIFO file. Ending communications in 5 seconds.")
    time.sleep(5)
    write_fifo("End Communication")

    # Manual read and write packet summary
    # text = "continue"
    # while text:
        # text = str(input("Write something into the fifo queue. Leave it blank to quit:\n"))
        # write_fifo(text)

    # Clean up by removing the FIFO
    os.remove(fifo_path)
    print("FIFO file removed")

