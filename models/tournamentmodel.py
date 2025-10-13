from typing import List

from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from models.player import Player
from models.round import Round
from utils.console_utils import ConsoleDisplayer
from utils.file_utils import read_json_file, save_to_json


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
        self.players: List[Player] = []

    def create(self, tournament):
        """Create a new tournament and save it to JSON file"""
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
