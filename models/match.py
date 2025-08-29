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

    def __str__(self):
        """Return string representation of match for printing"""
        match_player = f"{str(self.player1)} vs {str(self.player2)}\n"
        match_score = f"{self.score1} : {str(self.score2)}"
        return match_player + "\t" + match_score

    def __repr__(self):
        """Return string representation of match for printing"""
        return str(self)
