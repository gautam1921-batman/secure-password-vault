import os
import json
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"

def generate_and_save_key():
    """Generates a master encryption key and saves it locally."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print("[+] A new Master Key has been generated and saved locally.")

def load_key():
    """Loads the master key from the local file."""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("Master Key file missing! Please generate a key first.")
    with open(KEY_FILE, "rb") as f:
        return f.read()

def load_vault():
    """Loads the encrypted vault data or returns an empty dictionary."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_vault(data):
    """Saves the vault dictionary back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_password(account, password):
    """Encrypts and adds a password to the local JSON vault."""
    key = load_key()
    fernet = Fernet(key)
    
    # Encrypt the password string
    encrypted_password = fernet.encrypt(password.encode()).decode()
    
    vault = load_vault()
    vault[account] = encrypted_password
    save_vault(vault)
    print(f"[+] Successfully encrypted and saved credentials for: {account}")

def get_password(account):
    """Decrypts and retrieves a password for a given account."""
    vault = load_vault()
    if account not in vault:
        print(f"[-] No credentials found for account: {account}")
        return None
        
    key = load_key()
    fernet = Fernet(key)
    
    try:
        # Decrypt the stored ciphertext
        encrypted_password = vault[account].encode()
        decrypted_password = fernet.decrypt(encrypted_password).decode()
        return decrypted_password
    except Exception as e:
        print("[-] Decryption failed. Your master key might be invalid or corrupted.")
        return None
