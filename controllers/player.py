import json
import random
import re
import string

from utils.constants import PATH_DATA_JSON_FILE
from utils.file_utils import read_file, write_file


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
        """Check if the national id is exist in JSON file"""
        with open(PATH_DATA_JSON_FILE, "r") as json_file:
            data = json.load(json_file)

        for player in data["players"]:
            if player["national_id"] == national_id:
                return True
        return False

    def add_player(self, player):
        """Add a player to the tournament"""
        data = read_file(PATH_DATA_JSON_FILE)

        # automatic creation of the national identifiant
        letter = random.choice(string.ascii_uppercase)
        numbers = ''.join(random.choices(string.digits, k=5))
        national_id = letter + numbers
        if self.check_format_national_id(national_id) is not None:
            if not self.check_player_is_exist(national_id):
                data["players"].append({
                    "national_id": national_id,
                    "last_name": player.last_name.upper(),
                    "first_name": player.first_name.capitalize(),
                })

                write_file(PATH_DATA_JSON_FILE, data)

            else:
                print("Ce joueur existe déjà dans la base des joueurs "
                      "d'échecs.")
        else:
            print("Le format de l'identitifant national est "
                  "incorrect.\nFormat attendu : 1 lettre + 5 chiffres")
