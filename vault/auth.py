import sqlite3
import hashlib
import getpass
from vault.db import get_connection
from vault.security import generate_key, update_master_password


def hash_password(password: str) -> str:
    """Generate SHA-256 hash of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()


def is_registered() -> bool:
    """Check if a master password is already set."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM master")
    exists = c.fetchone()[0] > 0
    conn.close()
    return exists


def register_master():
    """Register a new master password if not already registered."""
    print("=== Register Master Password ===")
    while True:
        pw1 = getpass.getpass("Create master password: ")
        pw2 = getpass.getpass("Confirm master password: ")

        if pw1 != pw2:
            print("[!] Passwords do not match. Try again.")
            continue

        password_hash = hash_password(pw1)

        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO master (password_hash) VALUES (?)", (password_hash,))
        conn.commit()
        conn.close()

        generate_key(pw1)
        print("[+] Master password set successfully!")
        break


def login_master() -> bool:
    """Prompt for master password and verify it."""
    print("=== Master Login ===")
    pw = getpass.getpass("Enter master password: ")
    password_hash = hash_password(pw)

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM master LIMIT 1")
    stored_hash = c.fetchone()[0]
    conn.close()

    if password_hash == stored_hash:
        print("[✓] Login successful!")
        return True
    else:
        print("[!] Incorrect password.")
        return False


def change_master_password():
    """Update master password securely using old password verification."""
    print("=== Update Master Password ===")

    old_pw = getpass.getpass("Enter current master password: ")

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM master LIMIT 1")
    stored_hash = c.fetchone()[0]
    conn.close()

    if hash_password(old_pw) != stored_hash:
        print("[!] Incorrect current password. Cannot update.")
        return

    new_pw1 = getpass.getpass("Enter new master password: ")
    new_pw2 = getpass.getpass("Confirm new master password: ")

    if new_pw1 != new_pw2:
        print("[!] Passwords do not match. Try again.")
        return

    try:
        update_master_password(old_pw, new_pw1)
    except ValueError as e:
        print(f"[!] Error: {e}")
        return

    new_hash = hash_password(new_pw1)
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE master SET password_hash = ? WHERE id = 1", (new_hash,))
    conn.commit()
    conn.close()

    print("[✔] Master password updated successfully.")
