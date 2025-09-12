class Match:
    """Match class"""
    def __init__(self, match_id, player1, score1, player2, score2):
        """Initialise match with:
            match_id,
            player1,
            score1,
            player2,
            score2
        """
        self.match_id = match_id
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "player1": self.player1,
            "score1": self.score1,
            "player2": self.player2,
            "score2": self.score2,
        }

    def __str__(self):
        """Return string representation of match for printing"""
        # match_player = f"{str(self.player1)} vs {str(self.player2)}\n"
        player1 = f"{self.player1} - {self.score1}"
        player2 = f"{self.score2} - {self.player2}"
        return f"id:{self.match_id}\n {player1} vs {player2}"

    def __repr__(self):
        """Return string representation of match for printing"""
        return str(self)
