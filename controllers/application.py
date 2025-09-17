import time

from models.player import Player
from models.tournament import Tournament


class ApplicationController:
    """ Application class controller"""
    def __init__(self, player_controller, tournament_controller,
                 round_controller, match_controller, menu_view):
        """ Initialize the application controller """
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.round_controller = round_controller
        self.match_controller = match_controller
        self.menu_view = menu_view

    def run(self):
        """ Main method of the application controller """
        self.menu_view.show_menu()
        user_choice = self.menu_view.prompt_choice()
        if user_choice == "1":
            self.menu_view.clear_console()
            player = self.menu_view.player_prompt()
            self.player_controller.add_player(Player(player["lastname"],
                                              player[
                "firstname"]))
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
        elif user_choice.upper() == "Q":
            print("Au revoir et à bientôt 👋.")
        else:
            print("Votre choix est invalide.")
