from models.player import PlayerModel
from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from models.tournament import TournamentModel
from utils.file_utils import read_json_file, update_tournament
from utils.console_utils import ConsoleDisplayer


class TournamentController:
    """Tournament controller class"""

    def __init__(self):
        """Constructor"""
        self.tournament_model = TournamentModel()
        self.player_model = PlayerModel()
        # self.historical_pairs = []

    def create_a_tournament(self, tournament):
        """Create a new tournament"""
        self.tournament_model.create(tournament)

    def register_a_player_to_a_tournament(self, player, tournament_id):
        """Register a player to the specified tournament and save the player to
        the JSON file."""
        self.tournament_model.register_a_player(player, tournament_id)
        self.player_model.save_player_to_json(player)

    def unregister_a_player_from_a_tournament(self, tournament_id,
                                              national_id):
        """Unregister a player from the specified tournament"""
        self.tournament_model.unregister_a_player(tournament_id, national_id)

    def generate_a_tournament_round(self, round_number, players,
                                    tournament_id, round_id):
        """Generate a new tournament round."""
        self.tournament_model.generate_a_round(round_number, players,
                                               tournament_id, round_id)

    @staticmethod
    def update_player_points(tournament_id, round_id):
        """Update player's points
        Args:
            tournament_id (int): Identifier of the tournament
            round_id (int): Identifier of the current round
        """
        data = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )

        if tournament:
            players = {
                player["national_id"]: player for player in tournament[
                    "players"]
            }

            rounds = tournament["rounds"]
            round_ = next(
                (r for r in rounds if r["round_id"] == int(round_id)),
                None
            )
            for match_detail in round_["matchs"]:
                player1_id, player1_score = match_detail["match"][0]
                player2_id, player2_score = match_detail["match"][1]
                player1_score = float(player1_score)
                player2_score = float(player2_score)

                if player1_score == player2_score:
                    players[player1_id]["points"] += 0.5
                    players[player2_id]["points"] += 0.5
                else:
                    if player1_score > player2_score:
                        players[player1_id]["points"] += 1
                    else:
                        players[player2_id]["points"] += 1

            # save to json file
            for p in tournament["players"]:
                national_id = p["national_id"]
                if national_id == players[national_id]["national_id"]:
                    p["points"] = players[national_id]["points"]

            update_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE,
                tournament["tournament_id"],
                tournament
            )

            return ConsoleDisplayer.log(MESSAGES["points_updated"],
                                        level="INFO")
        else:
            return None
