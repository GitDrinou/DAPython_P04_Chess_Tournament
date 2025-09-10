import random

from utils.constants import PATH_DATA_JSON_FILE
from utils.date_utils import validate_date, checks_dates
from utils.file_utils import read_file, write_file


class TournamentController:

    @staticmethod
    def add_tournament(tournament, number_of_players):
        """Add a new tournament"""
        data = read_file(PATH_DATA_JSON_FILE)

        # automatic creation of the tournament id
        tournaments = data['tournaments']

        if len(tournaments) == 0:
            tournament_id = 1
        else:
            tournament_id = len(tournaments) + 1

        if tournament.number_of_rounds == "":
            tournament.number_of_rounds = 4
        else:
            tournament.number_of_rounds = int(tournament.number_of_rounds)

        start_date = validate_date(tournament.start_date)
        end_date = validate_date(tournament.end_date)

        if (start_date and end_date) and checks_dates(start_date, end_date):

            random_players = random.sample(data["players"],
                                           int(number_of_players))

            data["tournaments"].append({
                "tournament_id": tournament_id,
                "name": tournament.name.upper(),
                "location": tournament.location.capitalize(),
                "start_date": str(start_date),
                "end_date": str(end_date),
                "description": tournament.description,
                "number_of_rounds": tournament.number_of_rounds,
                "round_number": tournament.round_number,
                "players": random_players
            })

            write_file(PATH_DATA_JSON_FILE, data)
