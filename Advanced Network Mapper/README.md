# 🧭 Advanced Network Mapper

A Python network-mapping utility for authorized lab and defensive network inventory work.

## Features
- `/24` IPv4 host discovery using ping
- Bounded concurrent TCP port checks
- Common service-name lookup
- Cross-platform ping handling for Windows/Linux
- Proper socket cleanup
- Writes findings to `network_scan_results.txt`

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python network_mapper.py
```

Example network prefix:

```text
192.168.1.
```

## Notes
Host discovery depends on ICMP/ping availability. Firewalls may block ping even when a host is online.

## Ethical use
Use only on networks you own or are explicitly authorized to assess.
