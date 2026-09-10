from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin
import requests
from colorama import Fore, init

init(autoreset=True)

FOUND_CODES = {200, 301, 302, 403}
DEFAULT_THREADS = 20
TIMEOUT = 5


def scan_url(session, base_url, path):
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        response = session.get(url, timeout=TIMEOUT, allow_redirects=False)
        return url, response.status_code
    except requests.RequestException:
        return url, None


def start_scan(base_url, wordlist, threads_count):
    wordlist_path = Path(wordlist)
    if not wordlist_path.is_file():
        print(Fore.RED + f"[!] Wordlist not found: {wordlist}")
        return

    paths = [line.strip() for line in wordlist_path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
    if not paths:
        print(Fore.RED + "[!] Wordlist is empty.")
        return

    threads_count = max(1, min(threads_count, 100))
    found = []

    with requests.Session() as session:
        session.headers.update({"User-Agent": "Authorized-Security-Lab/1.0"})
        with ThreadPoolExecutor(max_workers=threads_count) as executor:
            futures = [executor.submit(scan_url, session, base_url, path) for path in paths]
            for future in as_completed(futures):
                url, status = future.result()
                if status in FOUND_CODES:
                    if status == 200:
                        color = Fore.GREEN
                    elif status in {301, 302}:
                        color = Fore.YELLOW
                    else:
                        color = Fore.MAGENTA
                    print(color + f"[{status}] {url}")
                    found.append((url, status))

    with open("advanced_found_directories.txt", "w", encoding="utf-8") as file:
        for url, status in sorted(found):
            file.write(f"{url} [{status}]\n")

    print(Fore.CYAN + f"\nScan completed. {len(found)} path(s) saved to advanced_found_directories.txt\n")


if __name__ == "__main__":
    print(Fore.CYAN + "=== ADVANCED DIRECTORY DISCOVERY TOOL ===")
    print("Use only on systems you own or are explicitly authorized to test.\n")

    base_url = input("Enter target URL (e.g., https://example.com): ").strip()
    wordlist = input("Enter wordlist filename: ").strip()

    if not base_url.startswith(("http://", "https://")):
        print(Fore.RED + "[!] URL must start with http:// or https://")
    else:
        try:
            threads_count = int(input(f"Threads to use ({DEFAULT_THREADS} recommended, max 100): ") or DEFAULT_THREADS)
        except ValueError:
            threads_count = DEFAULT_THREADS
        start_scan(base_url, wordlist, threads_count)
