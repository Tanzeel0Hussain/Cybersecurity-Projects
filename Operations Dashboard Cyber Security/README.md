# 🧠 Cyber Security Operations Dashboard (SOC Dashboard)

A defensive Flask SOC-learning project that accepts authorized authentication logs, analyzes repeated failed logins, calculates simple threat levels and generates alerts/reports.

## Features
- User registration and login
- Werkzeug password hashing instead of raw SHA-256
- Session secret loaded from environment when provided
- Safer uploaded filenames and file-type checks
- Tracks the uploaded log instead of selecting an arbitrary file
- Failed-login analysis
- LOW / MEDIUM / HIGH risk classification
- Alert and report generation
- Runtime database creation; generated database and reports are ignored by Git

## Project layout

```text
Operations Dashboard Cyber Security/
├── README.md
├── static/
├── templates/
└── SOC-Dashboard/
    ├── app.py
    ├── auth.py
    ├── log_analysis.py
    ├── risk_engine.py
    ├── alert_system.py
    ├── requirements.txt
    └── .gitignore
```

The Flask app is intentionally configured to use the `templates/` and `static/` folders one level above `SOC-Dashboard/`.

## Install & run

```bash
cd "Operations Dashboard Cyber Security/SOC-Dashboard"
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000/`.

For deployment, set a strong random `SECRET_KEY` environment variable and do not use Flask's development server as a production server.

## Defensive use
Analyze only logs that you are authorized to access. Threat levels in this project are simple learning heuristics, not a replacement for a production SIEM/SOC platform.
