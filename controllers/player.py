import json

from utils.constants import PATH_DATA_JSON_FILE


class PlayerController:

    @staticmethod
    def add_player(player):
        """Add a player to the tournament"""
        with open(PATH_DATA_JSON_FILE, "r") as players_file:
            data = json.load(players_file)

        if player.national_id[0].isalpha():
            data["players"].append({
                "national_id": player.national_id,
                "last_name": player.last_name,
                "first_name": player.first_name
            })
            with open(PATH_DATA_JSON_FILE, "w") as players_file:
                json.dump(data, players_file, indent=4)
        else:
            print("Le format de l'identitifant national est incorrect.")
