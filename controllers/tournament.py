from models.match_model import MatchModel
from models.player_model import PlayerModel
from models.round_model import RoundModel
from models.tournament_model import TournamentModel


class TournamentController:
    """Tournament controller class"""

    def __init__(self):
        """Constructor"""
        self.tournament_model = TournamentModel()
        self.player_model = PlayerModel()
        self.match_model = MatchModel()
        self.round_model = RoundModel()

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
        tournament = self.tournament_model.generate_a_round(round_number,
                                                            players,
                                                            tournament_id,
                                                            round_id)
        return tournament

    def start_a_round(self, tournament_id, round_id):
        round_info = self.round_model.start_up(tournament_id, round_id)
        return round_info

    def terminate_a_round(self, tournament_id, round_id):
        round_info = self.round_model.end_up(tournament_id, round_id)
        return round_info

    def save_round_matchs_scores(self, tournament, round_id, match_id,
                                 score1, score2):
        """Save all matchs scores for a round."""
        self.match_model.save_scores(tournament, round_id, match_id,
                                     score1, score2)

    def update_players_points_for_a_tournament(self, tournament_id, round_id):
        """Update all players' points."""
        self.tournament_model.update_players_points(tournament_id, round_id)
