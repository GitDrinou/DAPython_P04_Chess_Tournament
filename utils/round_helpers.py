from datetime import datetime

from core.constants import ALLOW_BYES, MESSAGES
from core.exceptions import RoundGenerationError


def validate_round_generation(selected_tournament):
    """Validate a round generation
        Args:
            selected_tournament (tournament): data for a tournament
    """
    number_of_rounds = int(selected_tournament["number_of_rounds"])

    if ALLOW_BYES:
        # If number of rounds is odd, players = rounds
        # if number of rounds id even, players = rounds - 1
        if number_of_rounds % 2 == 1:
            min_players = number_of_rounds
        else:
            min_players = number_of_rounds - 1
    else:
        # if no BYE, number of players must be even, and we round up
        # to the next even
        number_of_players = number_of_rounds + 1
        if number_of_players % 2 == 1:
            min_players = number_of_players
        else:
            min_players = number_of_players + 1

    total_players = len(selected_tournament["players"])
    if ((total_players < min_players)
            or total_players == 0):
        raise RoundGenerationError(
            f"{MESSAGES['invalide_number_of_players']} {min_players}"
        )

    today = datetime.today().date()
    start_date = datetime.strptime(selected_tournament["start_date"],
                                   "%d/%m/%Y")
    if start_date.date() > today:
        raise RoundGenerationError(MESSAGES["no_generate_due_to_date"])