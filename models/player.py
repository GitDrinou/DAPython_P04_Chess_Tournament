class Player:
    """Player class"""
    def __init__(self, last_name, first_name, point=0):
        """Initialise player with:
                national_id,
                last_name,
                first_name,
                point (default 0)
        """
        self.last_name = last_name
        self.first_name = first_name
        self.national_id = ""
        self.point = point

    def to_dict(self):
        return {
            "national_id": self.national_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "point": self.point
        }

    def __str__(self):
        """Return string representation of player for printing"""
        return f"{self.national_id} - {self.last_name} {self.first_name}"

    def __repr__(self):
        """Return string representation of player fir printing"""
        return str(self)
