"""Entry point of the application."""
import json
import os

from controllers.player import PlayerController
from models.player import Player
from utils.constants import PATH_DATA_JSON_FILE
from utils.file_utils import read_file


def initialize():
    """Initialize the application."""
    default_json = {
        "players": [],
        "tournaments": [],
    }
    if not os.path.isfile(PATH_DATA_JSON_FILE):
        with open(PATH_DATA_JSON_FILE, "w", encoding="utf-8") as json_file:
            json.dump(default_json, json_file, indent=4)


def main():
    """Main entry point of the application."""
    print("Ajouter un nouveau joueur:")
    national_id = input("Saisissez son identifiant national: ")
    last_name = input("Saisissez son nom de famille: ")
    first_name = input("Saisissez son prénom: ")

    # add player to players
    player_controller = PlayerController()
    player_controller.add_player(Player(national_id, last_name, first_name))

    data = read_file(PATH_DATA_JSON_FILE)
    print(f"JSON Players: {len(data['players'])}")


if __name__ == "__main__":
    initialize()
    main()
