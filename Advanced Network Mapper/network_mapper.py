import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

PORT_RANGE = range(20, 1025)
THREADS = 100
OUTPUT_FILE = "network_scan_results.txt"
TIMEOUT = 0.5


def banner():
    print(Fore.CYAN + "=== ADVANCED NETWORK MAPPER ===" + Style.RESET_ALL)
    print("Use only on networks you own or are explicitly authorized to assess.\n")


def is_host_alive(ip):
    system = platform.system().lower()
    if system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        command = ["ping", "-c", "1", "-W", "1", ip]

    try:
        return subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
    except OSError:
        return False


def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            if sock.connect_ex((ip, port)) != 0:
                return None

        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "Unknown"
        return port, service
    except OSError:
        return None


def scan_host(ip):
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(lambda port: scan_port(ip, port), PORT_RANGE)
        return [result for result in results if result]


def save_results(ip, ports):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
        file.write(f"\nHost: {ip}\n")
        for port, service in ports:
            file.write(f"Port {port} | Service: {service}\n")


def validate_prefix(prefix):
    parts = prefix.rstrip(".").split(".")
    if len(parts) != 3:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def main():
    banner()
    target = input(Fore.YELLOW + "Enter /24 network prefix (example: 192.168.1.): ").strip()

    if not validate_prefix(target):
        print(Fore.RED + "[!] Invalid /24 network prefix.")
        return

    target = target.rstrip(".") + "."
    open(OUTPUT_FILE, "w", encoding="utf-8").close()
    start_time = datetime.now()

    print(Fore.CYAN + "\n[+] Discovering live hosts...\n")

    for i in range(1, 255):
        ip = f"{target}{i}"
        if not is_host_alive(ip):
            continue

        print(Fore.GREEN + f"[✓] Host Alive: {ip}")
        ports = scan_host(ip)
        if ports:
            for port, service in ports:
                print(Fore.MAGENTA + f"    └─ Port {port} OPEN ({service})")
            save_results(ip, ports)
        else:
            print(Fore.YELLOW + "    └─ No open ports found in configured range")

    print(Fore.CYAN + f"\n[✔] Scan completed in {datetime.now() - start_time}")
    print(Fore.CYAN + f"[✔] Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
