# 🚀 Advanced Directory Bruteforcer

A controlled multi-threaded directory discovery tool for authorized cybersecurity labs and defensive testing.

## Features
- Bounded worker pool
- Detects useful HTTP status codes such as 200, 301, 302 and 403
- Request timeout and connection error handling
- Colorized terminal output
- Saves findings to `advanced_found_directories.txt`
- Safer input validation and normalized URLs

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python advanced_directory_bruteforcer.py
```

## Ethical use
Use only on websites and applications you own or have explicit permission to assess. High request rates can affect a server, so choose a reasonable thread count.
