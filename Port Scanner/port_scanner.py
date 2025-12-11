import socket
import threading

# Dictionary of common ports and their known services
COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP Proxy",
}

# Very small vulnerability list (demo purpose only)
VULNERABILITIES = {
    21: "Anonymous FTP login possible",
    22: "Weak SSH passwords risk",
    23: "Telnet transmits data in plain text (NOT secure)",
    80: "Check for outdated Apache/Nginx versions",
    3306: "MySQL default credentials vulnerability",
    3389: "Weak RDP protection risk"
}

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))

        if result == 0:
            service = COMMON_SERVICES.get(port, "Unknown Service")
            print(f"[OPEN] Port {port} ({service})")

            banner = grab_banner(ip, port)
            if banner:
                print(f"       Banner: {banner}")

            if port in VULNERABILITIES:
                print(f"        Possible Vulnerability: {VULNERABILITIES[port]}")

        sock.close()
    except:
        pass

def main():
    print("\n=== ADVANCED PORT SCANNER ===")
    ip = input("Enter target IP: ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nScanning {ip} from port {start_port} to {end_port}...\n")

    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    print("\n Scan Complete!\n")

if __name__ == "__main__":
    main()