import time

from models.player import Player
from models.tournament import Tournament
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import load_last_tournament


class ApplicationController:
    """ Application class controller"""
    def __init__(self, player_controller, tournament_controller,
                 round_controller, match_controller, menu_view, report_view):
        """ Initialize the application controller """
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.round_controller = round_controller
        self.match_controller = match_controller
        self.menu_view = menu_view
        self.report_view = report_view

    def run(self):
        """ Main method of the application controller """

        self.menu_view.show_menu()
        user_choice = self.menu_view.prompt_choice()
        last_tournament = load_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE)

        # user choice for main menu
        if user_choice == "1":
            self.menu_view.clear_console()
            player = self.menu_view.player_prompt()
            self.player_controller.add_player(Player(player["lastname"],
                                              player["firstname"]))
            time.sleep(2)
            self.menu_view.clear_console()
            self.menu_view.show_menu()
        elif user_choice == "2":
            self.menu_view.clear_console()
            tournament = self.menu_view.tournament_prompt()
            self.tournament_controller.add_new_tournament(
                Tournament(tournament["name"], tournament["location"],
                           tournament["start_date"], tournament["end_date"],
                           tournament["description"],
                           tournament["number_of_rounds"],
                           tournament["number_of_players"]),
                tournament["number_of_players"]
            )
            time.sleep(2)
            self.menu_view.clear_console()
            self.menu_view.show_menu()
        elif user_choice == "3":
            self.menu_view.clear_console()
            self.tournament_controller.generate_round(
                last_tournament["number_of_rounds"], 0,
                last_tournament["players"])
            time.sleep(2)
            self.menu_view.clear_console()
            round_choice = self.menu_view.round_prompt()
            if round_choice == "11":
                round_detail = self.round_controller.start_round()
                time.sleep(2)
                self.menu_view.clear_console()
                self.report_view.display_round_details(round_detail)
                self.menu_view.round_prompt()
            # TODO: display the round-detail
            # TODO: display the start and end match menu
        elif user_choice.upper() == "Q":
            print("Au revoir et à bientôt 👋.")
        else:
            print("Votre choix est invalide.")
