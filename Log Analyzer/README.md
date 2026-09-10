# 📊 Log Analyzer

A defensive Python log-analysis project for reviewing SSH authentication failures and producing a simple security report.

## Features
- Parses failed SSH login events
- Counts suspicious source IP addresses
- Counts targeted usernames
- Applies a configurable failed-attempt threshold
- Prints colorized findings
- Generates `security_report.txt`
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

Or analyze an authorized local log file:

```bash
python log_analyzer.py /path/to/auth.log
```

## Defensive use
This project is designed for Blue Team/SOC learning. Only analyze logs you are authorized to access.
