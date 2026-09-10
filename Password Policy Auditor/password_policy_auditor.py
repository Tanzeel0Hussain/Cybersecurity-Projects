import re
from getpass import getpass
from colorama import Fore, init

init(autoreset=True)

MIN_LENGTH = 12
REQUIRE_UPPER = True
REQUIRE_LOWER = True
REQUIRE_DIGIT = True
REQUIRE_SPECIAL = True


def audit_password(password):
    issues = []

    if len(password) < MIN_LENGTH:
        issues.append(f"Use at least {MIN_LENGTH} characters")
    if REQUIRE_UPPER and not re.search(r"[A-Z]", password):
        issues.append("Add an uppercase letter")
    if REQUIRE_LOWER and not re.search(r"[a-z]", password):
        issues.append("Add a lowercase letter")
    if REQUIRE_DIGIT and not re.search(r"[0-9]", password):
        issues.append("Add a digit")
    if REQUIRE_SPECIAL and not re.search(r"[^A-Za-z0-9\s]", password):
        issues.append("Add a special character")

    return issues


def main():
    print(Fore.CYAN + "=== PASSWORD POLICY AUDITOR ===")
    print("Passwords are checked locally and are not written to disk.\n")

    password = getpass(Fore.YELLOW + "Enter password to audit: ")
    issues = audit_password(password)

    print(Fore.CYAN + "\nPassword Audit Result:\n")
    if not issues:
        print(Fore.GREEN + "[✓] Password meets the configured policy requirements")
        return

    print(Fore.RED + "[!] Password does NOT meet the configured policy requirements:")
    for issue in issues:
        print(Fore.RED + f" - {issue}")


if __name__ == "__main__":
    main()
