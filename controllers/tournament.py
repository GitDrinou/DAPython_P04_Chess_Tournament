import random

from models.match import Match
from models.round import Round
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from utils.file_utils import read_json_file, save_to_json, update_tournament
from utils.console_utils import ConsoleDisplayer


class TournamentController:
    """Tournament controller class"""
    def __init__(self):
        self.historical_pairs = []

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

        return ConsoleDisplayer.log(MESSAGES["tournament_created"],
                                    level="INFO")

    def generate_a_round(self,  round_number, players,
                         tournament_id, round_id=None):
        """Generate a random tournament round"""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]

        for tournament in tournaments:
            count_matchs = 0
            total_matchs = 0
            count_round_ended = 0

            if round_id == 0 and tournament["tournament_id"] == tournament_id:

                # Count total of no ended rounds
                for round_detail in tournament["rounds"]:
                    if (round_detail["round_end_date"] == "" and
                            round_detail["round_start_date"] != "") or (
                            round_detail["round_start_date"] == "" and
                            round_detail["round_end_date"] == ""):
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
                    used_index = set()

                    for i in range(0, len(players)):
                        if i in used_index:
                            continue
                        player1 = players[i]
                        pair_found = False

                        for j in range(i + 1, len(players)):
                            if j in used_index:
                                continue

                            player2 = players[j]
                            pair = tuple(sorted((player1["national_id"],
                                                 player2["national_id"])))

                            if pair not in self.historical_pairs:
                                match = Match(id_match,
                                              player1=player1["national_id"],
                                              score1=0.0,
                                              player2=player2["national_id"],
                                              score2=0.0).to_dict()

                                round_detail.matches.append(match)
                                self.historical_pairs.append(pair)
                                id_match += 1
                                used_index.update((i, j))
                                pair_found = True
                                break

                        if not pair_found:
                            for j in range(i + 1, len(players)):
                                if j not in used_index:
                                    player2 = players[j]
                                    pair = tuple(sorted(
                                                    (player1["national_id"],
                                                     player2["national_id"])))
                                    match = Match(id_match,
                                                  player1=player1[
                                                      "national_id"],
                                                  score1=0.0,
                                                  player2=player2[
                                                      "national_id"],
                                                  score2=0.0).to_dict()
                                    round_detail.matches.append(match)
                                    self.historical_pairs.append(pair)
                                    id_match += 1
                                    used_index.update((i, j))
                                    break

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

                    ConsoleDisplayer.log(MESSAGES["round_generated"],
                                         level="INFO")
                    return tournament
                else:
                    ConsoleDisplayer.log(MESSAGES["no_generate_round"],
                                         level="WARNING")
                    return None
            else:
                if (round_id > 0 and tournament["tournament_id"] ==
                        tournament_id):
                    for round_detail in tournament["rounds"]:
                        if round_detail["round_id"] == round_id:
                            total_matchs += len(round_detail["matchs"])
                            for match in round_detail["matchs"]:
                                for player_id, score in match["match"]:
                                    if score == 0.0:
                                        count_matchs += 1

                            if (0 < count_matchs <= total_matchs or
                                    round_detail["round_start_date"] == ""):
                                return tournament
                            else:
                                ConsoleDisplayer.log(MESSAGES[
                                                      "round_already_ended"],
                                                     level="WARNING")
                                return None
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

                return ConsoleDisplayer.log(MESSAGES["points_updated"],
                                            level="INFO")
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

                return ConsoleDisplayer.log(MESSAGES["player_deleted"],
                                            level="INFO")
        return None
