from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import update_last_tournament


class MatchController:
    """Match controller class"""

    @staticmethod
    def save_score(tournament, round_detail, user_match_id, score1, score2):
        """ Update score for specific match """
        matchs = round_detail["matchs"]

        for item in matchs:
            data_match_id = item["match_id"]
            if data_match_id == int(user_match_id):
                match_detail = round_detail["matchs"][int(user_match_id)-1]
                match_detail["match"][0][1] = score1
                match_detail["match"][1][1] = score2
                break

        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                               tournament["tournament_id"],
                               tournament)
