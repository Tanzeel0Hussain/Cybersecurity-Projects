# 🔎 Port Scanner

A safe, educational Python TCP port scanner for systems you own or are explicitly authorized to test.

## Features
- Scans a user-selected TCP port range
- Uses a bounded thread pool for better stability
- Shows common service names for known ports
- Prints security notes as **heuristics**, not confirmed vulnerabilities
- Validates target and port input

## Run

```bash
python port_scanner.py
```

No third-party Python package is required.

## Important note
An open port or a service-specific warning is **not proof of a vulnerability**. Confirm findings using authorized defensive assessment methods.

## Ethical use
Use only on your own devices, lab systems, CTF environments, or systems for which you have clear permission.
