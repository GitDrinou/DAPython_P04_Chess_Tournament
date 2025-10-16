from models.round import RoundModel


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
