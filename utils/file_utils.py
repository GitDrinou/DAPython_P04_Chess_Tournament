import json

from utils.constants import (PATH_DATA_TOURNAMENTS_JSON_FILE,
                             PATH_DATA_PLAYERS_JSON_FILE)


def read_file(path_file):
    """Read a file and return a list"""
    with open(path_file, "r") as f:
        data = json.load(f)
        if data:
            return data
        else:
            return None


def write_file(path_file, data):
    """Write data to a file"""
    with open(path_file, "w") as f:
        json.dump(data, f, indent=4)


def save_to_json(key, **kwargs):
    """Save specific (tournament or player) data to the json file"""

    if key == "tournaments":
        data = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        path = PATH_DATA_TOURNAMENTS_JSON_FILE
        data["tournaments"].append({
            "tournament_id": kwargs["tournament_id"],
            "name": kwargs["name"].upper(),
            "location": kwargs["location"].capitalize(),
            "start_date": str(kwargs["start_date"]),
            "end_date": str(kwargs["end_date"]),
            "description": kwargs["description"],
            "number_of_rounds": kwargs["number_of_rounds"],
            "round_number": kwargs["round_number"],
            "is_on_break": False,
            "players": [],
            "rounds": []
        })
    else:
        data = read_file(PATH_DATA_PLAYERS_JSON_FILE)
        path = PATH_DATA_PLAYERS_JSON_FILE
        data["players"].append({
            "national_id": kwargs["national_id"],
            "last_name": kwargs["last_name"].upper(),
            "first_name": kwargs["first_name"].capitalize(),
        })

    write_file(path, data)


def load_tournament(path_file):
    """Load the last tournament data from the json file"""
    with open(path_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        datas = data.get("tournaments", [])
        if datas:
            return data["tournaments"][-1]
        else:
            return None


def update_tournament(path_file, tournament_id, new_value):
    """Update the last tournament data from the json file"""
    data = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)

    for index, tournament in enumerate(data["tournaments"]):
        if tournament.get("tournament_id") == int(tournament_id):
            data["tournaments"][index] = new_value
            break

    write_file(path_file, data)
