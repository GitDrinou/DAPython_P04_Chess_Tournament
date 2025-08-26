class Tournament:
    """Tournament class"""
    def __init__(self,
                 name,
                 location,
                 start_date,
                 end_date,
                 description,
                 number_of_round=4,
                 round_number=0):
        """Initialize tournament with:
            name,
            location,
            start_date,
            end_date,
            description,
            number of round (by default : 4)
            round number (by default : 0)
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_round = number_of_round
        self.round_number = round_number

        # lists of rounds and players by tournament
        self.rounds = []
        self.players = []

    def __str__(self):
        """Return string representation of tournament"""
        return (f"{self.name} du {self.start_date} au {self.end_date}\n "
                f"Description: {self.description}\nJoueurs: "
                f"{self.players}\nTours: {self.rounds}")

    def __repr__(self):
        """Return string representation of tournament"""
        return str(self)
