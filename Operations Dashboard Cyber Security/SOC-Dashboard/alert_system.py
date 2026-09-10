from pathlib import Path
from datetime import datetime


def generate_alerts(threat_summary, alerts_dir="alerts"):
    alerts_path = Path(alerts_dir)
    alerts_path.mkdir(parents=True, exist_ok=True)
    alerts_list = []

    for ip, info in threat_summary.get("IPs", {}).items():
        if info.get("level") == "HIGH":
            alerts_list.append(
                f"High-risk IP activity: {ip} ({info.get('attempts', 0)} failed attempts)"
            )

    for user, info in threat_summary.get("Users", {}).items():
        if info.get("level") == "HIGH":
            alerts_list.append(
                f"High-risk targeted account: {user} ({info.get('attempts', 0)} failed attempts)"
            )

    if not alerts_list:
        return [], None

    filename = alerts_path / f"alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filename.write_text("\n".join(alerts_list) + "\n", encoding="utf-8")
    return alerts_list, str(filename)
