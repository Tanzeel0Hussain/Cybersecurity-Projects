# 📊 Log Analyzer

A defensive Python log-analysis project for reviewing SSH authentication failures and producing text and optional JSON security reports.

## Features

- Parses failed SSH login events
- Counts suspicious source IP addresses
- Counts targeted usernames
- Applies a configurable failed-attempt threshold
- Prints colorized findings
- Generates `security_report.txt`
- Supports optional machine-readable JSON export
- Includes `sample_auth.log` so the project works immediately

## Install

```bash
pip install -r requirements.txt
```

## Run

Use the included sample log:

```bash
python log_analyzer.py sample_auth.log
```

Analyze an authorized local log file:

```bash
python log_analyzer.py /path/to/auth.log
```

Generate both text and JSON reports:

```bash
python log_analyzer.py sample_auth.log --json-output report.json
```

Use a custom suspicious-attempt threshold:

```bash
python log_analyzer.py sample_auth.log --threshold 10 --json-output report.json
```

## JSON Output

The optional JSON report contains:

- Generation timestamp
- Suspicious-attempt threshold
- Failed-login counts by IP address
- Suspicious/Observed status
- Targeted username counts

This format can be consumed by dashboards, automation scripts, and SOC/SIEM-style workflows.

## Example JSON Structure

```json
{
  "generated_at": "2026-09-13T04:00:00",
  "threshold": 5,
  "suspicious_ip_activity": [
    {
      "ip": "192.168.1.10",
      "failed_attempts": 7,
      "status": "SUSPICIOUS"
    }
  ],
  "targeted_usernames": [
    {
      "username": "admin",
      "failed_attempts": 4
    }
  ]
}
```

## Use Cases

- Blue Team training
- SOC log review
- SSH brute-force pattern detection
- Security automation
- Dashboard integration
- SIEM-style data processing

## Defensive Use

This project is designed for Blue Team/SOC learning and defensive security research.

Only analyze logs from systems you own or environments where you have explicit authorization.

Do not use this project to access, monitor, or analyze systems or data without permission.
