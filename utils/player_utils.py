import json
import re

from core.constants import PATH_DATA_PLAYERS_JSON_FILE


def check_format_national_id(national_id):
    """Check the format of the national id (1 letter + 5 numbers)
        Args:
            national_id (str): National identifier entered by the user
        Returns:
            Bool: True if the format of the national id is correct,
            False otherwise
    """
    if re.fullmatch(r'^[A-Za-z]\d{5}$', national_id):
        return True
    else:
        return False


def check_player_is_exist(national_id):
    """Check if the national id is existed in JSON file
        Args:
            national_id (str): National identifier entered by the user
    """
    with open(PATH_DATA_PLAYERS_JSON_FILE, "r") as json_file:
        data = json.load(json_file)

    for player in data["players"]:
        if player["national_id"] == national_id:
            return {
                "national_id": player["national_id"],
                "last_name": player["last_name"],
                "first_name": player["first_name"],
                "birth_date": player["birth_date"]
            }
    return None
