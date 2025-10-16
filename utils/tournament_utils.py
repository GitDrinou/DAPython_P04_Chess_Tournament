import json
from datetime import datetime

from utils.tournament_helpers import tournament_is_finished


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
        if not datas:
            return None

        today = datetime.today().date()
        tournaments = []

        for tournament in datas:
            if not tournament_is_finished(tournament):
                tournaments.append(tournament)
            else:
                tournament_start = tournament["start_date"]
                start_date = datetime.strptime(tournament_start,
                                               "%d/%m/%Y").date()
                if start_date >= today:
                    tournaments.append(tournament)

        if tournament_id is not None:
            tournament = next(
                (t for t in datas if t["tournament_id"] == int(
                    tournament_id)),
                None
            )
            return tournament

        if all_tournaments:
            return datas

    return tournaments

# def update_tournament(path_file, tournament_id, new_value):
#     """Update the last tournament data from the json file
#         Args:
#             path_file (str): Path to the JSON file
#             tournament_id (str): Identifier of the tournament
#             new_value (str): New value for the tournament key
#     """
#     data = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
#
#     for index, tournament in enumerate(data["tournaments"]):
#         if tournament.get("tournament_id") == int(tournament_id):
#             data["tournaments"][index] = new_value
#             break
#
#     write_json_file(path_file, data)
