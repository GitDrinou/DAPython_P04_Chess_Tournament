from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import update_tournament


class MatchController:
    """Match controller class"""

    @staticmethod
    def save_score(tournament, round_id, user_match_id, score1, score2):
        """Save a match score
            Args;
                tournament (dict): tournament detail
                round_id (int): Identifier of the current round
                user_match_id (int): Identifier of the current match
                score1 (float): Score 1 for the player1
                score2 (float): Score 2 for the player2
            Returns:
                round_ (round): round detail
        """
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
