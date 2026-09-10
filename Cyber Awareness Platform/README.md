# 🎓 Cyber Security Awareness & Risk Assessment Platform

A Flask-based defensive awareness application that helps users review everyday security habits and generates a simple risk score with recommendations.

## Features
- Cybersecurity awareness questionnaire
- Client-side answer validation
- Server-side answer validation
- Low / Medium / High risk result
- Security recommendations
- JSON report history
- Clean Flask structure
- Working `static/js/quiz.js` path
- Real SVG project banner

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

## Data
Assessment results are stored in `data/reports.json`. Do not store sensitive personal information in this demo data file.

## Scope
This is an educational risk-awareness tool, not a professional security audit or compliance certification system.
