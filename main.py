"""Entry point of the application."""
import json
import os
import random
from datetime import datetime

from controllers.player import PlayerController
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from utils.constants import PATH_DATA_JSON_FILE


def initialize():
    """Initialize the application."""
    default_json = {
        "players": [],
        "tournaments": [],
    }
    if not os.path.isfile(PATH_DATA_JSON_FILE):
        with open(PATH_DATA_JSON_FILE, "w", encoding="utf-8") as json_file:
            json.dump(default_json, json_file, indent=4)
    # else:
    #     with open(PATH_DATA_JSON_FILE, "r", encoding="utf-8") as json_file:
    #         default_json = json.load(json_file)



def main():
    """Main entry point of the application."""
    print("Ajouter un nouveau joueur:")
    national_id = input("Saisissez son identifiant national: ")
    last_name = input("Saisissez son nom de famille: ")
    first_name = input("Saisissez son prénom: ")


    # add player to players
    player_controller = PlayerController()
    player_controller.add_player(Player(national_id, last_name, first_name))



if __name__ == "__main__":
    initialize()
    main()
