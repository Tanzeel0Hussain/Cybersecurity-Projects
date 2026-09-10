from pathlib import Path
from flask import Flask, render_template, request, abort
import json
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent
POLICIES_FILE = BASE_DIR / "data" / "policies.json"
ALLOWED_SIZES = {"Small", "Medium", "Enterprise"}

app = Flask(__name__)


def load_policies():
    try:
        with POLICIES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def clean_field(value, field_name, max_length=100):
    value = (value or "").strip()
    if not value or len(value) > max_length:
        raise ValueError(f"Invalid {field_name}.")
    return value


def build_policy(company, industry, size):
    return f"""CYBER SECURITY POLICY
Organization: {company}
Industry: {industry}
Organization Size: {size}

1. Purpose
This policy defines baseline controls for protecting organizational systems, accounts, and data.

2. Access Control
Access must follow least-privilege principles and be reviewed regularly. Shared accounts should be avoided.

3. Authentication
Use strong unique passwords and multi-factor authentication wherever supported. Credentials must never be shared.

4. Device and Patch Management
Supported operating systems and applications should be kept current with security updates.

5. Data Protection
Sensitive information should be classified, protected in transit and at rest where appropriate, and shared only with authorized users.

6. Incident Reporting
Suspected security incidents, phishing, malware, lost devices, or unauthorized access must be reported promptly through the organization's approved process.

7. Backup and Recovery
Important business data should be backed up using tested recovery procedures and protected against unauthorized modification.

8. Security Awareness
Personnel should receive recurring security-awareness guidance relevant to their role.

9. Review and Compliance
This generated policy is a baseline template. The organization should review it against applicable laws, contracts, standards, and business requirements before adoption.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        company = clean_field(request.form.get("company"), "company name")
        industry = clean_field(request.form.get("industry"), "industry")
        size = clean_field(request.form.get("size"), "organization size", 30)
        if size not in ALLOWED_SIZES:
            raise ValueError("Invalid organization size.")
    except ValueError as exc:
        abort(400, description=str(exc))

    policy = build_policy(company, industry, size)
    record = {
        "company": company,
        "industry": industry,
        "size": size,
        "date": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "policy": policy,
    }

    POLICIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = load_policies()
    data.append(record)

    with POLICIES_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return render_template("policy.html", policy=policy)


if __name__ == "__main__":
    app.run()
