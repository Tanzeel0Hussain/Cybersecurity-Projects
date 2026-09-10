import time
import random
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"
DELAY_RANGE = (0.2, 0.6)
LOG_FILE = "simulation_log.txt"


def log_attempt(username, result):
    """Log only the username and result; never store attempted passwords."""
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now().isoformat(timespec='seconds')} | user={username} | result={result}\n")


def simulate_login(username, password):
    time.sleep(random.uniform(*DELAY_RANGE))
    return username == VALID_USERNAME and password == VALID_PASSWORD


def main():
    print(Fore.CYAN + "=== LOCAL LOGIN ATTACK SIMULATOR ===")
    print("This demo checks only hard-coded local credentials; it does not connect to websites or services.\n")

    usernames = [value.strip() for value in input(Fore.YELLOW + "Enter usernames (comma separated): ").split(",") if value.strip()]
    passwords = [value.strip() for value in input(Fore.YELLOW + "Enter passwords (comma separated): ").split(",") if value.strip()]

    if not usernames or not passwords:
        print(Fore.RED + "[!] Enter at least one username and one password.")
        return

    print(Fore.CYAN + "\n[+] Starting local simulation...\n")

    for user in usernames:
        for password in passwords:
            print(Fore.WHITE + f"Trying user: {user}")
            success = simulate_login(user, password)

            if success:
                print(Fore.GREEN + f"[✓] Simulated success for user: {user}")
                log_attempt(user, "SUCCESS")
                print(Fore.CYAN + "\n[✔] Demo credential matched. Simulation stopped.\n")
                return

            print(Fore.RED + "[✗] Simulated failure")
            log_attempt(user, "FAILED")

    print(Fore.YELLOW + "\n[!] Simulation finished. No demo credential matched.")


if __name__ == "__main__":
    main()
