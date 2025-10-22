"""Generates unique random strings for tokens or identifiers."""
import secrets

def unique_string(byte: int = 8) -> str:
    """Create a unique, URL-safe string using secure random bytes."""
    return secrets.token_urlsafe(byte)
