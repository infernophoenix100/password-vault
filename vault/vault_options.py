# vault/vault_ops.py
import sqlite3
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from vault.security import encrypt_password, decrypt_password

console = Console()


def add_entry(service, username, email, password):
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    encrypted = encrypt_password(password)
    c.execute("INSERT INTO vault (service, username, email, password) VALUES (?, ?, ?, ?)",
              (service, username, email, encrypted))
    conn.commit()
    conn.close()
    console.print(f"[bold green]✅ Added credentials for {service}.[/bold green]")


def list_services():
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("SELECT id, service, username, email FROM vault")
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print("[bold red]Vault is empty.[/bold red]")
        return []

    table = Table(title="Stored Accounts", show_lines=True)
    table.add_column("ID", justify="center")
    table.add_column("Service")
    table.add_column("Username")
    table.add_column("Email")

    for id, service, username, email in rows:
        table.add_row(str(id), service, username, email)

    console.print(table)
    return rows


def view_specific_entry():
    rows = list_services()
    if not rows:
        return

    entry_id = Prompt.ask("Enter ID of service to view")
    if not entry_id.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("SELECT service, username, email, password FROM vault WHERE id = ?", (entry_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        console.print("[bold red]No entry found with that ID.[/bold red]")
        return

    service, username, email, encrypted = row
    decrypted = decrypt_password(encrypted)

    panel_text = (
        f"[bold yellow]Service:[/bold yellow] {service}\n"
        f"[bold yellow]Username:[/bold yellow] {username}\n"
        f"[bold yellow]Email:[/bold yellow] {email}\n"
        f"[bold yellow]Password:[/bold yellow] [green]{decrypted}[/green]"
    )

    console.print(Panel(panel_text, title="Entry Details", expand=False, border_style="cyan"))


def delete_entry():
    rows = list_services()
    if not rows:
        return

    entry_id = Prompt.ask("Enter ID of entry to delete")
    if not entry_id.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    confirm = Confirm.ask(f"Are you sure you want to delete entry ID {entry_id}?")
    if not confirm:
        console.print("[bold yellow]Deletion cancelled.[/bold yellow]")
        return

    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("DELETE FROM vault WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

    console.print(f"[bold red]❌ Deleted entry {entry_id}.[/bold red]")


def view_all_entries():
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("SELECT id, service, username, email, password FROM vault")
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print("[bold red]Vault is empty.[/bold red]")
        return

    table = Table(title="Stored Passwords", show_lines=True)
    table.add_column("ID", justify="center")
    table.add_column("Service")
    table.add_column("Username")
    table.add_column("Email")
    table.add_column("Password")

    for id, service, username, email, encrypted in rows:
        decrypted = decrypt_password(encrypted)
        table.add_row(str(id), service, username, email, decrypted)

    console.print(table)
def update_service():
    rows = list_services()
    if not rows:
        return

    entry_id = Prompt.ask("Enter ID of entry to update service")
    if not entry_id.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    new_service = Prompt.ask("Enter new service name")
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("UPDATE vault SET service = ? WHERE id = ?", (new_service, entry_id))
    conn.commit()
    conn.close()

    console.print(f"[bold green]✅ Updated service name for entry ID {entry_id}.[/bold green]")


def update_email():
    rows = list_services()
    if not rows:
        return

    entry_id = Prompt.ask("Enter ID of entry to update email")
    if not entry_id.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    new_email = Prompt.ask("Enter new email")
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("UPDATE vault SET email = ? WHERE id = ?", (new_email, entry_id))
    conn.commit()
    conn.close()

    console.print(f"[bold green]✅ Updated email for entry ID {entry_id}.[/bold green]")


def update_password():
    rows = list_services()
    if not rows:
        return

    entry_id = Prompt.ask("Enter ID of entry to update password")
    if not entry_id.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    new_password = Prompt.ask("Enter new password", password=True)
    encrypted = encrypt_password(new_password)

    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("UPDATE vault SET password = ? WHERE id = ?", (encrypted, entry_id))
    conn.commit()
    conn.close()

    console.print(f"[bold green]✅ Updated password for entry ID {entry_id}.[/bold green]")
