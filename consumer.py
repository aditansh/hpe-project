import os
import errno
import time

fifo_path = '/tmp/my_fifo'

# Function to read from the FIFO
def read_fifo():
    try:
        with os.fdopen(os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK), 'r') as fifo:
            while True:
                try:
                    line = fifo.readline().strip()
                    if line:
                        print(f'Received: {line}')
                        if "End Communication" in line:
                            return
                    else:
                        time.sleep(0.1)  # Avoid busy-waiting
                except BlockingIOError:
                    time.sleep(0.1)  # No data yet, wait a bit
    except FileNotFoundError:
        print("FIFO file not found. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    print("Waiting for messages in FIFO queue...")

    while True:
        try:
            if os.path.exists(fifo_path):
                read_fifo()
            else:
                print("FIFO file removed or does not exist. Exiting.")
                break
        except KeyboardInterrupt:
            print("Consumer interrupted. Exiting.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

