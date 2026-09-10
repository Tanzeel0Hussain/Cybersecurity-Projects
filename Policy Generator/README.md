# 🛡️ Cyber Security Policy Generator

A Flask-based GRC/awareness project that generates a customizable cybersecurity policy draft from basic organization information.

## Features
- Organization name, industry and size input
- Generates a structured security-policy draft
- Covers access control, authentication, data protection, backups, incident response, acceptable use, vendors, awareness and policy review
- Stores generated drafts in `data/policies.json`
- Input validation and safer file handling

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

## Compliance note
The generated text is a **starter template**, not legal advice and not automatic ISO 27001, NIST, PCI DSS, HIPAA or other regulatory certification. Organizations should review policies with appropriate security, legal and compliance professionals.

## Defensive scope
This project is focused on governance, awareness and security-policy education; it does not perform offensive security actions.
