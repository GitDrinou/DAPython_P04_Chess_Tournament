from utils.file_utils import save_to_json
from utils.player_utils import check_player_is_exist


class PlayerModel:
    """Player class"""
    def __init__(
            self,
            national_id: str = None,
            last_name: str = None,
            first_name: str = None,
            birth_date: str = None,
            points: float = None):
        """Initialise player with:
                national_id: National Identification of the player,
                last_name: Last name of the player,
                first_name: First name of the player,
                birth_date: Birth date of the player,
                points: Tournament point of the player (by default = 0)
        """
        self.national_id = national_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.points = points

    def to_dict(self):
        return {
            "national_id": self.national_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "points": self.points
        }

    @staticmethod
    def save_player_to_json(player):
        """Save player to json
            Args:
                player: Player instance
        """
        if not check_player_is_exist(player.national_id):
            save_to_json(
                "players",
                national_id=player.national_id,
                last_name=player.last_name.upper(),
                first_name=player.first_name.capitalize(),
                birth_date=player.birth_date)

    def __str__(self):
        """Return string representation of player for printing"""
        return (f"{self.national_id} - {self.last_name} {self.first_name},"
                f" {self.birth_date}")

    def __repr__(self):
        """Return string representation of player fir printing"""
        return str(self)
