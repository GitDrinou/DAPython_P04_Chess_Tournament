from datetime import datetime

from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import read_file, update_last_tournament


class RoundController:
    """Round controller class"""

    @staticmethod
    def start_round():
        """Method that starts a round."""
        data_tournaments = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data_tournaments["tournaments"][-1]
        last_round = last_tournament["rounds"][-1]
        start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        last_tournament["round_number"] = last_round["name"][-1]
        last_round["round_start_date"] = start_date

        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                               last_tournament["tournament_id"],
                               last_tournament)

        print("Le tour a démarré.")

        return last_round

    @staticmethod
    def end_round():
        """Method that ends a round."""
        data_tournaments = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data_tournaments["tournaments"][-1]
        last_round = last_tournament["rounds"][-1]
        end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        last_tournament["round_number"] = last_round["name"][-1]
        last_round["round_end_date"] = end_date

        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                               last_tournament["tournament_id"],
                               last_tournament)

        print("Le tour est terminé.")

        return last_round
