import json
from typing import Any


def load(filename: str = "config") -> Any:
    try:
        with open(f"{filename}.json", "r", encoding="UTF-8") as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Failed to locate configuration file {filename}.json")
