# 📁 Directory Bruteforcer

A small authorized web-content discovery tool for learning how directory enumeration works in security testing.

## Features
- Reads paths from a wordlist
- Uses a bounded thread pool for controlled concurrency
- Request timeout handling
- Normalizes the base URL
- Saves discovered paths to `found_directories.txt`

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python directory_bruteforcer.py
```

Provide a URL you own or are permitted to test and a local wordlist file.

## Ethical use
Directory discovery can generate many HTTP requests. Use this project only in labs, CTFs, or on systems where you have explicit authorization.
