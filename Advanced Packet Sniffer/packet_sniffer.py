import argparse
from datetime import datetime
from pathlib import Path
from scapy.all import sniff, IP
from colorama import Fore, init

init(autoreset=True)

DEFAULT_LOG = "captured_packets.log"


def build_parser():
    parser = argparse.ArgumentParser(description="Authorized network packet metadata monitor")
    parser.add_argument("--interface", help="Network interface to capture from (optional)")
    parser.add_argument("--filter", default="ip", help="BPF capture filter (default: ip)")
    parser.add_argument("--count", type=int, default=0, help="Stop after N packets; 0 means run until interrupted")
    parser.add_argument("--output", default=DEFAULT_LOG, help="Log output file")
    return parser


def protocol_name(proto):
    return {6: "TCP", 17: "UDP", 1: "ICMP"}.get(proto, f"Other({proto})")


def packet_callback(packet, log_path):
    if IP not in packet:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    src = packet[IP].src
    dst = packet[IP].dst
    protocol = protocol_name(packet[IP].proto)
    length = len(packet)

    color = {
        "TCP": Fore.CYAN,
        "UDP": Fore.YELLOW,
        "ICMP": Fore.GREEN,
    }.get(protocol, Fore.MAGENTA)

    log_text = f"{timestamp} | {protocol} | {src} -> {dst} | Size: {length}"
    print(color + log_text)

    with log_path.open("a", encoding="utf-8") as file:
        file.write(log_text + "\n")


def main():
    args = build_parser().parse_args()
    if args.count < 0:
        raise SystemExit("--count must be 0 or greater")

    log_path = Path(args.output)
    print(Fore.LIGHTBLUE_EX + "=== ADVANCED PACKET SNIFFER ===")
    print("Captures packet metadata only. Use on networks you own or are authorized to monitor.")
    print("Press Ctrl+C to stop when --count is 0.\n")

    try:
        sniff(
            iface=args.interface,
            filter=args.filter or None,
            prn=lambda packet: packet_callback(packet, log_path),
            store=False,
            count=args.count,
        )
    except PermissionError:
        print(Fore.RED + "[!] Permission denied. Run with the required capture privileges.")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nCapture stopped by user.")
    except OSError as exc:
        print(Fore.RED + f"[!] Capture error: {exc}")


if __name__ == "__main__":
    main()
