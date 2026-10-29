import json
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
name_game_file = current_dir / "name-project-page.txt"

with open(name_game_file, "r", encoding="utf-8") as file:
    name_game = file.read()

data = {
    "name": name_game,
    "version": "1.0.0"
}

with open("resources/app/package.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)