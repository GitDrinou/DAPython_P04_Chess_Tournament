class Tournament:
    """Tournament class"""
    def __init__(self,
                 name,
                 location,
                 start_date,
                 end_date,
                 description,
                 number_of_rounds=4,
                 round_number=0):
        """Initialize tournament with:
            name,
            location,
            start_date,
            end_date,
            description,
            number of rounds (by default : 4)
            round number (by default : 0)
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.round_number = round_number

        # lists of rounds and players by tournament
        self.rounds = []
        self.players = []

        # check if the tournament is on break or not
        self.is_on_break = False

    def __str__(self):
        """Return string representation of tournament"""
        return (f"{self.name} du {self.start_date} au {self.end_date}\n "
                f"Description: {self.description}\nJoueurs: "
                f"{self.players}\nTours: {self.rounds}")

    def __repr__(self):
        """Return string representation of tournament"""
        return str(self)
