import random
from typing import List

from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from models.match import MatchModel
from models.player import PlayerModel
from models.round import RoundModel
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
        self.rounds: List[RoundModel] = []
        self.players: List[PlayerModel] = []

        # use for pairing players
        self.historical_pairs = []

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
                national_id (str): Identifier of the player
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

            ConsoleDisplayer.log(MESSAGES["player_unregistered"], level="INFO")

    def generate_a_round(self, round_number, players,
                         tournament_id, round_id=None):
        """Generate a tournament round
            Args:
                round_number (int): the current round number
                players (list): list of players
                tournament_id (int): Identifier of the tournament
                round_id (int): Identifier of the current round (by default
                None)
        """
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )

        if tournament:
            if round_id == 0:
                # Count total of no ended rounds
                count_round_ended = sum(1 for r in tournament["rounds"] if
                                        not r["round_end_date"] and r[
                                            "round_start_date"])

                if count_round_ended > 0:
                    return None

                round_number += 1
                round_name = f"Round {round_number}"
                round_ = RoundModel(round_number, round_name)

                if round_number == 1:
                    random.shuffle(players)
                else:
                    players.sort(key=lambda player: (player["points"],
                                                     random.random()),
                                 reverse=True)

                # Generate pairing
                try:
                    pairings = self._generate_pairings(players)
                except ValueError as e:
                    ConsoleDisplayer.log(str(e), level="ERROR")
                    return None

                round_.matchs = [
                    MatchModel(
                        match_id=i+1,
                        player1=p1["national_id"],
                        score1=0.0,
                        player2=p2["national_id"],
                        score2=0.0).to_dict()
                    for i, (p1, p2) in enumerate(pairings)
                ]

                data_round = {
                    "round_id": round_number,
                    "name": round_name,
                    "round_start_date": str(round_.start_date),
                    "round_end_date": str(round_.end_date),
                    "matchs": round_.matchs
                }

                tournament["rounds"].append(data_round)
                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"],
                                  tournament)

                ConsoleDisplayer.log(MESSAGES["round_generated"],
                                     level="INFO")
                return tournament

            else:
                # Case if manager or while application stop before saving
                # scores
                rounds = tournament["rounds"]
                current_round = next(
                    (r for r in rounds if r["round_id"] == round_id),
                    None
                )

                if current_round:
                    if self._is_round_ready_to_update(current_round):
                        return tournament
                    else:
                        return "round_already_ended"
                return None
        return None

    def _generate_pairings(self, players):
        """Generate pairings for a tournament
            Args:
                players (list): list of players
        """

        from itertools import combinations
        possible_pairs = list(combinations(players, 2))
        possible_pairs = [
            (p1, p2) for p1, p2 in possible_pairs
            if tuple(
                sorted(
                    (p1["national_id"], p2["national_id"])
                )
            ) not in self.historical_pairs
        ]

        if not possible_pairs:
            raise ValueError(MESSAGES["players_already_played_together"])

        possible_pairs.sort(key=lambda pair: abs(pair[0]["points"] - pair[
            1]["points"]))

        pairings = []
        used = set()

        # While there are unpaired players and possible pairs
        while len(used) < len(players) and possible_pairs:
            p1, p2 = possible_pairs.pop(0)
            if p1["national_id"] not in used and p2["national_id"] not in used:
                pairings.append((p1, p2))
                used.update([p1["national_id"], p2["national_id"]])
                self.historical_pairs.append(tuple((p1["national_id"],
                                                    p2["national_id"])))

        if len(used) != len(players):
            raise ValueError(MESSAGES["no_possible_pairing"])

        return pairings

    @staticmethod
    def _is_round_ready_to_update(round_data: dict):
        """Check if a round is ready to update"""
        total_matchs = 0
        total_matchs += len(round_data["matchs"])
        unscored_matchs = 0
        for match in round_data["matchs"]:
            for _, score in match["match"]:
                if score == 0.0:
                    unscored_matchs += 1

        return (unscored_matchs / total_matchs == 2) or (round_data[
            "round_start_date"] == "")

    @staticmethod
    def update_players_points(tournament_id, round_id):
        """Update all players' points.
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
