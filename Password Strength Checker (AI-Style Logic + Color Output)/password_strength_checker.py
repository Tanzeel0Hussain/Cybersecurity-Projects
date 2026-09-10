import re
from getpass import getpass

COMMON_PASSWORDS = {
    "1234", "123456", "password", "qwerty", "admin",
    "iloveyou", "123123", "abc123", "root", "111111",
}


def password_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 12 characters; 16+ is better for important accounts.")

    checks = (
        (r"[A-Z]", "Add uppercase letters (A-Z)."),
        (r"[a-z]", "Add lowercase letters (a-z)."),
        (r"[0-9]", "Add numbers (0-9)."),
        (r"[^A-Za-z0-9\s]", "Add special characters."),
    )

    for pattern, suggestion in checks:
        if re.search(pattern, password):
            score += 1
        else:
            suggestions.append(suggestion)

    lowered = password.lower()
    if lowered in COMMON_PASSWORDS or any(weak in lowered for weak in COMMON_PASSWORDS if len(weak) >= 6):
        score = max(0, score - 3)
        suggestions.append("Avoid common passwords and predictable words.")

    if score >= 7:
        strength = "VERY STRONG"
    elif score >= 5:
        strength = "STRONG"
    elif score >= 3:
        strength = "MEDIUM"
    else:
        strength = "WEAK"

    return strength, suggestions


def main():
    print("=== PASSWORD STRENGTH CHECKER ===")
    print("Rule-based local heuristic; no AI model is used and the password is not saved.\n")
    password = getpass("Enter a password to analyze: ")

    strength, suggestions = password_strength(password)
    print(f"\nPassword Strength: {strength}")

    if suggestions:
        print("\nSuggestions to improve:")
        for suggestion in dict.fromkeys(suggestions):
            print(f"- {suggestion}")
    else:
        print("\nNo improvements suggested by the configured rules.")


if __name__ == "__main__":
    main()
