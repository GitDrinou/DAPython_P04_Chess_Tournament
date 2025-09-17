import random

from models.match import Match
from models.round import Round
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, \
    PATH_DATA_PLAYERS_JSON_FILE
from utils.date_utils import validate_date, checks_dates
from utils.file_utils import read_file, save_to_json


class TournamentController:
    """Tournament controller class"""

    @staticmethod
    def add_new_tournament(tournament_detail, number_of_players):
        """Add a new tournament"""
        data_tournaments = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        data_players = read_file(PATH_DATA_PLAYERS_JSON_FILE)

        # automatic creation of the tournament id
        tournaments = data_tournaments['tournaments']
        tournament_id = max(1, len(tournaments) + 1)

        # check if the number of rounds is empty or under de default number
        if (tournament_detail.number_of_rounds == ""
                or int(tournament_detail.number_of_rounds) < 4):
            tournament_detail.number_of_rounds = 4

        start_date = validate_date(tournament_detail.start_date)
        end_date = validate_date(tournament_detail.end_date)

        if (start_date and end_date) and checks_dates(start_date, end_date):

            # randomize players from data with default points to 0
            random_players = random.sample(data_players["players"],
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
                         players=random_players
                         )

            message = "Le nouveau tournoi a été enregistré avec succès."
            return print("---------------------------\n" + message)
        else:
            return print("L'enregistrement du tournoi n'a pas abouti. "
                         "Veuillez renouveler votre saisie.")

    @staticmethod
    def generate_round(number_of_rounds, round_number, players):
        """Generate a random tournament round"""
        match = None

        if int(round_number) > int(number_of_rounds):
            return None

        round_number += 1
        round_name = "Round {}".format(round_number)
        round_detail = Round(round_name)

        if round_number == 1:
            random.shuffle(players)
        else:
            players.sort(key=lambda player: player["points"], reverse=True)
        id_match = 1
        for i in range(0, len(players), 2):
            player1 = {
                "national_id": players[i]["national_id"],
                "points": players[i + 1]["points"]
            }
            player2 = {
                "national_id": players[i+1]["national_id"],
                "points": players[i+1]["points"]
            }
            match = Match(id_match, player1=player1["national_id"],
                          score1=player1[
                "points"], player2=player2["national_id"],
                          score2=player2["points"]).to_dict()

            id_match += 1
            round_detail.matches.append(match)

        return {
                "name": round_name,
                "round_start_date": str(round_detail.start_date),
                "round_end_date": str(round_detail.end_date),
                "matchs": round_detail.matches
            }
