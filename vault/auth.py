import sqlite3
import hashlib
import getpass
from vault.db import get_connection
from vault.security import generate_key

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def is_registered() -> bool:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM master")
    exists = c.fetchone()[0] > 0
    conn.close()
    return exists

def register_master():
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
