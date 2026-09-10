import hashlib
from pathlib import Path
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

WORDLIST_FILE = "wordlist.txt"
HASH_FILE = "hashes.txt"
OUTPUT_FILE = "matched_hashes.txt"
SUPPORTED_HASHES = {"md5", "sha1", "sha256"}


def hash_word(word, algorithm):
    data = word.encode("utf-8")
    if algorithm == "md5":
        return hashlib.md5(data).hexdigest()
    if algorithm == "sha1":
        return hashlib.sha1(data).hexdigest()
    return hashlib.sha256(data).hexdigest()


def load_lines(filename):
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(filename)
    return [line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]


def main():
    print(Fore.CYAN + "=== OFFLINE HASH MATCHING LAB ===")
    print("Use only with hashes and wordlists you own or are authorized to test.\n")
    print(Fore.YELLOW + "Supported hash types: md5, sha1, sha256")
    hash_type = input(Fore.YELLOW + "Enter hash type: ").strip().lower()

    if hash_type not in SUPPORTED_HASHES:
        print(Fore.RED + "[!] Unsupported hash type.")
        return

    try:
        hashes = load_lines(HASH_FILE)
        wordlist = load_lines(WORDLIST_FILE)
    except FileNotFoundError as exc:
        print(Fore.RED + f"[!] Required file not found: {exc.args[0]}")
        print("Use the included sample hashes.txt and wordlist.txt or replace them with authorized lab data.")
        return

    if not hashes or not wordlist:
        print(Fore.RED + "[!] Input files must not be empty.")
        return

    print(Fore.CYAN + f"\n[+] Loaded {len(hashes)} hash(es) and {len(wordlist)} candidate word(s).\n")
    start = datetime.now()
    matched = []

    lookup = {hash_word(word, hash_type): word for word in wordlist}
    for digest in hashes:
        word = lookup.get(digest.lower())
        if word is not None:
            print(Fore.GREEN + f"[✓] MATCH FOUND -> {digest}")
            matched.append(f"{digest} : {word}")
        else:
            print(Fore.RED + f"[✗] NO MATCH -> {digest}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(matched))
        if matched:
            file.write("\n")

    print(Fore.CYAN + f"\n[✔] Finished in {datetime.now() - start}")
    print(Fore.CYAN + f"[✔] Authorized lab matches saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
