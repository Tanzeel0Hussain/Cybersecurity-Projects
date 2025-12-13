import re
from collections import Counter
from datetime import datetime

def analyze_logs(file_path):
    failed_ips = []
    failed_users = []

    with open(file_path, "r", errors="ignore") as f:
        lines = f.readlines()

    for line in lines:
        if "Failed password" in line:
            ip_match = re.search(r'from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)
            user_match = re.search(r'for (invalid user )?(\w+)', line)

            if ip_match:
                failed_ips.append(ip_match.group(1))
            if user_match:
                failed_users.append(user_match.group(2))

    ip_counter = Counter(failed_ips)
    user_counter = Counter(failed_users)
    return ip_counter, user_counter

def generate_report(file_path, ip_counter, user_counter):
    report_file = "reports/analysis_report.txt"
    with open(report_file, "w") as f:
        f.write(f"LOG ANALYSIS REPORT - {datetime.now()}\n\n")
        f.write("Top Suspicious IPs:\n")
        for ip, count in ip_counter.items():
            status = "SUSPICIOUS" if count >= 5 else "Normal"
            f.write(f"{ip} → {count} attempts ({status})\n")

        f.write("\nMost Targeted Users:\n")
        for user, count in user_counter.items():
            f.write(f"{user} → {count} attempts\n")
    return report_file
