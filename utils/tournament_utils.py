import json
from datetime import datetime

from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import read_json_file, write_json_file


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
