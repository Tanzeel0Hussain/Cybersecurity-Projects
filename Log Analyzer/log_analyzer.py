import argparse
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from colorama import Fore, init

init(autoreset=True)

FAILED_THRESHOLD = 5
DEFAULT_OUTPUT = "security_report.txt"


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze authorized SSH/authentication logs for failed login patterns")
    parser.add_argument("logfile", nargs="?", default="sample_auth.log", help="Path to auth log (default: sample_auth.log)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Report output file")
    parser.add_argument("--threshold", type=int, default=FAILED_THRESHOLD, help="Failed-attempt threshold for suspicious activity")
    return parser.parse_args()


def load_logs(path):
    return Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()


def analyze_logs(lines):
    failed_ips = []
    failed_users = []

    for line in lines:
        if "Failed password" not in line:
            continue

        ip_match = re.search(r"from ([0-9]+(?:\.[0-9]+){3})", line)
        user_match = re.search(r"for (?:invalid user )?([^\s]+)", line)

        if ip_match:
            failed_ips.append(ip_match.group(1))
        if user_match:
            failed_users.append(user_match.group(1))

    return Counter(failed_ips), Counter(failed_users)


def generate_report(ip_counter, user_counter, output_file, threshold):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("=== SECURITY LOG ANALYSIS REPORT ===\n")
        file.write(f"Generated on: {datetime.now().isoformat(timespec='seconds')}\n\n")
        file.write("Suspicious IP Activity:\n")
        if not ip_counter:
            file.write("No failed-login IP addresses detected.\n")
        for ip, count in ip_counter.most_common():
            status = "SUSPICIOUS" if count >= threshold else "Observed"
            file.write(f"{ip} -> {count} attempts ({status})\n")

        file.write("\nTargeted Usernames:\n")
        if not user_counter:
            file.write("No targeted usernames detected.\n")
        for user, count in user_counter.most_common():
            file.write(f"{user} -> {count} attempts\n")


def display_results(ip_counter, user_counter, threshold):
    print(Fore.CYAN + "\n[+] Failed-login IP activity:\n")
    if not ip_counter:
        print(Fore.GREEN + "No failed-login IP addresses detected.")
    for ip, count in ip_counter.most_common():
        color = Fore.RED if count >= threshold else Fore.YELLOW
        print(color + f"{ip} -> {count} failed attempt(s)")

    print(Fore.CYAN + "\n[+] Targeted usernames:\n")
    if not user_counter:
        print(Fore.GREEN + "No usernames detected.")
    for user, count in user_counter.most_common():
        print(Fore.MAGENTA + f"{user} -> {count} attempt(s)")


def main():
    args = parse_args()
    if args.threshold < 1:
        raise SystemExit("--threshold must be at least 1")

    path = Path(args.logfile)
    if not path.is_file():
        print(Fore.RED + f"[!] Log file not found: {path}")
        print("Provide a path, e.g. python log_analyzer.py /var/log/auth.log")
        return

    print(Fore.CYAN + "=== SECURITY LOG ANALYZER ===")
    logs = load_logs(path)
    ip_counter, user_counter = analyze_logs(logs)
    display_results(ip_counter, user_counter, args.threshold)
    generate_report(ip_counter, user_counter, args.output, args.threshold)
    print(Fore.GREEN + f"\n[✔] Report saved to {args.output}")


if __name__ == "__main__":
    main()
