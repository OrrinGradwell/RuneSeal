import json
import requests
import typer

from rich import print
from runeseal.config import DEFAULT_API_URL, SESSION_FILE

app = typer.Typer(help="🔑 Manage secrets in RuneSeal")

def load_session():
    if not SESSION_FILE.exists():
        print("[red]❌ No session found. Please log in first.[/red]")
        raise typer.Exit(code=1)
    return json.loads(SESSION_FILE.read_text())

@app.command("add")
def add_secret(
    key: str = typer.Option(..., "--key", "-k", help="Secret key name"),
    value: str = typer.Option(..., "--value", "-v", help="Secret value to store"),
    api_url: str = typer.Option(
        DEFAULT_API_URL, "--api-url", "-u", help="Vault API URL"
    ),
):
    """Store a new secret (key-value pair) in the vault."""
    token_data = load_session()
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "X-API-Key": token_data.get("api_key", ""),
    }
    payload = {"key": key, "value": value}

    try:
        response = requests.post(f"{api_url}/secrets", json=payload, headers=headers)
        response.raise_for_status()
        print(f"[green]✅ Secret '{key}' stored successfully.[/green]")
    except requests.exceptions.RequestException as e:
        print(f"[red]❌ Failed to store secret: {e}[/red]")
        raise typer.Exit(code=1)

@app.command("list")
def list_secrets(
    api_url: str = typer.Option(
        DEFAULT_API_URL, "--api-url", "-u", help="Vault API URL"
    )
):
    """Retrieve all keys for the current user."""
    token_data = load_session()
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "X-API-Key": token_data.get("api_key", ""),
    }

    try:
        response = requests.get(f"{api_url}/secrets", headers=headers)
        response.raise_for_status()
        secrets = response.json()
        print("[cyan]📜 Your Secrets:[/cyan]")
        for s in secrets:
            print(f" - {s['key']}")
    except requests.exceptions.RequestException as e:
        print(f"[red]❌ Failed to list secrets: {e}[/red]")
        raise typer.Exit(code=1)

@app.command("delete")
def delete_secret(
    key: str = typer.Option(..., "--key", "-k", help="Key of the secret to delete"),
    api_url: str = typer.Option(
        DEFAULT_API_URL, "--api-url", "-u", help="Vault API URL"
    ),
):
    """Delete a stored secret."""
    token_data = load_session()
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "X-API-Key": token_data.get("api_key", ""),
    }

    try:
        response = requests.delete(f"{api_url}/secrets/{key}", headers=headers)
        response.raise_for_status()
        print(f"[green]🗑️ Secret '{key}' deleted.[/green]")
    except requests.exceptions.RequestException as e:
        print(f"[red]❌ Failed to delete secret: {e}[/red]")
        raise typer.Exit(code=1)
