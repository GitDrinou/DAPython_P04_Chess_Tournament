"""Entry point of the application."""
import json
import os

from controllers.application import ApplicationController
from controllers.match import MatchController
from controllers.player import PlayerController
from controllers.round import RoundController
from controllers.tournament import TournamentController
# from controllers.round import RoundController
# from controllers.tournament import TournamentController
# from controllers.tournament import TournamentController
# from models.tournament import Tournament
from utils.constants import (PATH_DATA_TOURNAMENTS_JSON_FILE,
                             PATH_DATA_PLAYERS_JSON_FILE)
from utils.file_utils import (read_file)
from views.menu import MenuView
from views.report import ReportView


def initialize():
    """Initialize the application."""

    if not os.path.isfile(PATH_DATA_PLAYERS_JSON_FILE):
        default_data = {"players": [], }
        with open(PATH_DATA_PLAYERS_JSON_FILE, "w",
                  encoding="utf-8") as json_file:
            json.dump(default_data, json_file, indent=4)

    if not os.path.isfile(PATH_DATA_TOURNAMENTS_JSON_FILE):
        default_data = {"tournaments": [], }
        with (open(PATH_DATA_TOURNAMENTS_JSON_FILE, "w", encoding="utf-8")
              as json_file):
            json.dump(default_data, json_file, indent=4)


def main():
    """Main entry point of the application."""
    data_players = read_file(PATH_DATA_PLAYERS_JSON_FILE)
    # data_tournaments = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)

    total_players = len(data_players["players"])
    if total_players == 0:
        print("Vous n'avez pas de joueurs enregistrés dans votre base. "
              "Veuillez en saisir en utilisant l'option indiquée dans le "
              "menu.")
    else:
        player_controller = PlayerController()
        tournament_controller = TournamentController()
        round_controller = RoundController()
        match_controller = MatchController()
        main_view = MenuView()
        report_view = ReportView()
        application_controller = ApplicationController(player_controller,
                                                       tournament_controller,
                                                       round_controller,
                                                       match_controller,
                                                       main_view, report_view)
        application_controller.run()

        # start a round and update data json
        # last_round = last_tournament["rounds"][-1]

        # round_controller = RoundController()
        # round_start = round_controller.start_round()
        # round_number = last_round["name"][-1]
        # last_tournament["round_number"] = round_number
        # last_round["round_start_date"] = round_start
        # update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
        #                        last_tournament["tournament_id"],
        #                        last_tournament)

        # end a round and update data json
        # round_controller = RoundController()
        # round_end = round_controller.end_round()
        # last_round["round_end_date"] = round_end
        # update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
        #                        last_tournament["tournament_id"],
        #                        last_tournament)

        # # save score for match
        # match_controller = MatchController()
        # match_controller.save_score(last_tournament, last_round,
        #                             user_match_id="1", score1="1",
        #                             score2="0")
        # match_controller.save_score(last_tournament, last_round,
        #                             user_match_id="2", score1="1",
        #                             score2="1")


if __name__ == "__main__":
    initialize()
    main()
