import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# ---------------- CONFIG ---------------- #
PORT_RANGE = range(20, 1025)
THREADS = 100
OUTPUT_FILE = "network_scan_results.txt"
# ---------------------------------------- #

def banner():
    print(Fore.CYAN + """
███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██║ ██╗ 
██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
    """ + Style.RESET_ALL)

def is_host_alive(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            return port, service
        sock.close()
    except:
        pass
    return None

def scan_host(ip):
    open_ports = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(lambda p: scan_port(ip, p), PORT_RANGE)
        for res in results:
            if res:
                open_ports.append(res)
    return open_ports

def save_results(ip, ports):
    with open(OUTPUT_FILE, "a") as file:
        file.write(f"\nHost: {ip}\n")
        for port, service in ports:
            file.write(f"Port {port} | Service: {service}\n")

def main():
    banner()
    target = input(Fore.YELLOW + "Enter network (example: 192.168.1.): ")

    print(Fore.CYAN + "\n[+] Scanning live hosts...\n")

    start_time = datetime.now()

    for i in range(1, 255):
        ip = f"{target}{i}"
        if is_host_alive(ip):
            print(Fore.GREEN + f"[✓] Host Alive: {ip}")
            ports = scan_host(ip)
            if ports:
                for port, service in ports:
                    print(Fore.MAGENTA + f"    └─ Port {port} OPEN ({service})")
                save_results(ip, ports)
            else:
                print(Fore.YELLOW + "    └─ No open ports found")

    end_time = datetime.now()
    print(Fore.CYAN + f"\n[✔] Scan completed in {end_time - start_time}")
    print(Fore.CYAN + f"[✔] Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()