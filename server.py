#!/usr/bin/env python3
import socket
import time

# Configure the server to listen on all interfaces and a specified port.
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5001  # Port to listen on


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

            # Keep reading data until the client signals EOF (empty read)
            while True:
                data = conn.recv(4096)  # Receive in 4KB chunks
                if not data:
                    break
                total_received += len(data)

            end_time = time.time()
            elapsed = end_time - start_time
            throughput = total_received / elapsed if elapsed > 0 else 0

            print(f"Received {total_received} bytes in {elapsed:.2f} seconds.")
            print(f"Throughput: {throughput / 1024:.2f} KB/s")

            # Send an acknowledgment back to the client
            conn.sendall(b"ACK")


if __name__ == "__main__":
    start_server()
