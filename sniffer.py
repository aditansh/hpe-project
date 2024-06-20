from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

# Capture packets and save to a variable
def capture_packets(interface, count):
    packets = sniff(iface=interface, count=count, prn=packet_callback)
    return packets

if __name__ == "__main__":
    interface = "wlo1"  # Replace with your network interface
    count = 10  # Number of packets to capture
    
    captured_packets = capture_packets(interface, count)
    
    # Do something with the captured packets
    # For example, print the summary of all captured packets
    for packet in captured_packets:
        print(packet.summary())

