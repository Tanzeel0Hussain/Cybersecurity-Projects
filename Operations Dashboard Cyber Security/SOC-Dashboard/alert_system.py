import os
from datetime import datetime

ALERTS_DIR = "alerts"
os.makedirs(ALERTS_DIR, exist_ok=True)

def generate_alerts(threat_summary):
    alerts_list = []

    # High risk IPs
    for ip, info in threat_summary["IPs"].items():
        if info["level"] == "HIGH":
            alerts_list.append(f"High-Risk IP Detected: {ip} ({info['attempts']} failed attempts)")

    # High risk Users
    for user, info in threat_summary["Users"].items():
        if info["level"] == "HIGH":
            alerts_list.append(f"High-Risk User Detected: {user} ({info['attempts']} failed attempts)")

    # Save alerts to file
    if alerts_list:
        filename = os.path.join(ALERTS_DIR, f"alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(filename, "w") as f:
            for alert in alerts_list:
                f.write(alert + "\n")
        return alerts_list, filename
    return [], None
