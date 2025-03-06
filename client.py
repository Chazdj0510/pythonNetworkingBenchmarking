#!/usr/bin/env python3
import socket
import time
import hmac
import hashlib

# Set the server address and port (adjust if running on a different machine)
HOST = '127.0.0.1'  # Server IP address
PORT = 5001  # Server port
SECRET_KEY = b"supersecretkey123" # Shared secret for HMAC

def generate_hmac(data):
    """Generate HMAC for the given data."""
    return hmac.new(SECRET_KEY, data, hashlib.sha256).digest()


def run_client():
    # Benchmark settings:
    message_size = 1024 * 1024  # 1 MB per message
    num_messages = 100  # Total of 10 messages
    total_bytes = message_size * num_messages
    data = b'a' * message_size  # Create a 1 MB block of data
    hmac_value = generate_hmac(data)  # Compute HMAC

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Start timer for the benchmark
        start_time = time.time()

        # Send the data in a loop
        for i in range(num_messages):
            # Generate HMAC and append it to the message
            client_socket.sendall(data)  # Send actual data
            client_socket.sendall(hmac_value)  # Send HMAC
            print(f"Sent message {i + 1}/{num_messages}")

        # Shutdown the sending side to indicate completion
        client_socket.shutdown(socket.SHUT_WR)

        # Optionally, wait for an acknowledgment from the server
        ack = client_socket.recv(1024)
        print("Received acknowledgment:", ack.decode())

        end_time = time.time()
        elapsed = end_time - start_time
        throughput = total_bytes / elapsed if elapsed > 0 else 0

        print(f"Sent {total_bytes} bytes in {elapsed:.2f} seconds.")
        print(f"Throughput: {throughput / 1024:.2f} KB/s")


if __name__ == "__main__":
    run_client()

