"""
Lab 2: Multi-threaded Client Server Model
------------------------------------------
The dispatcher accepts every connection and immediately starts
a new worker thread for each client.
"""

import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 65002


def handle_client(conn, addr):
    with conn:
        request = conn.recv(1024).decode()

        print(f"[WORKER-{threading.get_ident()}] Working on {addr}")
        time.sleep(2)  # simulate slow work

        reply = f"Processed '{request}' by worker thread {threading.get_ident()}"
        conn.sendall(reply.encode())

        print(f"[WORKER-{threading.get_ident()}] Done with {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        print(f"[DISPATCHER] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            print(f"[DISPATCHER] Accepted {addr}, spawning worker thread")

            worker = threading.Thread(
                target=handle_client,
                args=(conn, addr)
            )
            worker.start()


if __name__ == "__main__":
    main()
