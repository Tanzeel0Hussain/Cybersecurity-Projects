import re
from collections import Counter
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ---------------- CONFIG ---------------- #
LOG_FILE = "auth.log"
OUTPUT_FILE = "security_report.txt"
FAILED_THRESHOLD = 5
# ---------------------------------------- #

def banner():
    print(Fore.CYAN + """
██╗      ██████╗  ██████╗     █████╗ ███╗   ██╗ █████╗ ██╗     
██║     ██╔═══██╗██╔════╝    ██╔══██╗████╗  ██║██╔══██╗██║     
██║     ██║   ██║██║  ███╗   ███████║██╔██╗ ██║███████║██║     
██║     ██║   ██║██║   ██║   ██╔══██║██║╚██╗██║██╔══██║██║     
███████╗╚██████╔╝╚██████╔╝   ██║  ██║██║ ╚████║██║  ██║███████╗
╚══════╝ ╚═════╝  ╚═════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
    """ + Style.RESET_ALL)

def load_logs():
    with open(LOG_FILE, "r", errors="ignore") as file:
        return file.readlines()

def analyze_logs(lines):
    failed_ips = []
    failed_users = []

    for line in lines:
        if "Failed password" in line:
            ip_match = re.search(r'from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)
            user_match = re.search(r'for (invalid user )?(\w+)', line)

            if ip_match:
                failed_ips.append(ip_match.group(1))
            if user_match:
                failed_users.append(user_match.group(2))

    return Counter(failed_ips), Counter(failed_users)

def generate_report(ip_counter, user_counter):
    with open(OUTPUT_FILE, "w") as file:
        file.write("=== SECURITY LOG ANALYSIS REPORT ===\n")
        file.write(f"Generated on: {datetime.now()}\n\n")

        file.write("Top Suspicious IP Addresses:\n")
        for ip, count in ip_counter.items():
            status = "SUSPICIOUS" if count >= FAILED_THRESHOLD else "Normal"
            file.write(f"{ip} → {count} attempts ({status})\n")

        file.write("\nMost Targeted Usernames:\n")
        for user, count in user_counter.items():
            file.write(f"{user} → {count} attempts\n")

def display_results(ip_counter, user_counter):
    print(Fore.CYAN + "\n[+] Suspicious IP Activity:\n")
    for ip, count in ip_counter.items():
        if count >= FAILED_THRESHOLD:
            print(Fore.RED + f"[!] {ip} → {count} failed attempts")
        else:
            print(Fore.YELLOW + f"[•] {ip} → {count} attempts")

    print(Fore.CYAN + "\n[+] Targeted Usernames:\n")
    for user, count in user_counter.items():
        print(Fore.MAGENTA + f"{user} → {count} attempts")

def main():
    banner()
    print(Fore.CYAN + "[*] Loading log file...")

    logs = load_logs()
    ip_counter, user_counter = analyze_logs(logs)

    display_results(ip_counter, user_counter)
    generate_report(ip_counter, user_counter)

    print(Fore.GREEN + f"\n[✔] Analysis complete")
    print(Fore.GREEN + f"[✔] Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
