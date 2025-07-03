import typer

from runeseal.cli import admin, auth, secrets
from runeseal.config import load_environment

app = typer.Typer(name="RuneSeal CLI", help="🔐 RuneSeal ▸ Secure Secrets Vault")

# Subcommands
app.add_typer(auth.app, name="login")
app.add_typer(admin.app, name="admin")
app.add_typer(secrets.app, name="secret")


@app.callback()
def main():
    """RuneSeal CLI Entry"""
    load_environment()


if __name__ == "__main__":
    app()
