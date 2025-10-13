from typing import List

from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from models.player import PlayerModel
from models.round import Round
from utils.console_utils import ConsoleDisplayer
from utils.file_utils import read_json_file, save_to_json, update_tournament


class TournamentModel:
    """Tournament class"""
    def __init__(
            self,
            tournament_id: int = None,
            name: str = None,
            location: str = None,
            start_date: str = None,
            end_date: str = None,
            description: str = None,
            number_of_rounds: int = None,
            round_number: int = None):
        """Initialize tournament with:
            tournament_id: Identifier of the tournament
            name: Name of the tournament,
            location: Location of the tournament,
            start_date: Start date of the tournament,
            end_date: End date of the tournament,
            description: Description of the tournament,
            number_of_rounds: Number of rounds in a tournament (by default : 4)
            round_number: number of the current round (by default : 0)
        """
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.round_number = round_number

        # lists of rounds and players by tournament
        self.rounds: List[Round] = []
        self.players: List[PlayerModel] = []

    def create(self, tournament):
        """Create a new tournament and save it to JSON file
            Args:
                tournament: Tournament instance
        """
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments['tournaments']
        id_tournament = self.tournament_id
        if id_tournament is None:
            id_tournament = max(1, len(tournaments) + 1)

        # Validate the number of rounds
        if (tournament.number_of_rounds == "" or int(
                tournament.number_of_rounds) < 4):
            self.number_of_rounds = 4

        save_to_json(
            "tournaments",
            tournament_id=id_tournament,
            name=tournament.name.upper(),
            location=tournament.location.capitalize(),
            start_date=tournament.start_date,
            end_date=tournament.end_date,
            description=tournament.description,
            number_of_rounds=tournament.number_of_rounds,
            round_number=0,
            players=[],
            rounds=[]
        )

        return ConsoleDisplayer.log(MESSAGES["tournament_created"],
                                    level="INFO")

    @staticmethod
    def register_a_player(player: PlayerModel, tournament_id: int):
        """Register a player to a specific tournament and save it to JSON file
        Args:
            player (PlayerModel): player info to add and save
            tournament_id (int): Identifier of a specific tournament
        """
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )

        if tournament:
            tournament["players"].append({
                "national_id": player.national_id,
                "last_name": player.last_name.upper(),
                "first_name": player.first_name.capitalize(),
                "birth_date": player.birth_date,
                "points": 0.0
            })

            update_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE,
                tournament["tournament_id"],
                tournament
            )

            ConsoleDisplayer.log(MESSAGES["player_registered"], level="INFO")

    @staticmethod
    def unregister_a_player(tournament_id, national_id):
        """Unregister an identified player from the tournament
            Args:
                tournament_id (int): Identifier of the tournament
                national_id (int): Identifier of the player
        """
        data = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == int(
                tournament_id)),
            None
        )

        if tournament:
            tournament["players"] = [player for player in tournament[
                "players"] if player.get("national_id") != national_id]

            update_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE,
                tournament["tournament_id"],
                tournament
            )

            return ConsoleDisplayer.log(MESSAGES["player_unregistered"],
                                        level="INFO")
        else:
            return None

    def __str__(self):
        """Return string representation of tournament"""
        return (f"Identifiant du tournoi: {self.tournament_id} - {self.name}\n"
                f"Du {self.start_date} au {self.end_date}\n"
                f"Description: {self.description}\n"
                f"Nombre de tours: {self.number_of_rounds}\n"
                f"Numéro du tour en cours: {self.round_number}\n"
                f"Joueurs:\n"
                f"{self.players}\n"
                f"Tours:\n"
                f"{self.rounds}")

    def __repr__(self):
        """Return string representation of tournament"""
        return str(self)
