from collections import Counter

# Threat thresholds
LOW_THRESHOLD = 1
MEDIUM_THRESHOLD = 3
HIGH_THRESHOLD = 5

def calculate_threat(ip_counter, user_counter):
    threat_summary = {"IPs": {}, "Users": {}}

    for ip, count in ip_counter.items():
        if count >= HIGH_THRESHOLD:
            level = "HIGH"
        elif count >= MEDIUM_THRESHOLD:
            level = "MEDIUM"
        else:
            level = "LOW"
        threat_summary["IPs"][ip] = {"attempts": count, "level": level}

    for user, count in user_counter.items():
        if count >= HIGH_THRESHOLD:
            level = "HIGH"
        elif count >= MEDIUM_THRESHOLD:
            level = "MEDIUM"
        else:
            level = "LOW"
        threat_summary["Users"][user] = {"attempts": count, "level": level}

    return threat_summary

def generate_threat_report(threat_summary, report_file="reports/threat_report.txt"):
    with open(report_file, "w") as f:
        f.write("=== THREAT ANALYSIS REPORT ===\n\n")
        f.write("IP THREAT LEVELS:\n")
        for ip, info in threat_summary["IPs"].items():
            f.write(f"{ip} → {info['attempts']} attempts → {info['level']}\n")

        f.write("\nUSER THREAT LEVELS:\n")
        for user, info in threat_summary["Users"].items():
            f.write(f"{user} → {info['attempts']} attempts → {info['level']}\n")

    return report_file
