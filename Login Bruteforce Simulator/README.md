# 🧪 Login Bruteforce Simulator

A **local-only educational simulator** that demonstrates repeated login attempts without targeting a real website or remote account.

## Features
- Fixed local demo credentials
- User-supplied test username/password lists
- Random delay to make attempts observable
- Stops when the local simulated credentials match
- Logs attempt outcome without storing plaintext passwords

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python login_bruteforce_simulator.py
```

## Safety design
This project does not send login attempts to remote services. It is intentionally limited to a local simulation for learning authentication and monitoring concepts.
