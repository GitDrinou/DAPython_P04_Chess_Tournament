from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import update_tournament


class MatchController:
    """Match controller class"""

    @staticmethod
    def save_score(tournament, round_id, user_match_id, score1, score2):
        """ Update score for specific match """
        rounds = tournament["rounds"]
        round_ = next(
            (r for r in rounds if r["round_id"] == round_id),
            None
        )

        if round_:
            matchs = round_["matchs"]
            match = next(
                (m for m in matchs if m["match_id"] == user_match_id),
                None
            )

            if match:
                match_detail = round_["matchs"][int(user_match_id) - 1]
                match_detail["match"][0][1] = score1
                match_detail["match"][1][1] = score2

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"], tournament)

            return round_
        else:
            return None
