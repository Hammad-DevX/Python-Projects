# Password Strength Checker (Python CLI)

A simple and secure **command-line password strength checker** built using Python.  
The program evaluates passwords based on common real-world security rules.

---

## Features

- Checks password length (minimum 8 characters)
- Validates:
  - Uppercase letters
  - Lowercase letters
  - Digits
  - Special characters
- Classifies password strength:
  - ❌ Weak
  - ⚠️ Medium
  - ✅ Strong
- Allows multiple checks in one session
- Safe handling (password is never printed back)

---

## Rules Used

| Rule | Requirement |
|---|---|
| Length | ≥ 8 characters |
| Uppercase | At least 1 |
| Lowercase | At least 1 |
| Digit | At least 1 |
| Special Character | At least 1 |

---

## Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/your-username/password-strength-checker.git
