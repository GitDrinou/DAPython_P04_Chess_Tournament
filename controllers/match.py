from utils.console_utils import ConsoleLogger
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from utils.file_utils import update_tournament


class MatchController:
    """Match controller class"""

    @staticmethod
    def save_score(tournament, round_id, user_match_id, score1, score2):
        """ Update score for specific match """
        rounds = tournament["rounds"]
        for round_detail in rounds:
            try:
                if round_detail["round_id"] == round_id:

                    matchs = round_detail["matchs"]

                    for item in matchs:
                        data_match_id = item["match_id"]
                        if data_match_id == int(user_match_id):
                            match_detail = round_detail["matchs"][int(
                                user_match_id) - 1]
                            match_detail["match"][0][1] = score1
                            match_detail["match"][1][1] = score2
                            break

                    update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                      tournament["tournament_id"],
                                      tournament)
            except KeyError:
                ConsoleLogger.log(MESSAGES["error_on_save"], level="ERROR")

            return round_detail
        return None
