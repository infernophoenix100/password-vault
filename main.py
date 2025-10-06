from vault.db import init_db
from vault.auth import (
    is_registered,
    register_master,
    login_master,
    change_master_password
)
from vault.menu import menu
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel

console = Console()

if __name__ == "__main__":
    init_db()

    if not is_registered():
        register_master()

    console.clear()
    console.print(Panel.fit("[bold cyan]🔐 PASSWORD VAULT ACCESS[/bold cyan]", border_style="cyan"))

    console.print("""
[bold yellow]1.[/bold yellow] Login  
[bold yellow]2.[/bold yellow] Change Master Password  
[bold yellow]3.[/bold yellow] Exit
    """)

    choice = Prompt.ask("[green]Select an option[/green]", choices=["1", "2", "3"])

    if choice == "1":
        if login_master():
            console.print("[bold green]✅ Access granted. Opening vault...[/bold green]")
            menu()
        else:
            console.print("[bold red][!] Access denied.[/bold red]")

    elif choice == "2":
        change_master_password()

    elif choice == "3":
        console.print("[bold red]Exiting...[/bold red]")
