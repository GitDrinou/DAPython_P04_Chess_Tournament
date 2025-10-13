import json
from datetime import datetime

from core.constants import (PATH_DATA_TOURNAMENTS_JSON_FILE,
                            PATH_DATA_PLAYERS_JSON_FILE)


def read_json_file(path_file):
    """Read a JSON file and return a list
        Args:
            path_file (str): Path to the JSON file
    """
    with open(path_file, "r") as f:
        data = json.load(f)
        if data:
            return data
        else:
            return None


def write_json_file(path_file, data):
    """Write data to a JSON file
        Args:
            path_file (str): Path to the JSON file
            data (dict): Data to be written
    """
    with open(path_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_to_json(key, **kwargs):
    """Save specific (tournament or player) data to the json file
        Args:
            key (str): Key of the data to be saved (tournament or player)
            **kwargs: Data to be saved
    """

    if key == "tournaments":
        data = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        path = PATH_DATA_TOURNAMENTS_JSON_FILE
        data["tournaments"].append({
            "tournament_id": kwargs["tournament_id"],
            "name": kwargs["name"],
            "location": kwargs["location"],
            "start_date": kwargs["start_date"].strftime("%d/%m/%Y"),
            "end_date": kwargs["end_date"].strftime("%d/%m/%Y"),
            "description": kwargs["description"],
            "number_of_rounds": kwargs["number_of_rounds"],
            "round_number": kwargs["round_number"],
            "players": [],
            "rounds": []
        })
    else:
        data = read_json_file(PATH_DATA_PLAYERS_JSON_FILE)
        path = PATH_DATA_PLAYERS_JSON_FILE
        data["players"].append({
            "national_id": kwargs["national_id"],
            "last_name": kwargs["last_name"].upper(),
            "first_name": kwargs["first_name"].capitalize(),
            "birth_date": kwargs["birth_date"],
        })

    write_json_file(path, data)


def load_tournament(path_file, tournament_id=None, all_tournaments=False):
    """Load the last tournament data from the json file
        Args:
            path_file (str): Path to the JSON file
            tournament_id (str): Identifier of the tournament
            all_tournaments (bool): True to load all tournaments (by
            default = False)
    """
    with open(path_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        datas = data.get("tournaments", [])
        if datas:
            if tournament_id is not None:
                for tournament in datas:
                    if tournament["tournament_id"] == int(tournament_id):
                        return tournament
                return None
            else:
                tournaments = []
                if all_tournaments:
                    return datas
                else:
                    today = datetime.today().date()
                    for tournament in datas:
                        tournament_start = tournament["start_date"]
                        start_date = datetime.strptime(tournament_start,
                                                       "%d/%m/%Y"
                                                       ).date()
                        number_of_rounds = int(tournament["number_of_rounds"])
                        round_number = int(tournament["round_number"])
                        if (number_of_rounds > round_number and start_date
                                >= today):
                            tournaments.append(tournament)
                    return tournaments
        else:
            return None


def update_tournament(path_file, tournament_id, new_value):
    """Update the last tournament data from the json file
        Args:
            path_file (str): Path to the JSON file
            tournament_id (str): Identifier of the tournament
            new_value (str): New value for the tournament key
    """
    data = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)

    for index, tournament in enumerate(data["tournaments"]):
        if tournament.get("tournament_id") == int(tournament_id):
            data["tournaments"][index] = new_value
            break

    write_json_file(path_file, data)


def write_file(path_file, data):
    """Write data to a file
        Args:
            path_file (str): Path to the file
            data (dict): Data to be written
    """
    with open(path_file, "w", encoding="utf-8") as f:
        f.write(data)
