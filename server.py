#!/usr/bin/env python3
import socket
import time
import hmac
import hashlib

# Configure the server to listen on all interfaces and a specified port.
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5001  # Port to listen on
SECRET_KEY = b"supersecretkey123" # Shared secret for HMAC

def verify_hmac(received_hmac, data):
    """Verify HMAC integrity."""
    expected_hmac = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
    return hmac.compare_digest(expected_hmac, received_hmac)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = server_socket.accept()
        with conn:
            print('Connected by', addr)
            total_received = 0
            start_time = time.time()

            data_chunks = []

            # Keep reading data until the client signals EOF (empty read)
            while True:
                chunk = conn.recv(4096)  # Receive in 4KB chunks
                if not chunk:
                    break
                data_chunks.append(chunk)
                total_received += len(chunk)

            # Extract HMAC (first 32 bytes) and message
            data = b''.join(data_chunks[:-1])  # All except last chunk (HMAC)
            received_hmac = data_chunks[-1]  # Last chunk is the HMAC

            # Verify HMAC
            if verify_hmac(received_hmac, data):
                print(f"Received {total_received} bytes successfully.")
                conn.sendall(b"ACK")  # Send acknowledgment
            else:
                print("HMAC verification failed! Data integrity compromised.")

                
            end_time = time.time()
            elapsed = end_time - start_time
            throughput = total_received / elapsed if elapsed > 0 else 0

            print(f"Throughput: {throughput / 1024:.2f} KB/s")



if __name__ == "__main__":
    start_server()
