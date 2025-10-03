from datetime import datetime

from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import read_json_file, update_tournament


class RoundController:
    """Round controller class"""

    @staticmethod
    def start_up(tournament_id):
        """Method that starts a round."""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        for tournament in tournaments:
            if tournament["tournament_id"] == tournament_id:
                last_round = tournament["rounds"][-1]
                start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                tournament["round_number"] = last_round["name"][-1]
                last_round["round_start_date"] = start_date

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"],
                                  tournament)

                print("\n===================================================="
                      "=\nLe tour a démarré.\nLes joueurs peuvent commencer "
                      "leurs matchs.\n======================================="
                      "==============")

                return last_round
        return None

    @staticmethod
    def end_up(tournament_id):
        """Method that terminate the round."""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        for tournament in tournaments:
            if tournament["tournament_id"] == tournament_id:
                last_round = tournament["rounds"][-1]
                if last_round["round_start_date"] == "":
                    print("\n================================================")
                    print("Le tour n'a pas encore démarré.\nVous ne pouvez "
                          "pas terminer ce tour avant de l'avoir démarré.")
                    print("================================================")
                else:
                    end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                    tournament["round_number"] = last_round["name"][-1]
                    last_round["round_end_date"] = end_date

                    update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                      tournament["tournament_id"],
                                      tournament)

                    print("\n================================================")
                    print("Le tour est terminé.\nVous allez à présent être "
                          "invité à enregistrer les scores pour chaque "
                          "matchs du tour.")
                    print("\n================================================")

                    return last_round
        return None

    @staticmethod
    def is_finished(rounds):
        """Method that checks if the round is finished."""
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
