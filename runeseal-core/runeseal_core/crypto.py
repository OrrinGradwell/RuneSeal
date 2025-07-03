import os

from cryptography.fernet import Fernet

FERNET_SECRET = os.getenv("SYSTEM_PASSWORD", "changeme_this_is_dev_only").encode()


def _get_cipher():
    # Derive Fernet-compatible key (must be 32 url-safe base64 bytes)
    from base64 import urlsafe_b64encode

    padded = FERNET_SECRET.ljust(32, b"0")[:32]
    return Fernet(urlsafe_b64encode(padded))


def encrypt(text: str) -> str:
    cipher = _get_cipher()
    return cipher.encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    cipher = _get_cipher()
    return cipher.decrypt(token.encode()).decode()
