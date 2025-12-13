import hashlib
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# ---------------- CONFIG ---------------- #
WORDLIST_FILE = "wordlist.txt"
HASH_FILE = "hashes.txt"
OUTPUT_FILE = "cracked_passwords.txt"
SUPPORTED_HASHES = ["md5", "sha1", "sha256"]
# ---------------------------------------- #

def banner():
    print(Fore.CYAN + """
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██╔═══╝ 
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██║     
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝     
    """ + Style.RESET_ALL)

def hash_word(word, algo):
    word = word.encode()
    if algo == "md5":
        return hashlib.md5(word).hexdigest()
    elif algo == "sha1":
        return hashlib.sha1(word).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(word).hexdigest()

def load_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

def main():
    banner()

    print(Fore.YELLOW + "[*] Supported Hash Types: md5, sha1, sha256")
    hash_type = input(Fore.YELLOW + "Enter hash type: ").lower()

    if hash_type not in SUPPORTED_HASHES:
        print(Fore.RED + "[!] Unsupported hash type")
        return

    hashes = load_file(HASH_FILE)
    wordlist = load_file(WORDLIST_FILE)

    print(Fore.CYAN + f"\n[+] Loaded {len(hashes)} hashes")
    print(Fore.CYAN + f"[+] Loaded {len(wordlist)} words\n")

    cracked = []

    start = datetime.now()

    for h in hashes:
        found = False
        for word in wordlist:
            if hash_word(word, hash_type) == h:
                print(Fore.GREEN + f"[✓] CRACKED → {h} = {word}")
                cracked.append(f"{h} : {word}")
                found = True
                break
        if not found:
            print(Fore.RED + f"[✗] NOT FOUND → {h}")

    with open(OUTPUT_FILE, "w") as file:
        for item in cracked:
            file.write(item + "\n")

    end = datetime.now()
    print(Fore.CYAN + f"\n[✔] Finished in {end - start}")
    print(Fore.CYAN + f"[✔] Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
