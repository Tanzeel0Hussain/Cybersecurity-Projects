import requests
import threading
import queue
from colorama import Fore, Style, init

init(autoreset=True)

print(Fore.CYAN + """
=========================================
      ADVANCED DIRECTORY BRUTEFORCER
=========================================
""")

found = []
q = queue.Queue()

# -----------------------------
# Load wordlist into Queue
# -----------------------------
def load_wordlist(wordlist):
    with open(wordlist, "r") as file:
        for line in file:
            q.put(line.strip())


# -----------------------------
# Bruteforce Function
# -----------------------------
def scan_url(base_url):
    while not q.empty():
        path = q.get()
        url = f"{base_url}/{path}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Pentester-Tool)"
        }

        try:
            response = requests.get(url, headers=headers, timeout=3)

            if response.status_code in [200, 301, 302, 403]:

                if response.status_code == 200:
                    print(Fore.GREEN + f"[FOUND 200] {url}")
                elif response.status_code == 301 or response.status_code == 302:
                    print(Fore.YELLOW + f"[REDIRECT {response.status_code}] {url}")
                elif response.status_code == 403:
                    print(Fore.MAGENTA + f"[FORBIDDEN 403] {url}")

                found.append(f"{url} [{response.status_code}]")

            else:
                print(Fore.RED + f"[{response.status_code}] {url}")

        except:
            print(Fore.RED + f"[ERROR] {url}")

        q.task_done()


# -----------------------------
# Start Bruteforce
# -----------------------------
def start_attack(base_url, wordlist, threads_count):
    load_wordlist(wordlist)

    threads = []

    for _ in range(threads_count):
        t = threading.Thread(target=scan_url, args=(base_url,))
        t.daemon = True
        threads.append(t)
        t.start()

    q.join()

    # Save results
    with open("advanced_found_directories.txt", "w") as file:
        for item in found:
            file.write(item + "\n")

    print(Fore.CYAN + "\nScan Completed! Results saved to advanced_found_directories.txt\n")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    base_url = input("Enter target URL (e.g., https://example.com): ").strip().rstrip("/")
    wordlist = input("Enter wordlist filename: ").strip()
    threads_count = int(input("Threads to use (10 recommended): "))

    start_attack(base_url, wordlist, threads_count)
