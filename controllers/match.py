from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import update_last_tournament


class MatchController:
    """Match controller class"""

    @staticmethod
    def save_score(last_tournament, round_id, user_match_id, score1, score2):
        """ Update score for specific match """
        last_round = last_tournament["rounds"][-1]
        if last_round["round_id"] == round_id:

            matchs = last_round["matchs"]

            for item in matchs:
                data_match_id = item["match_id"]
                if data_match_id == int(user_match_id):
                    match_detail = last_round["matchs"][int(user_match_id) - 1]
                    match_detail["match"][0][1] = score1
                    match_detail["match"][1][1] = score2
                    break

            update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                   last_tournament["tournament_id"],
                                   last_tournament)

            print("Les scores ont été enregistrés.")
        else:
            print("Une erreur est survenue lors de l'enregistrement.")

        return last_round
