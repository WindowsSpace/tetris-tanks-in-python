import json
import os
from pathlib import Path
from settings import DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT

localSave = False

if not localSave:
    appdata_route = os.environ.get("APPDATA")

    if appdata_route:
        SAVE_DIR = Path(appdata_route) / "Pixel Tanks"
    else:
        SAVE_DIR = Path.home() / ".pixel_tanks"

    SAVE_DIR.mkdir(parents=True, exist_ok=True)
else:
    SAVE_DIR = Path("saves")
    SAVE_DIR.mkdir(exist_ok=True)

DIRECTION_TO_NAME = {DIR_UP: "up", DIR_DOWN: "down", DIR_LEFT: "left", DIR_RIGHT: "right"}
NAME_TO_DIRECTION = {v: k for k, v in DIRECTION_TO_NAME.items()}

def save_game(slot, player, enemy_manager, game_state) -> None:
    data = {
        "player": {
            "grid_x": player.grid_x, "grid_y": player.grid_y,
            "direction": DIRECTION_TO_NAME[player.direction],
        },
        "enemies": [
            {"grid_x": e.grid_x, "grid_y": e.grid_y, "direction": DIRECTION_TO_NAME[e.direction]}
            for e in enemy_manager.enemies_group
        ],
        "stats": {
            "lives": game_state["lives"],
            "score": game_state["score"],
            "level": game_state["level"],
            "target": game_state["target_enemies"],
            "kills_this_level": game_state["kills_this_level"],
            "global_kills": game_state["global_kills"]
        }
    }
    filepath = SAVE_DIR / f"slot_{slot}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_game(slot):
    filepath = SAVE_DIR / f"slot_{slot}.json"
    if not filepath.exists():
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_save(slot) -> None:
    filepath = SAVE_DIR / f"slot_{slot}.json"
    if filepath.exists():
        os.remove(filepath)

def load_hi_score():
    filepath = SAVE_DIR / "hiscore.json"
    if not filepath.exists(): return 0
    with open(filepath, "r") as f:
        return json.load(f).get("hi_score", 0)

def save_hi_score(score) -> None:
    if score <= load_hi_score(): return
    filepath = SAVE_DIR / "hiscore.json"
    with open(filepath, "w") as f:
        json.dump({"hi_score": score}, f)
