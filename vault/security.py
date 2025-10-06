import os
import hashlib
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def generate_key(master_password: str):
    """Generate and save a Fernet key derived from master password."""
    salt = b"static_salt_please_change"
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
    fernet_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(fernet_key)
    print("[+] New encryption key created.")
    return fernet_key

def load_key():
    """Load encryption key."""
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_password(password: str) -> bytes:
    key = load_key()
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(encrypted: bytes) -> str:
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted).decode()
