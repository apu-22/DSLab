"""
Lab 2: Multi-threaded Client
----------------------------
Fires N near-simultaneous requests at the server.
"""

import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 65002
N = 100  # number of "simultaneous" clients


def worker(i):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(f"request-{i}".encode())
        reply = s.recv(1024).decode()
        print(f"[CLIENT {i}] {reply}")


def main():
    start = time.time()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"\nAll {N} requests completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
