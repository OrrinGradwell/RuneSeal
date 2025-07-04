import json
import requests
import typer

from getpass import getpass
from rich import print
from runeseal.config import DEFAULT_API_URL, SESSION_FILE

app = typer.Typer(help="🔐 Log in to your RuneSeal vault")

@app.command("login")
def login(
    api_url: str = typer.Option(
        DEFAULT_API_URL, "--api-url", "-u", help="Vault API base URL"
    )
):
    """Authenticate with RuneSeal and store session info locally."""
    print("[bold cyan]🔐 RuneSeal Login[/bold cyan]")
    username = typer.prompt("Username")
    password = getpass("Password: ")

    payload = {"username": username, "password": password}
    try:
        response = requests.post(f"{api_url}/auth/login", json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("[red]❌ Login failed: Invalid credentials or connection issue.[/red]")
        raise typer.Exit(code=1)

    token = response.json()
    SESSION_FILE.write_text(json.dumps(token, indent=2))
    print(f"[green]✅ Logged in as [bold]{username}[/bold]. Session saved.[/green]")
