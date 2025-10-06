#!/usr/bin/env python3
from vault.db import init_db
from vault.auth import is_registered, register_master, login_master
from vault.menu import menu

if __name__ == "__main__":
    init_db()

    if not is_registered():
        register_master()

    if login_master():
        menu()
    else:
        print("[!] Access denied.")
