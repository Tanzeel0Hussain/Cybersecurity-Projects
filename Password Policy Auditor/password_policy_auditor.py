import re
from colorama import Fore, Style, init

init(autoreset=True)

# ---------------- POLICY RULES ---------------- #
MIN_LENGTH = 8
REQUIRE_UPPER = True
REQUIRE_LOWER = True
REQUIRE_DIGIT = True
REQUIRE_SPECIAL = True
# ---------------------------------------------- #

def banner():
    print(Fore.CYAN + """
██████╗  █████╗ ███████╗███████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝
██████╔╝███████║███████╗███████╗
██╔═══╝ ██╔══██║╚════██║╚════██║
██║     ██║  ██║███████║███████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
Password Policy Auditor
    """)

def audit_password(password):
    issues = []

    if len(password) < MIN_LENGTH:
        issues.append("Minimum length not met")

    if REQUIRE_UPPER and not re.search(r"[A-Z]", password):
        issues.append("Missing uppercase letter")

    if REQUIRE_LOWER and not re.search(r"[a-z]", password):
        issues.append("Missing lowercase letter")

    if REQUIRE_DIGIT and not re.search(r"[0-9]", password):
        issues.append("Missing digit")

    if REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("Missing special character")

    return issues

def main():
    banner()
    password = input(Fore.YELLOW + "Enter password to audit: ")

    issues = audit_password(password)

    print(Fore.CYAN + "\nPassword Audit Result:\n")

    if not issues:
        print(Fore.GREEN + "[✓] Password meets all security policy requirements")
    else:
        print(Fore.RED + "[!] Password does NOT meet policy requirements:\n")
        for issue in issues:
            print(Fore.RED + f" - {issue}")

if __name__ == "__main__":
    main()