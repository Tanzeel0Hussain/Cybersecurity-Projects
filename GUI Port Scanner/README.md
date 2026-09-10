# 🖥️ GUI Port Scanner

A Tkinter desktop interface for authorized TCP port scanning.

## Features
- Simple graphical interface
- Target IP and custom port range
- Bounded worker threads to avoid creating one thread per port
- Real-time open-port results
- Banner attempt with graceful error handling
- Input validation

## Run

```bash
python gui_port_scanner.py
```

Tkinter and socket are part of the standard Python distribution on most desktop installations. On some Linux systems you may need the OS package for Tk.

## Notes
The scanner reports reachable TCP ports. A reachable port does not automatically mean a service is vulnerable.

## Ethical use
Use only on systems you own or have explicit permission to assess.
