"""Configuration module for srt-translator."""

import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Define constants
CONFIG_DIR = Path.home() / ".srt-translator"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_api_key(api_key_arg: Optional[str] = None) -> str:
    """
    Load the OpenAI API key from various sources in order of precedence:
    1. Command-line argument
    2. Environment variable
    3. .env file
    4. Config file

    Args:
        api_key_arg: API key provided via command-line argument

    Returns:
        str: The API key
    """
    # 1. Check command-line argument
    if api_key_arg:
        return api_key_arg

    # 2. Check environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    # 3. Check .env file
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    # 4. Check config file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                api_key = config.get("api_key")
                if api_key:
                    return api_key
        except (json.JSONDecodeError, IOError):
            pass

    return ""


def save_api_key(api_key: str) -> None:
    """
    Save the API key to the config file.

    Args:
        api_key: The API key to save
    """
    # Create config directory if it doesn't exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Read existing config if it exists
    config = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # Update config with new API key
    config["api_key"] = api_key

    # Write config back to file
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
