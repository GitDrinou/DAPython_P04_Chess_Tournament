from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.tournament_utils import update_tournament


class MatchModel:
    """Match class"""
    def __init__(
            self,
            match_id: int = None,
            player1: str = None,
            score1: float = None,
            player2: str = None,
            score2: float = None):
        """Initialise match with:
            match_id: Identifier of the match,
            player1: National Identifier of the player1,
            score1: Score of the player1,
            player2: National Identifier of the player2,
            score2: Score of the player2,
        """
        self.match_id = match_id
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    def to_dict(self):
        """Return dict representation of match"""
        return {
            "match_id": self.match_id,
            "match": ([self.player1, self.score1], [self.player2, self.score2])
        }

    @staticmethod
    def save_scores(tournament, round_id, match_id, score1, score2):
        """Save a match score
            Args;
                tournament (Tournament): tournament info
                round_id (int): Identifier of the current round
                match_id (int): Identifier of the current match
                score1 (float): Score 1 for the player1
                score2 (float): Score 2 for the player2
            Returns:
                round_ (Round): round info
        """
        rounds = tournament["rounds"]
        round_ = next(
            (r for r in rounds if r["round_id"] == round_id),
            None
        )

        if round_:
            matchs = round_["matchs"]
            match = next(
                (m for m in matchs if m["match_id"] == match_id),
                None
            )

            if match:
                match_detail = round_["matchs"][int(match_id) - 1]
                match_detail["match"][0][1] = score1
                match_detail["match"][1][1] = score2

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"], tournament)

            return round_
        else:
            return None

    def __str__(self):
        """Return string representation of match for printing"""
        return [self.player1, self.score1], [self.player2, self.score2]

    def __repr__(self):
        """Return string representation of match for printing"""
        return str(self)
