import re

def check_password_strength(password):
    length = len(password)
    uppercase = any(char.isupper() for char in password)
    lowercase = any(char.islower() for char in password)
    digits = any(char.isdigit() for char in password)
    special_chars = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    score = 0

    if length >= 8:
        score += 1
    if uppercase:
        score += 1
    if lowercase:
        score += 1
    if digits:
        score += 1
    if special_chars:
        score += 1

    if score == 5:
        return "Very Strong"
    elif score >= 4:
        return "Strong"
    elif score >= 3:
        return "Moderate"
    elif score >= 2:
        return "Weak"
    else:
        return "Very Weak"

def main():
    password = input("Enter your password: ")
    strength = check_password_strength(password)
    print("Password Strength:", strength)

if __name__ == "__main__":
    main()
