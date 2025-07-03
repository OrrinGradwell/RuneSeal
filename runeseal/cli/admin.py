from pathlib import Path

import requests
import typer
import yaml
from rich import print

from runeseal.config import DEFAULT_API_URL

app = typer.Typer(help="🛠️ Administrative commands for RuneSeal")


@app.command("init")
def init_admin(
    from_file: Path = typer.Option(
        ..., "--from-file", "-f", help="Path to YAML file with initial passwords"
    ),
    api_url: str = typer.Option(
        DEFAULT_API_URL, "--api-url", "-u", help="Vault API base URL"
    ),
):
    """
    Bootstrap the first admin and system password into RuneSeal.
    """
    print("[bold green]🔧 Initializing RuneSeal Vault...[/bold green]")

    if not from_file.exists():
        print(f"[red]❌ File not found: {from_file}[/red]")
        raise typer.Exit(code=1)

    try:
        with open(from_file, "r") as f:
            secrets = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"[red]⚠️ Failed to parse YAML: {e}[/red]")
        raise typer.Exit(code=1)

    try:
        response = requests.post(f"{api_url}/admin/init", json=secrets)
        response.raise_for_status()
        print("[green]✅ RuneSeal initialized successfully.[/green]")
    except requests.exceptions.RequestException as e:
        print(f"[red]❌ Init failed: {e}[/red]")
        raise typer.Exit(code=1)
