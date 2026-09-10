# 📡 Advanced Packet Sniffer

A Python + Scapy packet observation tool for defensive network learning and authorized monitoring.

## Features
- Captures IPv4 traffic
- Identifies TCP, UDP, ICMP and other IP protocols
- Shows timestamp, source, destination and packet size
- Optional interface and capture filter support
- Writes summarized packet metadata to `captured_packets.log`
- Graceful handling of permission and capture errors

## Install

```bash
pip install -r requirements.txt
```

## Run

Linux usually requires elevated packet-capture permission:

```bash
sudo python packet_sniffer.py
```

On Windows, run the terminal with the permissions required by your packet capture driver.

## Privacy & ethical use
Capture traffic only on networks and interfaces you are authorized to monitor. This project logs packet metadata, not a claim of full Wireshark functionality.
