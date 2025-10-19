from datetime import datetime

from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from utils.console_utils import ConsoleDisplayer
from utils.file_utils import read_json_file, update_tournament


class RoundModel:
    """Round class"""
    def __init__(
            self,
            round_id: int = None,
            name: str = None):
        """Initialise player with:
            round_id: Identifier of the round,
            name: Name of the round
        """
        self.round_id = round_id
        self.name = name
        self.start_date = ""
        self.end_date = ""
        self.matchs = []

    def to_dict(self):
        return {
            "round_id": self.round_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matchs": self.matchs
        }

    @staticmethod
    def start_up(tournament_id, round_id):
        """Method that starts a round
            Args:
                tournament_id (int): Identifier of a specific tournament
                round_id (int): Identifier of a specific round
            Returns:
                round_item (Round): round info
        """
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )

        if tournament:
            rounds = tournament["rounds"]
            round_ = next(
                (r for r in rounds if r["round_id"] == round_id),
                None
            )

            start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            if round_:
                tournament["round_number"] = round_["name"][-1]
                round_["round_start_date"] = start_date

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"], tournament)

                ConsoleDisplayer.log(MESSAGES["round_started"],
                                     level="INFO")

                return round_
            else:
                last_round = tournament["rounds"][-1]
                tournament["round_number"] = last_round["name"][-1]
                last_round["round_start_date"] = start_date

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"], tournament)

                ConsoleDisplayer.log(MESSAGES["round_started"], level="INFO")

                return last_round
        else:
            return None

    @staticmethod
    def end_up(tournament_id, round_id):
        """Method that terminates a round
            Args:
                tournament_id (int): Identifier of a specific tournament
                round_id (int): Identifier of a specific round
            Returns:
                round_item (round): round details
        """
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )

        if tournament:
            rounds = tournament["rounds"]
            round_ = next(
                (r for r in rounds if r["round_id"] == round_id),
                None
            )

            end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            if round_:
                if round_["round_start_date"] == "":
                    ConsoleDisplayer.log(MESSAGES["round_not_started"],
                                         level="WARNING")
                    return None
                else:
                    round_["round_end_date"] = end_date

                    update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                      tournament["tournament_id"], tournament)

                    ConsoleDisplayer.log(MESSAGES["round_ended"], level="INFO")

                    return round_
            else:
                last_round = tournament["rounds"][-1]
                last_round["round_end_date"] = end_date

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"], tournament)

                ConsoleDisplayer.log(MESSAGES["round_ended"], level="INFO")

                return last_round
        else:
            return None

    @staticmethod
    def is_finished(rounds):
        """Method that checks if a round is finished or not..
            Args:
                rounds (list): list of rounds
            Returns:
                finished_rounds (list): List of rounds with finished
                indicator (X).
        """
        finished_rounds = []
        counter_match = 0
        for round_ in rounds:
            for match_ in round_["matchs"]:
                player1_id, player1_score = match_["match"][0]
                player2_id, player2_score = match_["match"][1]
                player1_score = float(player1_score)
                player2_score = float(player2_score)

                if player1_score == 0.0 and player2_score == 0.0:
                    counter_match += 1

            if (counter_match == len(round_["matchs"])
                    or round_["round_end_date"] == ""):
                finished_rounds.append({
                    "round_id": round_["round_id"],
                    "is_finished": ""
                })
            else:
                finished_rounds.append({
                    "round_id": round_["round_id"],
                    "is_finished": "X"
                })

        return finished_rounds

    def __str__(self):
        """Return string representation of round for printing"""
        round_info = f"{self.name} - du {self.start_date} au {self.end_date}\n"
        round_matchs = ("Matchs: \n\t" + "\n\t".join(str(match) for match in
                                                     self.matchs))

        return round_info + "\n" + round_matchs

    def __repr__(self):
        """Return string representation of round for printing"""
        return str(self)
