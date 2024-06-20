import os
import errno
import time
import multiprocessing
import subprocess

fifo_path = '/tmp/my_fifo'
packets_to_capture = 15

# Function to create the FIFO
def create_fifo():
    try:
        os.mkfifo(fifo_path)
        print(f"Created FIFO at {fifo_path}")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            print(f"FIFO at {fifo_path} already exists")

# Producer: Function to capture network data and write to the FIFO
def producer():
    print("Starting producer process...")
    create_fifo()
    try:
        with os.fdopen(os.open(fifo_path, os.O_WRONLY), 'w') as fifo:
            print("Capturing network data with tshark...")
            # Replace 'eth0' with the appropriate network interface for your setup
            command = ['tshark', '-i', 'wlo1', '-l', '-c', str(packets_to_capture)]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            packet_count = 0
            for line in iter(process.stdout.readline, b''):
                fifo.write(line.decode())
                fifo.flush()
                print(f"Produced: {line.strip()}")
                packet_count += 1
                if packet_count >= packets_to_capture:
                    break
                time.sleep(0.5)  # Wait 0.5 seconds before logging the next packet
            process.stdout.close()
            process.wait()
    except Exception as e:
        print(f"Producer encountered an error: {e}")
    finally:
        print("Producer process finished")

# Consumer: Function to read from the FIFO and log data
def consumer():
    print("Starting consumer process...")
    try:
        with os.fdopen(os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK), 'r') as fifo:
            with open('network_log.txt', 'a') as log_file:
                packet_count = 0
                while packet_count < packets_to_capture:
                    try:
                        line = fifo.readline().strip()
                        if line:
                            log_file.write(f"{line}\n")
                            log_file.flush()
                            print(f"Logged: {line}")
                            packet_count += 1
                        else:
                            time.sleep(0.1)  # Avoid busy-waiting
                    except BlockingIOError:
                        time.sleep(0.1)  # No data yet, wait a bit
    except FileNotFoundError:
        print("FIFO file not found. Exiting.")
    except Exception as e:
        print(f"Consumer encountered an error: {e}")
    finally:
        print("Consumer process finished")

if __name__ == "__main__":
    print("Starting main process...")
    
    # Create two child processes
    producer_process = multiprocessing.Process(target=producer)
    consumer_process = multiprocessing.Process(target=consumer)
    
    # Start the producer and consumer processes
    producer_process.start()
    consumer_process.start()
    
    # Wait for both processes to finish
    producer_process.join()
    consumer_process.join()
    
    # Clean up by removing the FIFO
    if os.path.exists(fifo_path):
        os.remove(fifo_path)
        print("FIFO file removed")

    print("Main process finished")

