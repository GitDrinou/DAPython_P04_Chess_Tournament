class Round:
    """Round class"""
    def __init__(self, name, start_date, end_date, players):
        """Initialise player with:
            name,
            start_date,
            end_date
        """
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.players = players

    def __str__(self):
        """Return string representation of round for printing"""
        round_info = f"{self.name} - du {self.start_date} au {self.end_date}\n"
        round_players = ("Joueurs: \n\t" + "\n\t".join(str(player) for
                                                       player in self.players))
        return round_info + round_players

    def __repr__(self):
        """Return string representation of round for printing"""
        return str(self)
