from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin
import requests

MAX_WORKERS = 20
TIMEOUT = 5
FOUND_CODES = {200, 301, 302, 403}


def scan_path(session, base_url, path):
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        response = session.get(url, timeout=TIMEOUT, allow_redirects=False)
        if response.status_code in FOUND_CODES:
            return url, response.status_code
    except requests.RequestException:
        pass
    return None


def start_scan(base_url, wordlist_file):
    wordlist = Path(wordlist_file)
    if not wordlist.is_file():
        print(f"[!] Wordlist not found: {wordlist_file}")
        return

    paths = [line.strip() for line in wordlist.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
    if not paths:
        print("[!] Wordlist is empty.")
        return

    found = []
    with requests.Session() as session:
        session.headers.update({"User-Agent": "Authorized-Security-Lab/1.0"})
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(scan_path, session, base_url, path) for path in paths]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    url, status = result
                    print(f"[FOUND {status}] {url}")
                    found.append(result)

    with open("found_directories.txt", "w", encoding="utf-8") as output:
        for url, status in sorted(found):
            output.write(f"{url} [{status}]\n")

    print(f"\nScan complete. {len(found)} path(s) recorded in found_directories.txt")


if __name__ == "__main__":
    print("=== Directory Discovery Tool ===")
    print("Use only with systems you own or have explicit permission to test.\n")
    base_url = input("Enter target URL (e.g., https://example.com): ").strip()
    wordlist_file = input("Enter wordlist filename: ").strip()

    if not base_url.startswith(("http://", "https://")):
        print("[!] URL must start with http:// or https://")
    else:
        start_scan(base_url, wordlist_file)
