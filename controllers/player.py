import json
import re

from utils.constants import PATH_DATA_PLAYERS_JSON_FILE, \
    PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import save_to_json, update_tournament, read_json_file


class PlayerController:

    @staticmethod
    def check_format_national_id(national_id):
        """Check the format of the national id (1 letter + 5 numbers)"""
        if re.fullmatch(r'^[A-Za-z]\d{5}$', national_id):
            return national_id
        else:
            return None

    @staticmethod
    def check_player_is_exist(national_id):
        """Check if the national id is existed in JSON file"""
        with open(PATH_DATA_PLAYERS_JSON_FILE, "r") as json_file:
            data = json.load(json_file)

        for player in data["players"]:
            if player["national_id"] == national_id:
                return True
        return False

    def add(self, player):
        """Add a player to the tournament"""

        if self.check_format_national_id(player.national_id) is not None:
            # save round to JSON file
            data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
            last_tournament = data_tournaments["tournaments"][-1]
            last_tournament["players"].append({
                "national_id": player.national_id.capitalize(),
                "last_name": player.last_name.upper(),
                "first_name": player.first_name.capitalize(),
                "points": 0.0
            })

            update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                              last_tournament["tournament_id"],
                              last_tournament)

            if not self.check_player_is_exist(player.national_id):
                save_to_json("players",
                             national_id=player.national_id.capitalize(),
                             last_name=player.last_name.upper(),
                             first_name=player.first_name.capitalize())

            print("=====================================================")
            print("\nLe joueur a été inscrit au tournoi avec succès.")

        else:
            print("Le format de l'identitifant national est "
                  "incorrect.\nFormat attendu : 1 lettre + 5 chiffres")
