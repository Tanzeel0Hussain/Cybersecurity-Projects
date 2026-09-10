import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = 100
TIMEOUT = 0.6


def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            if sock.connect_ex((ip, port)) == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "Unknown"
                return port, service
    except OSError:
        pass
    return None


def start_scan(ip_entry, start_entry, end_entry, output_box, scan_btn):
    target = ip_entry.get().strip()

    try:
        ip = socket.gethostbyname(target)
        start_port = int(start_entry.get())
        end_port = int(end_entry.get())
    except (socket.gaierror, ValueError):
        messagebox.showerror("Error", "Enter a valid IP/hostname and numeric ports.")
        return

    if not (1 <= start_port <= end_port <= 65535):
        messagebox.showerror("Error", "Port range must be between 1 and 65535.")
        return

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Scanning {ip} from {start_port} to {end_port}...\n\n")
    scan_btn.config(state=tk.DISABLED)

    def worker():
        results = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        def finish():
            for port, service in sorted(results):
                output_box.insert(tk.END, f"[OPEN] Port {port} — Service: {service}\n")
            output_box.insert(tk.END, f"\nScan complete. {len(results)} open port(s) found.\n")
            output_box.see(tk.END)
            scan_btn.config(state=tk.NORMAL)

        app.after(0, finish)

    import threading
    threading.Thread(target=worker, daemon=True).start()


app = tk.Tk()
app.title("GUI Port Scanner")
app.geometry("700x500")
app.config(bg="#1e1e1e")

title = tk.Label(app, text="GUI Port Scanner", fg="white", bg="#1e1e1e", font=("Arial", 18, "bold"))
title.pack(pady=12)

subtitle = tk.Label(app, text="Authorized systems only", fg="#bbbbbb", bg="#1e1e1e")
subtitle.pack()

frame = tk.Frame(app, bg="#1e1e1e")
frame.pack(pady=10)

for row, label in enumerate(("Target IP / Hostname:", "Start Port:", "End Port:")):
    tk.Label(frame, text=label, fg="white", bg="#1e1e1e").grid(row=row, column=0, padx=6, pady=6, sticky="e")

ip_entry = tk.Entry(frame, width=34)
ip_entry.grid(row=0, column=1)
start_entry = tk.Entry(frame, width=34)
start_entry.grid(row=1, column=1)
end_entry = tk.Entry(frame, width=34)
end_entry.grid(row=2, column=1)

output_box = scrolledtext.ScrolledText(app, width=82, height=18, bg="#111111", fg="white")
output_box.pack(pady=12)

scan_btn = tk.Button(
    app,
    text="Start Scan",
    width=22,
    bg="#00aa00",
    fg="white",
    command=lambda: start_scan(ip_entry, start_entry, end_entry, output_box, scan_btn),
)
scan_btn.pack(pady=8)

app.mainloop()
