import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

def scan_port(ip, port, output_box):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))

        if result == 0:
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "No Banner"

            output_box.insert(tk.END, f"[OPEN] Port {port} — Banner: {banner}\n")
            output_box.see(tk.END)

        s.close()
    except Exception as e:
        pass

def start_scan(ip_entry, start_entry, end_entry, output_box):
    ip = ip_entry.get()
    start_port = start_entry.get()
    end_port = end_entry.get()

    if not ip or not start_port or not end_port:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        start_port = int(start_port)
        end_port = int(end_port)
    except:
        messagebox.showerror("Error", "Ports must be numbers!")
        return

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Scanning {ip} from {start_port} to {end_port}...\n\n")

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, output_box))
        thread.start()

# GUI Setup
app = tk.Tk()
app.title("GUI Port Scanner")
app.geometry("600x400")
app.config(bg="#1e1e1e")

title = tk.Label(app, text="Advanced GUI Port Scanner", fg="white", bg="#1e1e1e", font=("Arial", 16, "bold"))
title.pack(pady=10)

frame = tk.Frame(app, bg="#1e1e1e")
frame.pack()

tk.Label(frame, text="Target IP:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(frame, width=30)
ip_entry.grid(row=0, column=1)

tk.Label(frame, text="Start Port:", fg="white", bg="#1e1e1e").grid(row=1, column=0, padx=5, pady=5)
start_entry = tk.Entry(frame, width=30)
start_entry.grid(row=1, column=1)

tk.Label(frame, text="End Port:", fg="white", bg="#1e1e1e").grid(row=2, column=0, padx=5, pady=5)
end_entry = tk.Entry(frame, width=30)
end_entry.grid(row=2, column=1)

scan_btn = tk.Button(app, text="Start Scan", width=20, bg="#00aa00", fg="white",
                     command=lambda: start_scan(ip_entry, start_entry, end_entry, output_box))
scan_btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(app, width=70, height=15, bg="#111111", fg="white")
output_box.pack(pady=10)

app.mainloop()