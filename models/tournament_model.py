import random
from typing import List

from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES, \
    DEFAULT_NUMBER_OF_ROUNDS, DEFAULT_SCORE, POINT_EQUALITY_VALUE, \
    POINT_WIN_VALUE, ERROR_ROUND_ENDED
from models.match_model import MatchModel
from models.player_model import PlayerModel
from models.round_model import RoundModel
from utils.console_utils import ConsoleDisplayer
from utils.file_utils import read_json_file, save_to_json, update_tournament
from utils.tournament_helpers import get_tournament_details


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
            number_of_rounds: int = DEFAULT_NUMBER_OF_ROUNDS,
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
        self.players: List[PlayerModel] = []
        self.rounds: List[RoundModel] = []

        # use for pairing players
        self.historical_pairs = set()

    def to_dict(self):
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "round_number": self.round_number,
            "players": self.players,
            "rounds": self.rounds
        }

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
                tournament.number_of_rounds) < DEFAULT_NUMBER_OF_ROUNDS):
            tournament.number_of_rounds = self.number_of_rounds

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

    def register_a_player(self, selected_tournament_id, player_id):
        """Register a player to a specific tournament and save it to JSON file
        Args:
            selected_tournament_id (int): tournament id
            player_id (string): player national id
        """
        self.tournament_id = selected_tournament_id
        tournament = get_tournament_details(self.tournament_id)

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
        self.tournament_id = selected_tournament_id
        tournament = get_tournament_details(self.tournament_id)

        if tournament:
            tournament["players"] = [player for player in tournament[
                "players"] if player.get("national_id") != player_id]

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
            self._register_previous_pairs(tournament["rounds"])
            if round_id == 0:
                # Count total of no ended rounds
                count_round_ended = sum(1 for r in tournament["rounds"] if
                                        not r["round_end_date"] and r[
                                            "round_start_date"])

                if count_round_ended > 0:
                    return None

                round_number += 1
                self._generate_new_round(tournament, round_number, players)

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"],
                                  tournament)

                ConsoleDisplayer.log(MESSAGES["round_generated"],
                                     level="INFO")
                return tournament

            else:
                return self._terminate_current_round(tournament, round_id)
        return None

    def _generate_new_round(self, tournament, round_number, players):
        """Generate a new round
            Args:tournament (dict): tournament info
        """

        round_name = f"Round {round_number}"
        round_ = RoundModel(round_number, round_name)

        if round_number == 1:
            random.shuffle(players)
        else:
            players.sort(key=lambda player: (player["points"],
                                             random.random()), reverse=True)

        # Generate pairing
        try:
            pairings, bye_player = self._generate_pairings(players)
        except ValueError as e:
            ConsoleDisplayer.log(str(e), level="ERROR")
            return None

        round_.matchs = [
            MatchModel(
                match_id=i + 1,
                player1=p1["national_id"],
                score1=0.0,
                player2=p2["national_id"],
                score2=0.0).to_dict()
            for i, (p1, p2) in enumerate(pairings)
        ]

        # if player BYE exist
        if bye_player:
            bye_match = {
                "match_id": len(round_.matchs) + 1,
                "match": [
                    (bye_player["national_id"], "BYE"),
                ]
            }
            round_.matchs.append(bye_match)

        data_round = {
            "round_id": round_number,
            "name": round_name,
            "round_start_date": str(round_.start_date),
            "round_end_date": str(round_.end_date),
            "matchs": round_.matchs
        }

        tournament["rounds"].append(data_round)
        return tournament

    def _terminate_current_round(self, tournament, round_id):
        """Terminate the current round
            Args:
                tournament (dict): tournament info
                round_id (int): identifier of the current round
        """
        rounds = tournament["rounds"]
        current_round = next(
            (r for r in rounds if r["round_id"] == int(round_id)),
            None
        )
        if current_round is not None:
            if not self._is_round_ready_to_update(current_round):
                return tournament
            else:
                return ERROR_ROUND_ENDED
        return None

    def _have_played_before(self, player1, player2):
        """Check if players have already played before
            Args:
                player1 (str): player1 national_id
                player2 (str): player2 national_id
        """
        return (frozenset((player1, player2))
                in self.historical_pairs)

    def _save_pair(self, player1, player2):
        """Save a pair to historical pairings
        Args:
            player1 (str): player1 national_id
            player2 (str): player2 national_id
        """
        self.historical_pairs.add(frozenset((player1, player2)))

    def _register_previous_pairs(self, rounds):
        """Load all prévious pairs from existing tournament rounds"""
        for round_ in rounds:
            for match in round_["matchs"]:
                p1 = match["match"][0][0]
                p2 = match["match"][0][1]
                self._save_pair(p1, p2)

    def _generate_pairings(self, players):
        """Generate pairings for a tournament
            Args:
                players (list): list of players
        """
        pairs = []
        used = set()
        bye_player = None

        if len(players) % 2 == 1:
            bye_player = random.choice(players)
            ConsoleDisplayer.log(f"{MESSAGES['number_of_players_is_odd']}\n"
                                 f"{bye_player['last_name']}"
                                 f" {bye_player['first_name']}"
                                 f" {MESSAGES['will_be_bye']}", level="INFO")
            players = [p for p in players if p["national_id"] != bye_player[
                "national_id"]]

        i = 0
        while i < len(players) - 1:
            p1 = players[i]
            if p1["national_id"] in used:
                i += 1
                continue

            p2 = None
            for j in range(i + 1, len(players)):
                contender = players[j]
                contender_id = contender["national_id"]
                if (contender_id not in used
                        and not self._have_played_before(p1["national_id"],
                                                         contender_id)):
                    p2 = contender
                    break

            # if not, force pairing with the next unpaired player
            if not p2:
                for j in range(i + 1, len(players)):
                    contender = players[j]
                    if contender["national_id"] not in used:
                        p2 = contender
                        break

            if not p2:
                break

            pairs.append((p1, p2))
            self._save_pair(p1["national_id"], p2["national_id"])
            used.update({p1["national_id"], p2["national_id"]})
            i += 1
        return pairs, bye_player

    @staticmethod
    def _is_round_ready_to_update(round_data: dict):
        """Check if a round is ready to update"""
        unscored_matchs = 0

        for match in round_data["matchs"]:
            match_entries = match.get("match", [])
            if len(match_entries) == 1:
                continue

            player1_id, score1 = match_entries[0]
            player2_id, score2 = match_entries[1]

            if score1 == DEFAULT_SCORE and score2 == DEFAULT_SCORE:
                unscored_matchs += 1

        return unscored_matchs == 0 or round_data["round_start_date"] == ""

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
                    "players"]}
            rounds = tournament["rounds"]
            round_ = next(
                (r for r in rounds if r["round_id"] == int(round_id)), None)
            for match_detail in round_["matchs"]:
                if len(match_detail["match"]) == 1:
                    bye_player_id = match_detail["match"][0][0]
                    if bye_player_id in players:
                        players[bye_player_id]["points"] += POINT_WIN_VALUE
                        ConsoleDisplayer.log(
                            f"{players[bye_player_id]['first_name']} "
                            f"{players[bye_player_id]['last_name']} "
                            f"{MESSAGES['have_win_point']}", level="INFO")
                else:
                    player1_id, player1_score = match_detail["match"][0]
                    player2_id, player2_score = match_detail["match"][1]
                    player1_score = float(player1_score)
                    player2_score = float(player2_score)
                    if player1_score == player2_score:
                        players[player1_id]["points"] += POINT_EQUALITY_VALUE
                        players[player2_id]["points"] += POINT_EQUALITY_VALUE
                    else:
                        if player1_score > player2_score:
                            players[player1_id]["points"] += POINT_WIN_VALUE
                        else:
                            players[player2_id]["points"] += POINT_WIN_VALUE
            for p in tournament["players"]:
                national_id = p["national_id"]
                if national_id == players[national_id]["national_id"]:
                    p["points"] = players[national_id]["points"]
            update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                              tournament["tournament_id"], tournament)
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
