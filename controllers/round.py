from datetime import datetime

from utils.console_utils import ConsoleDisplayer
from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from utils.file_utils import read_json_file, update_tournament


class RoundController:
    """Round controller class"""

    @staticmethod
    def end_up(tournament_id, round_id):
        """Method that terminates a round
            Args:
                tournament_id (int): Identifier of a specific tournament
                round_id (int): Identifier of a specific round
            Returns:
                round_item (round): round details
        """
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )

        if tournament:
            rounds = tournament["rounds"]
            round_ = next(
                (r for r in rounds if r["round_id"] == round_id),
                None
            )

            end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            round_item = {}
            if round_:
                if round_["round_start_date"] == "":
                    ConsoleDisplayer.log(MESSAGES["round_not_started"],
                                         level="WARNING")
                else:
                    round_["round_end_date"] = end_date

                    update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                      tournament["tournament_id"], tournament)

                    round_item = round_

                    ConsoleDisplayer.log(MESSAGES["round_ended"], level="INFO")
            else:
                last_round = tournament["rounds"][-1]
                last_round["round_end_date"] = end_date

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"], tournament)

                round_item = last_round

                ConsoleDisplayer.log(MESSAGES["round_ended"], level="INFO")

            return round_item
        else:
            return None

    @staticmethod
    def is_finished(rounds):
        """Method that checks if a round is finished or not..
            Args:
                rounds (list): list of rounds
            Returns:
                list_finished_rounds (list): round list finished or not.
        """
        list_finished_rounds = []

        count_match = 0
        for round_detail in rounds:
            for match_detail in round_detail["matchs"]:
                player1_id, player1_score = match_detail["match"][0]
                player2_id, player2_score = match_detail["match"][1]
                player1_score = float(player1_score)
                player2_score = float(player2_score)

                if player1_score == 0.0 and player2_score == 0.0:
                    count_match += 1

            if (count_match == len(round_detail["matchs"])
                    or round_detail["round_end_date"] == ""):
                list_finished_rounds.append({
                    "round_id": round_detail["round_id"],
                    "is_finished": ""
                })
            else:
                list_finished_rounds.append({
                    "round_id": round_detail["round_id"],
                    "is_finished": "X"
                })

        return list_finished_rounds
