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
            start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            if round_id == 0:
                last_round = tournament["rounds"][-1]
                tournament["round_number"] = last_round["name"][-1]
                last_round["round_start_date"] = start_date

                update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                  tournament["tournament_id"], tournament)

                ConsoleDisplayer.log(MESSAGES["round_started"], level="INFO")

                return last_round
            else:
                round_ = next(
                    (r for r in rounds if r["round_id"] == round_id),
                    None
                )

                if round_:
                    tournament["round_number"] = round_["name"][-1]
                    round_["round_start_date"] = start_date

                    update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                      tournament["tournament_id"], tournament)

                    ConsoleDisplayer.log(MESSAGES["round_started"],
                                         level="INFO")

                    return round_
                return None
        else:
            return None

    def __str__(self):
        """Return string representation of round for printing"""
        round_info = f"{self.name} - du {self.start_date} au {self.end_date}\n"
        round_matchs = ("Matchs: \n\t" + "\n\t".join(str(match) for match in
                                                     self.matchs))

        return round_info + "\n" + round_matchs

    def __repr__(self):
        """Return string representation of round for printing"""
        return str(self)
