from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, DEFAULT_SCORE, \
    MESSAGES
from models.player_model import PlayerModel
from models.tournament_model import TournamentModel
from utils.console_utils import ConsoleDisplayer
from utils.file_utils import read_json_file, update_tournament

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
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] ==
             self.tournament.tournament_id),
            None
        )
        print(tournament)
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