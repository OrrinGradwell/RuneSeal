import os
from pathlib import Path

from dotenv import load_dotenv

# Load from .env if present
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Defaults & constants
HOME_DIR = Path.home()
CONFIG_DIR = HOME_DIR / ".runeseal"
SESSION_FILE = CONFIG_DIR / "session.json"
DEFAULT_API_URL = os.getenv(
    "API_URL", f"http://localhost:{os.getenv('API_PORT', 8443)}"
)


def load_environment():
    """Ensure config directory exists and environment is loaded."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
