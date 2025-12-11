import requests
import threading

found_paths = []

def scan_path(base_url, path):
    url = f"{base_url}/{path}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[FOUND] {url}")
            found_paths.append(url)
        else:
            print(f"[404] {url}")
    except:
        print(f"[ERROR] {url}")

def start_bruteforce(base_url, wordlist_file):
    threads = []

    with open(wordlist_file, 'r') as file:
        for line in file:
            path = line.strip()
            t = threading.Thread(target=scan_path, args=(base_url, path))
            threads.append(t)
            t.start()

    for thread in threads:
        thread.join()

    # Save results
    with open("found_directories.txt", "w") as output:
        for item in found_paths:
            output.write(item + "\n")

    print("\nScan complete! Results saved to found_directories.txt")

if __name__ == "__main__":
    print("=== Directory Bruteforcer ===")

    base_url = input("Enter target URL (e.g., https://example.com): ").strip()
    wordlist_file = input("Enter wordlist file name: ").strip()

    start_bruteforce(base_url, wordlist_file)