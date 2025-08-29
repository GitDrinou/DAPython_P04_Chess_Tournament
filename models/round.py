class Round:
    """Round class"""
    def __init__(self, round_id, name, start_date, end_date, players,
                 matches=None):
        """Initialise player with:
            round_id,
            name,
            start_date,
            end_date
        """
        if matches is None:
            matches = []
        self.round_id = round_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.players = players
        self.matches = matches

    def __str__(self):
        """Return string representation of round for printing"""
        round_info = f"{self.name} - du {self.start_date} au {self.end_date}\n"
        round_players = ("Joueurs: \n\t" + "\n\t".join(str(player) for
                                                       player in self.players))
        round_matches = ("Matches: \n\t" + "\n\t".join(str(match) for
                                                       match in self.matches))

        return round_info + round_players + "\n" + round_matches

    def __repr__(self):
        """Return string representation of round for printing"""
        return str(self)
