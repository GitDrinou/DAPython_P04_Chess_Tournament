import random

from models.match import Match
from models.round import Round
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import read_json_file, save_to_json, update_tournament
from views.messages import message_rounds_reached, message_round_generated, \
    message_round_not_generated


class TournamentController:
    """Tournament controller class"""

    @staticmethod
    def create(tournament_detail):
        """Create a new tournament"""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
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
                     start_date=tournament_detail.start_date,
                     end_date=tournament_detail.end_date,
                     description=tournament_detail.description,
                     number_of_rounds=tournament_detail.number_of_rounds,
                     round_number=tournament_detail.round_number,
                     players=[]
                     )

        return print("\n===================================================="
                     "=\nLe nouveau tournoi a été créé avec "
                     "succès.\nVous allez être redirigé vers le menu "
                     "principal de l'application.\n=========================="
                     "===========================")

    @staticmethod
    def generate_a_round(number_of_rounds, round_number, players,
                         tournament_id, round_id=None):
        """Generate a random tournament round"""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]

        for tournament in tournaments:
            count_matchs = 0
            total_matchs = 0
            count_round_ended = 0
            if round_id == 0 and tournament["tournament_id"] == tournament_id:
                if int(round_number) == int(number_of_rounds):
                    return print(message_rounds_reached)

                for round_detail in tournament["rounds"]:
                    if (round_detail["round_end_date"] == "" and
                            round_detail["round_start_date"] != ""):
                        count_round_ended += 1

                if count_round_ended == 0:
                    round_number += 1
                    round_name = "Round {}".format(round_number)
                    round_detail = Round(round_number, round_name)

                    if round_number == 1:
                        random.shuffle(players)
                    else:
                        players.sort(key=lambda player: (player["points"],
                                                         random.random()),
                                     reverse=True)

                    id_match = 1
                    historical_pairs = []

                    for i in range(0, len(players), 2):
                        player1 = {"national_id": players[i]["national_id"]}
                        player2 = {"national_id": players[i+1]["national_id"]}
                        pair = tuple(sorted((player1["national_id"], player2[
                            "national_id"])))
                        if pair not in historical_pairs:
                            match = Match(id_match, player1=player1[
                                "national_id"], score1=0.0, player2=player2[
                                "national_id"], score2=0.0).to_dict()

                            id_match += 1
                            round_detail.matches.append(match)
                            historical_pairs.append(pair)

                    data_round = {
                        "round_id": round_number,
                        "name": round_name,
                        "round_start_date": str(round_detail.start_date),
                        "round_end_date": str(round_detail.end_date),
                        "matchs": round_detail.matches
                    }

                    tournament["rounds"].append(data_round)

                    update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                      tournament["tournament_id"],
                                      tournament)

                    print(message_round_generated)
                    return tournament
                else:
                    print(message_round_not_generated)
                    return None
            else:
                if (round_id > 0 and tournament["tournament_id"] ==
                        tournament_id):
                    for round_detail in tournament["rounds"]:
                        total_matchs += len(round_detail["matchs"])
                        for match in round_detail["matchs"]:
                            for player_id, score in match["match"]:
                                if score == 0.0:
                                    count_matchs += 1

                    if count_matchs <= total_matchs:
                        return tournament
        return None

    @staticmethod
    def update_player_points(tournament_id, round_id):
        """Update player's points"""
        data = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data["tournaments"]
        for tournament in tournaments:
            if tournament["tournament_id"] == tournament_id:
                players = {
                    player["national_id"]: player for player in tournament[
                        "players"]
                }

                for round_detail in tournament["rounds"]:
                    if round_detail.get("round_id") == int(round_id):
                        for match_detail in round_detail["matchs"]:
                            player1_id, player1_score = match_detail[
                                "match"][0]
                            player2_id, player2_score = match_detail[
                                "match"][1]
                            player1_score = float(player1_score)
                            player2_score = float(player2_score)

                            if player1_score == player2_score:
                                players[player1_id]["points"] += 0.5
                                players[player2_id]["points"] += 0.5
                            else:
                                if player1_score > player2_score:
                                    players[player1_id]["points"] += 1
                                else:
                                    players[player2_id]["points"] += 1

                # save to json file
                for player in tournament["players"]:
                    if player["national_id"] == players[player["national_id"]][
                                    "national_id"]:
                        player["points"] = players[player["national_id"]][
                            "points"]

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"],
                                  tournament)

                return print("\n=============================================="
                             "=======\nLes points ont été mis à jour.\nVous "
                             "allez être redirigé vers le menu de gestion "
                             "du tournoi.\n==================================="
                             "==================")
        return None

    @staticmethod
    def delete_a_player(tournament_id, national_id):
        """Delete an identify player from the tournament"""
        data = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data["tournaments"]
        for tournament in tournaments:
            if tournament["tournament_id"] == tournament_id:
                tournament["players"] = [player for player in tournament[
                    "players"] if player.get('national_id') != national_id]

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"],
                                  tournament)

                return print("\n=============================================="
                             "=======\nLe joueur a bien été supprimé du "
                             "tournoi.\n======================================"
                             "============")
        return None
