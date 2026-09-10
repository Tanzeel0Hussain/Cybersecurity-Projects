import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP Proxy",
}

SECURITY_NOTES = {
    21: "FTP may expose credentials if used without encryption.",
    23: "Telnet sends traffic in plaintext and should be avoided.",
    80: "HTTP is unencrypted; prefer HTTPS for sensitive traffic.",
    3306: "Database ports should normally be restricted from public access.",
    3389: "RDP should be protected with MFA, firewall rules, and strong authentication.",
}

MAX_WORKERS = 100
TIMEOUT = 0.6


def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            if sock.connect_ex((ip, port)) != 0:
                return None

        service = COMMON_SERVICES.get(port, "Unknown Service")
        note = SECURITY_NOTES.get(port)
        return port, service, note
    except OSError:
        return None


def main():
    print("\n=== PORT SCANNER ===")
    target = input("Enter target IP/hostname: ").strip()

    try:
        ip = socket.gethostbyname(target)
        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
    except (socket.gaierror, ValueError):
        print("[!] Invalid hostname/IP or port value.")
        return

    if not (1 <= start_port <= end_port <= 65535):
        print("[!] Port range must be between 1 and 65535.")
        return

    print(f"\nScanning {ip} from port {start_port} to {end_port}...\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
        results = []
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    for port, service, note in sorted(results):
        print(f"[OPEN] Port {port} ({service})")
        if note:
            print(f"       Security note: {note}")

    print(f"\nScan complete. {len(results)} open port(s) found.")
    print("Use only on systems you own or are explicitly authorized to test.\n")


if __name__ == "__main__":
    main()
