import re

# List of commonly used weak passwords
COMMON_PASSWORDS = [
    "1234", "123456", "password", "qwerty", "admin",
    "iloveyou", "123123", "abc123", "root", "111111"
]

def password_strength(password):
    score = 0
    suggestions = []

    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 12 characters.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters (A-Z).")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters (a-z).")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add numbers (0-9).")

    # Special Characters
    if re.search(r"[@$!%*?&#^+=_.,-]", password):
        score += 1
    else:
        suggestions.append("Add special characters (!@#$%).")

    # Common Password Check
    for weak in COMMON_PASSWORDS:
        if weak in password.lower():
            suggestions.append("Avoid common passwords like '123456', 'password'.")
            score = max(0, score - 2)

    # Strength Category
    if score >= 6:
        strength = "VERY STRONG"
    elif score >= 4:
        strength = "STRONG"
    elif score >= 2:
        strength = "MEDIUM"
    else:
        strength = "WEAK"

    return strength, suggestions

def main():
    print("=== Password Strength Checker ===")
    password = input("Enter a password to analyze: ")

    strength, suggestions = password_strength(password)

    print(f"\nPassword Strength: {strength}")

    if suggestions:
        print("\nSuggestions to improve:")
        for s in suggestions:
            print(f"- {s}")
    else:
        print("\nYour password is strong. No improvements needed!")

if __name__ == "__main__":
    main()