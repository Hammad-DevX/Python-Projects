import string


def has_uppercase(pw: str) -> bool:
    for ch in pw:
        if ch.isupper():
            return True
        
    return False

def has_lowercase(pw: str) -> bool:
    for ch in pw:
        if ch.islower():
            return True
    
    return False

def has_digit(pw: str) -> bool:
    for ch in pw:
        if ch.isdigit():
            return True
        
    return False

def has_special_char(pw: str) -> bool:
    for ch in pw:
        if ch in string.punctuation:
            return True
        
    return False

def has_valid_length(pw: str) -> bool:
    return len(pw) >= 8

def calculate_strength(pw) -> str:

    rules_met: int = 0

    if has_uppercase(pw):
        rules_met += 1

    if has_lowercase(pw):
        rules_met += 1

    if has_digit(pw):
        rules_met += 1

    if has_special_char(pw):
        rules_met += 1

    if has_valid_length(pw):
        rules_met += 1

    if rules_met <= 2:
        return "❌ Weak"
    elif rules_met <= 4:
        return "⚠️ Medium"
    else:
        return "✅ Strong"


def main():

    while True:
        user_password = input("Enter Password: ")

        if user_password.lower() == "exit":
            print("Program Terminated")
            break
        
        strength = calculate_strength(user_password)
        print("Password Strenght:", strength)

main()

