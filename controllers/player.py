import json

from utils.constants import PATH_DATA_JSON_FILE


class PlayerController:

    @staticmethod
    def check_format_national_id(national_id):
        """Check the format of the national id (1 letter + 5 numbers)"""
        if national_id[0].isalpha() and national_id[1:].isdigit():
            return national_id.upper()
        else:
            return None

    def add_player(self, player):
        """Add a player to the tournament"""
        with open(PATH_DATA_JSON_FILE, "r") as players_file:
            data = json.load(players_file)

        if self.check_format_national_id(player.national_id) is not None:
            data["players"].append({
                "national_id": player.national_id,
                "last_name": player.last_name.upper(),
                "first_name": player.first_name
            })
            with open(PATH_DATA_JSON_FILE, "w") as players_file:
                json.dump(data, players_file, indent=4)
        else:
            print("Le format de l'identitifant national est "
                  "incorrect.\nFormat attendu : 1 lettre + 5 chiffres")
