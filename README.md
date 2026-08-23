# Secure Local Password Vault 🔐

A cryptographically secure, local command-line application built in Python to safely store and manage account credentials. This project implements industry-standard data protection methods to ensure passwords are encrypted at rest.

## 🛠️ Security Architecture & Tech Stack

- **Symmetric Encryption:** Utilizes the `cryptography` library's **Fernet** implementation (AES-128 in CBC mode with HMAC authentication).
- **Key Derivation Function (KDF):** Implements **PBKDF2** (Password-Based Key Derivation Function 2) with SHA-256 hashing and 480,000 iterations to derive secure encryption keys directly from a user's Master Password.
- **Hidden Terminal Input:** Uses Python's native `getpass` module to prevent shoulder-surfing attacks by masking input length during authentication.
- **Local Data Storage:** Encrypted ciphertexts are structured and saved locally within a JSON database.

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com
cd secure-password-vault
```

### 2. Set up the virtual environment & dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch the application
```bash
python main.py
```

## 🔒 Configuration & Safety
Sensitive key components (`salt.key`) and the local database (`passwords.json`) are strictly restricted from version control via `.gitignore` configurations to prevent accidental leaks.
