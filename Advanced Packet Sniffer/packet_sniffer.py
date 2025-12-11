from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

log_file = "captured_packets.log"

def packet_callback(packet):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        proto = packet[IP].proto
        length = len(packet)

        if proto == 6:     # TCP
            protocol = "TCP"
            color = Fore.CYAN
        elif proto == 17:  # UDP
            protocol = "UDP"
            color = Fore.YELLOW
        elif proto == 1:   # ICMP
            protocol = "ICMP"
            color = Fore.GREEN
        else:
            protocol = f"Other({proto})"
            color = Fore.MAGENTA

        log_text = f"{timestamp} | {protocol} | {src} → {dst} | Size: {length}"

        print(color + log_text)

        with open(log_file, "a") as f:
            f.write(log_text + "\n")

print(Fore.LIGHTBLUE_EX + """
=========================================
     ADVANCED PACKET SNIFFER - SCAPY
=========================================
""")

print("Starting live packet capture...\n")

sniff(prn=packet_callback, store=False)