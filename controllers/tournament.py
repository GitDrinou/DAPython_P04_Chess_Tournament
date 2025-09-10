import random

from utils.constants import PATH_DATA_JSON_FILE
from utils.date_utils import validate_date, checks_dates
from utils.file_utils import read_file, save_to_json


class TournamentController:

    @staticmethod
    def add_new_tournament(tournament_detail, number_of_players):
        """Add a new tournament"""
        data = read_file(PATH_DATA_JSON_FILE)

        # automatic creation of the tournament id
        tournaments = data['tournaments']
        tournament_id = max(1, len(tournaments) + 1)

        # check if the number of rounds is empty or under de default number
        if (tournament_detail.number_of_rounds == ""
                or tournament_detail.number_of_rounds < 4):
            tournament_detail.number_of_rounds = 4
        else:
            tournament_detail.number_of_rounds = int(tournament_detail.
                                                     number_of_rounds)

        start_date = validate_date(tournament_detail.start_date)
        end_date = validate_date(tournament_detail.end_date)

        if (start_date and end_date) and checks_dates(start_date, end_date):

            # randomize players from data with default points to 0
            random_players = random.sample(data["players"],
                                           int(number_of_players))
            for player in random_players:
                player["points"] = 0

            save_to_json("tournaments",
                         tournament_id=tournament_id,
                         name=tournament_detail.name.upper(),
                         location=tournament_detail.location.capitalize(),
                         start_date=str(start_date),
                         end_date=str(end_date),
                         description=tournament_detail.description,
                         number_of_rounds=tournament_detail.number_of_rounds,
                         round_number=tournament_detail.round_number,
                         random_players=random_players
                         )
