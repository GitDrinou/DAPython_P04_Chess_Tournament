import random

from models.match import Match
from models.round import Round
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import read_file, save_to_json, update_last_tournament


class TournamentController:
    """Tournament controller class"""

    @staticmethod
    def add_new_tournament(tournament_detail):
        """Add a new tournament"""
        data_tournaments = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments['tournaments']
        tournament_id = max(1, len(tournaments) + 1)

        # check if the number of rounds is empty or under de default number
        if (tournament_detail.number_of_rounds == "" or int(
                tournament_detail.number_of_rounds) < 4):
            tournament_detail.number_of_rounds = 4

        save_to_json("tournaments",
                     tournament_id=tournament_id,
                     name=tournament_detail.name.upper(),
                     location=tournament_detail.location.capitalize(),
                     start_date=str(tournament_detail.start_date),
                     end_date=str(tournament_detail.end_date),
                     description=tournament_detail.description,
                     number_of_rounds=tournament_detail.number_of_rounds,
                     round_number=tournament_detail.round_number,
                     players=[]
                     )

        message = ("Le nouveau tournoi a été enregistré avec succès.\n"
                   "Vous pouvez à présent générer le premier tour.")
        return print("---------------------------\n" + message)

    @staticmethod
    def generate_round(number_of_rounds, round_number, players):
        """Generate a random tournament round"""
        data_tournaments = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data_tournaments["tournaments"][-1]

        if int(round_number) == int(number_of_rounds):
            return print("Vous avez atteint le nombre de tours pour ce "
                         "tournoi.")

        round_number += 1
        round_name = "Round {}".format(round_number)
        round_detail = Round(round_number, round_name)

        if round_number == 1:
            random.shuffle(players)
        else:
            players.sort(key=lambda player: player["points"], reverse=True)

        id_match = 1

        for i in range(0, len(players), 2):
            player1 = {
                "national_id": players[i]["national_id"]
            }
            player2 = {
                "national_id": players[i+1]["national_id"]
            }
            match = Match(id_match, player1=player1["national_id"],
                          score1=0.0, player2=player2["national_id"],
                          score2=0.0).to_dict()

            id_match += 1
            round_detail.matches.append(match)

        data_round = {
            "round_id": round_number,
            "name": round_name,
            "round_start_date": str(round_detail.start_date),
            "round_end_date": str(round_detail.end_date),
            "matchs": round_detail.matches
        }

        last_tournament["rounds"].append(data_round)

        # save round to JSON file
        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                               last_tournament["tournament_id"],
                               last_tournament)

        return print("Le tour a été généré et enregistré avec succès.")

    @staticmethod
    def update_player_points(round_id):
        """Update player's points"""
        data = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data["tournaments"][-1]
        players = {player["national_id"]: player for player in
                   last_tournament["players"]}

        for round_detail in last_tournament["rounds"]:
            if round_detail.get("round_id") == int(round_id):
                for match_detail in round_detail["matchs"]:
                    player1_id, player1_score = match_detail["match"][0]
                    player2_id, player2_score = match_detail["match"][1]
                    player1_score = float(player1_score)
                    player2_score = float(player2_score)

                    # Points conditions (win = 1, lose = 0, draw = 0,5)
                    if player1_score == player2_score:
                        players[player1_id]["points"] += 0.5
                        players[player2_id]["points"] += 0.5
                    else:
                        if player1_score > player2_score:
                            players[player1_id]["points"] += 1
                        else:
                            players[player2_id]["points"] += 1

        # save update to json file
        for player in last_tournament["players"]:
            if player["national_id"] == players[player["national_id"]][
                            "national_id"]:
                player["points"] = players[player["national_id"]]["points"]

        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                               last_tournament["tournament_id"],
                               last_tournament)

        return print("Les points ont été mis à jour.\nVous allez être "
                     "redirigé vers le menu de gestion du tournoi.")

    @staticmethod
    def break_tournament(tournament_id):
        """Make a break for a tournament"""
        data = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data["tournaments"][-1]
        if last_tournament["tournament_id"] == tournament_id:
            last_tournament["is_on_break"] = True

        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                               tournament_id, last_tournament)

        return print("\nLe tournoi est en pause.\nVous allez être redirigé "
                     "vers le menu principal de l'application.")

    @staticmethod
    def unbreak_tournament(tournament_id):
        """Unbreak the tournament"""
        data = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data["tournaments"][-1]
        if last_tournament["tournament_id"] == tournament_id:
            last_tournament["is_on_break"] = False

        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                               tournament_id, last_tournament)

    @staticmethod
    def delete_a_player(tournament_id, national_id):
        """Delete an identify player from the tournament"""
        data = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data["tournaments"][-1]
        if last_tournament["tournament_id"] == tournament_id:
            last_tournament["players"] = [player for player in last_tournament[
                "players"] if player.get('national_id') != national_id]

            update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                   last_tournament["tournament_id"],
                                   last_tournament)

        return print("\nLe joueur a bien été supprimé.")
