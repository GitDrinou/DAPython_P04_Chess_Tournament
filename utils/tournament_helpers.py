from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from models.round_model import RoundModel
from utils.file_utils import read_json_file


def tournament_is_finished(tournament):
    """Check if tournament is finished
        Args:
            tournament (dict): tournament details
        Returns:
            bool: True if tournament is finished
    """
    number_of_rounds = tournament["number_of_rounds"]
    rounds = tournament["rounds"]
    list_finished_rounds = RoundModel().is_finished(rounds)
    counter = sum(
        obj["is_finished"] == "X" for obj in list_finished_rounds)

    if counter == int(number_of_rounds):
        return True
    else:
        return False


def get_tournament_details(tournament_id):
    """Get tournament details
        Args:
            tournament_id (int): tournament identifier
    """
    data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
    tournaments = data_tournaments["tournaments"]
    return next(
        (t for t in tournaments if t["tournament_id"] == tournament_id),
        None
    )
