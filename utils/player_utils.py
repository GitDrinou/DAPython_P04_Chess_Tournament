import json
import re

from utils.constants import PATH_DATA_PLAYERS_JSON_FILE


def check_format_national_id(national_id):
    """Check the format of the national id (1 letter + 5 numbers)"""
    if re.fullmatch(r'^[A-Za-z]\d{5}$', national_id):
        return national_id
    else:
        return None


def check_player_is_exist(national_id):
    """Check if the national id is existed in JSON file"""
    with open(PATH_DATA_PLAYERS_JSON_FILE, "r") as json_file:
        data = json.load(json_file)

    for player in data["players"]:
        if player["national_id"] == national_id:
            return {
                "last_name": player["last_name"],
                "first_name": player["first_name"],
            }
    return None
