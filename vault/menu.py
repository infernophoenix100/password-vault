from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from vault.vault_options import (
    add_entry,
    view_specific_entry,
    delete_entry,
    view_all_entries,
    update_email,
    update_password,
    update_service,
)

console = Console()


def menu(master_password: str):
    """Main vault menu that reuses the provided master password."""
    while True:
        console.clear()
        console.print(Panel("[bold cyan]PASSWORD VAULT MENU[/bold cyan]"))

        console.print("""
[bold yellow]1.[/bold yellow] Add new entry  
[bold yellow]2.[/bold yellow] View specific entry  
[bold yellow]3.[/bold yellow] Delete an entry  
[bold yellow]4.[/bold yellow] View all passwords  
[bold yellow]5.[/bold yellow] Update service name  
[bold yellow]6.[/bold yellow] Update email  
[bold yellow]7.[/bold yellow] Update password  
[bold yellow]8.[/bold yellow] Exit
        """)

        choice = Prompt.ask("[green]Select an option[/green]", choices=[str(i) for i in range(1, 9)])

        if choice == "1":
            service = Prompt.ask("Service name")
            username = Prompt.ask("Username")
            email = Prompt.ask("Email")
            password = Prompt.ask("Password", password=True)
            add_entry(service, username, email, password, master_password)

        elif choice == "2":
            view_specific_entry(master_password)

        elif choice == "3":
            delete_entry()

        elif choice == "4":
            view_all_entries(master_password)

        elif choice == "5":
            update_service()

        elif choice == "6":
            update_email()

        elif choice == "7":
            update_password(master_password)

        elif choice == "8":
            console.print("[bold green]Goodbye![/bold green]")
            break

        if not Confirm.ask("\nReturn to main menu?", default=True):
            console.print("[bold red]Exiting...[/bold red]")
            break
