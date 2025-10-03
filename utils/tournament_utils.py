from controllers.round import RoundController
from views.messages import message_tournament_terminated


def tournament_is_finished(tournament):
    """Check if tournament is finished"""
    number_of_rounds = tournament["number_of_rounds"]
    round_number = tournament["round_number"]
    rounds = tournament["rounds"]
    list_finished_rounds = RoundController().is_finished(rounds)
    existe_false = any(item['is_finished'] is False for item in
                       list_finished_rounds)

    if not existe_false and number_of_rounds == round_number:
        return print(message_tournament_terminated)
    else:
        return None
