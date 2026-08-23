import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

DATA_FILE = "passwords.json"
SALT_FILE = "salt.key"

def get_or_create_salt():
    """Generates a unique salt for key derivation or loads the existing one."""
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt
    with open(SALT_FILE, "rb") as f:
        return f.read()

def derive_key(master_password: str) -> bytes:
    """Derives a cryptographically secure Fernet key from the Master Password."""
    salt = get_or_create_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, # Industry standard iterations
    )
    # Turn the raw password into a secure 32-byte string and URL-safe encode it
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

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

def add_password(account, password, master_password):
    """Encrypts and adds a password to the local JSON vault using the Master Password."""
    key = derive_key(master_password)
    fernet = Fernet(key)
    
    encrypted_password = fernet.encrypt(password.encode()).decode()
    
    vault = load_vault()
    vault[account] = encrypted_password
    save_vault(vault)
    print(f"[+] Successfully encrypted and saved credentials for: {account}")

def get_password(account, master_password):
    """Decrypts and retrieves a password using the provided Master Password."""
    vault = load_vault()
    if account not in vault:
        print(f"[-] No credentials found for account: {account}")
        return None
        
    key = derive_key(master_password)
    fernet = Fernet(key)
    
    try:
        encrypted_password = vault[account].encode()
        decrypted_password = fernet.decrypt(encrypted_password).decode()
        return decrypted_password
    except Exception:
        print("[-] Access Denied: Incorrect Master Password or corrupted data.")
        return None
