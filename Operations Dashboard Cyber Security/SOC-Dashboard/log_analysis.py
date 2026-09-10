import re
from collections import Counter
from datetime import datetime


def analyze_logs(file_path):
    failed_ips = []
    failed_users = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if "Failed password" not in line:
                continue

            ip_match = re.search(r"from ([0-9]+(?:\.[0-9]+){3})", line)
            user_match = re.search(r"for (?:invalid user )?([^\s]+)", line)

            if ip_match:
                failed_ips.append(ip_match.group(1))
            if user_match:
                failed_users.append(user_match.group(1))

    return Counter(failed_ips), Counter(failed_users)


def generate_report(file_path, ip_counter, user_counter, report_file="reports/analysis_report.txt"):
    with open(report_file, "w", encoding="utf-8") as file:
        file.write("=== LOG ANALYSIS REPORT ===\n")
        file.write(f"Source: {file_path}\n")
        file.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n")

        file.write("Suspicious IP Activity:\n")
        if not ip_counter:
            file.write("No failed-login IP activity detected.\n")
        for ip, count in ip_counter.most_common():
            status = "SUSPICIOUS" if count >= 5 else "Observed"
            file.write(f"{ip} -> {count} attempts ({status})\n")

        file.write("\nTargeted Users:\n")
        if not user_counter:
            file.write("No targeted usernames detected.\n")
        for user, count in user_counter.most_common():
            file.write(f"{user} -> {count} attempts\n")

    return report_file
