"""
Lab 2a: Limiting the Worker Pool
--------------------------------
The dispatcher still accepts every connection immediately,
but only MAX_WORKERS worker threads may be doing their
2-second simulated work at the same time.

Extra clients are accepted right away, but their worker threads
wait on the semaphore until a slot becomes available.
"""

import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 65002
MAX_WORKERS = 2

# At most MAX_WORKERS threads can hold a permit at once.
worker_slots = threading.Semaphore(MAX_WORKERS)


def handle_client(conn, addr):
    """Runs inside its own worker thread."""
    with conn:
        request = conn.recv(1024).decode()

        print(f"[WORKER-{threading.get_ident()}] Waiting for a free slot ({addr})")

        # Blocks here if two workers are already doing the slow work.
        with worker_slots:
            print(f"[WORKER-{threading.get_ident()}] Got a slot, working on {addr}")

            time.sleep(2)  # simulate slow work

            reply = f"Processed '{request}' by worker thread {threading.get_ident()}"
            conn.sendall(reply.encode())

            print(f"[WORKER-{threading.get_ident()}] Done with {addr}, releasing slot")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        print(
            f"[DISPATCHER] Listening on {HOST}:{PORT} "
            f"(max {MAX_WORKERS} concurrent workers)"
        )

        while True:
            # IMPORTANT: accept() is unchanged and never waits for a worker slot.
            conn, addr = server_socket.accept()

            print(f"[DISPATCHER] Accepted {addr}, spawning worker thread")

            worker = threading.Thread(
                target=handle_client,
                args=(conn, addr)
            )
            worker.start()


if __name__ == "__main__":
    main()
