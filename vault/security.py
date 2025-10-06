import os
import base64
import hashlib
from cryptography.fernet import Fernet


KEY_FILE = "secret.key"
SALT_FILE = "salt.bin"


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a 32-byte encryption key from master password and salt."""
    return base64.urlsafe_b64encode(
        hashlib.pbkdf2_hmac("sha256", master_password.encode(), salt, 200_000)
    )


def generate_key(master_password: str):
    """Generate a new Fernet key and encrypt it with master password."""
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as sf:
        sf.write(salt)

    derived_key = derive_key(master_password, salt)
    f = Fernet(derived_key)

    vault_key = Fernet.generate_key()

    encrypted_vault_key = f.encrypt(vault_key)

    with open(KEY_FILE, "wb") as kf:
        kf.write(encrypted_vault_key)

    print("[+] Encrypted secret key generated and saved securely.")
    return vault_key


def load_key(master_password: str) -> bytes:
    """Load and decrypt Fernet key using master password."""
    if not (os.path.exists(KEY_FILE) and os.path.exists(SALT_FILE)):
        raise FileNotFoundError("Missing key or salt file. Run setup first.")

    with open(SALT_FILE, "rb") as sf:
        salt = sf.read()

    with open(KEY_FILE, "rb") as kf:
        encrypted_vault_key = kf.read()

    derived_key = derive_key(master_password, salt)
    f = Fernet(derived_key)

    try:
        vault_key = f.decrypt(encrypted_vault_key)
        return vault_key
    except Exception:
        raise ValueError("Invalid master password!")


def encrypt_password(password: str, master_password: str) -> bytes:
    """Encrypt password using decrypted vault key."""
    key = load_key(master_password)
    f = Fernet(key)
    return f.encrypt(password.encode())


def decrypt_password(encrypted: bytes, master_password: str) -> str:
    """Decrypt password using decrypted vault key."""
    key = load_key(master_password)
    f = Fernet(key)
    return f.decrypt(encrypted).decode()

def update_master_password(old_password: str, new_password: str):
    """
    Update master password by decrypting the old vault key with the old password,
    then re-encrypting it with the new password.
    """
    if not (os.path.exists(KEY_FILE) and os.path.exists(SALT_FILE)):
        raise FileNotFoundError("Missing key or salt file.")

    with open(SALT_FILE, "rb") as sf:
        old_salt = sf.read()

    with open(KEY_FILE, "rb") as kf:
        encrypted_vault_key = kf.read()

    old_derived_key = derive_key(old_password, old_salt)
    f_old = Fernet(old_derived_key)

    try:
        vault_key = f_old.decrypt(encrypted_vault_key)
    except Exception:
        raise ValueError("❌ Incorrect old master password — cannot update.")

    new_salt = os.urandom(16)
    with open(SALT_FILE, "wb") as sf:
        sf.write(new_salt)

    new_derived_key = derive_key(new_password, new_salt)
    f_new = Fernet(new_derived_key)

    new_encrypted_vault_key = f_new.encrypt(vault_key)

    with open(KEY_FILE, "wb") as kf:
        kf.write(new_encrypted_vault_key)

    print("[✔] Master password updated successfully.")
