class Round:
    """Round class"""
    def __init__(self, name):
        """Initialise player with:
            name,
            start_date,
            end_date
        """

        self.name = name
        self.start_date = ""
        self.end_date = ""
        self.matches = []

    def to_dict(self):
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches": self.matches
        }

    def __str__(self):
        """Return string representation of round for printing"""
        round_info = f"{self.name} - du {self.start_date} au {self.end_date}\n"
        round_matches = ("Matches: \n\t" + "\n\t".join(str(match) for
                                                       match in self.matches))

        return round_info + "\n" + round_matches

    def __repr__(self):
        """Return string representation of round for printing"""
        return str(self)
