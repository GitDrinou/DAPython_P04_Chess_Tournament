from controllers.round import RoundController
from utils.console_utils import ConsoleDisplayer
from utils.constants import MESSAGES


def tournament_is_finished(tournament):
    """Check if tournament is finished"""
    number_of_rounds = tournament["number_of_rounds"]
    rounds = tournament["rounds"]
    list_finished_rounds = RoundController().is_finished(rounds)
    counter = sum(obj["is_finished"] == "X" for obj in list_finished_rounds)

    if counter == int(number_of_rounds):
        ConsoleDisplayer.log(MESSAGES["congratulations"], level="INFO")
        return False
    else:
        return True
