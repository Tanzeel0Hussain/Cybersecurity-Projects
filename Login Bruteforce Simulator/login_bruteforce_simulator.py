import time
import random
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# ---------------- CONFIG ---------------- #
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"
DELAY_RANGE = (0.5, 1.5)
LOG_FILE = "bruteforce_log.txt"
# ---------------------------------------- #

def banner():
    print(Fore.CYAN + """
██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
    """ + Style.RESET_ALL)

def log_attempt(username, password, result):
    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.now()} | {username}:{password} -> {result}\n")

def simulate_login(username, password):
    time.sleep(random.uniform(*DELAY_RANGE))
    return username == VALID_USERNAME and password == VALID_PASSWORD

def main():
    banner()

    usernames = input(Fore.YELLOW + "Enter usernames (comma separated): ").split(",")
    passwords = input(Fore.YELLOW + "Enter passwords (comma separated): ").split(",")

    print(Fore.CYAN + "\n[+] Starting brute force simulation...\n")

    for user in usernames:
        for pwd in passwords:
            print(Fore.WHITE + f"Trying {user.strip()} : {pwd.strip()}")

            success = simulate_login(user.strip(), pwd.strip())

            if success:
                print(Fore.GREEN + f"[✓] SUCCESS → {user}:{pwd}")
                log_attempt(user, pwd, "SUCCESS")
                print(Fore.CYAN + "\n[✔] Valid credentials found. Stopping attack.\n")
                return
            else:
                print(Fore.RED + "[✗] Failed")
                log_attempt(user, pwd, "FAILED")

    print(Fore.YELLOW + "\n[!] Brute force finished. No valid credentials found.")

if __name__ == "__main__":
    main()
