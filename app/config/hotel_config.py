import json
from pathlib import Path


def load_hotel_config(hotel_id):
    config_path = Path("hotels") / hotel_id / "config.json"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Nie znaleziono konfiguracji hotelu: {hotel_id}"
        )

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    return config