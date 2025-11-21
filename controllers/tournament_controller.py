from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, DEFAULT_SCORE, \
    MESSAGES
from models.player_model import PlayerModel
from models.tournament_model import TournamentModel
from utils.console_utils import ConsoleDisplayer
from utils.file_utils import read_json_file, update_tournament
from utils.tournament_helpers import get_tournament_details


class TournamentController():
    def __init__(self):
        self.tournament = TournamentModel()


    def register_a_player(self, selected_tournament_id, player_id):
        """Register a player to a specific tournament and save it to JSON file
        Args:
            selected_tournament_id (int): tournament id
            player_id (string): player national id
        """
        self.tournament.tournament_id = selected_tournament_id
        tournament = get_tournament_details(self.tournament.tournament_id)

        if tournament:
            tournament["players"].append({
                "national_id": player_id,
                "points": DEFAULT_SCORE
            })

            update_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE,
                tournament["tournament_id"],
                tournament
            )

        ConsoleDisplayer.log(MESSAGES["player_registered"], level="INFO")

    def unregister_a_player(self, selected_tournament_id, player_id):
        """Unregister an identified player from the tournament
            Args:
                selected_tournament_id (int): Identifier of the tournament
                player_id (str): Identifier of the player
        """
        self.tournament.tournament_id = selected_tournament_id
        tournament = get_tournament_details(self.tournament.tournament_id)

        if tournament:
            tournament["players"] = [player for player in tournament[
                "players"] if player.get("national_id") != player_id]

            update_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE,
                tournament["tournament_id"],
                tournament
            )

            ConsoleDisplayer.log(MESSAGES["player_unregistered"], level="INFO")