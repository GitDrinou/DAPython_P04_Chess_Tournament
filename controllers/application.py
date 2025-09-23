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
        while True:
            self.menu_view.clear_console()
            self.menu_view.show_menu()
            user_choice = self.menu_view.prompt_choice()

            # user choice for main menu
            if user_choice == "1":
                self.menu_view.clear_console()
                player = self.menu_view.player_prompt()
                self.player_controller.add_player(Player(player["lastname"],
                                                  player["firstname"]))
                time.sleep(2)
                self.menu_view.clear_console()
            elif user_choice == "2":
                self.menu_view.clear_console()
                tournament = self.menu_view.tournament_prompt()
                self.tournament_controller.add_new_tournament(
                    Tournament(tournament["name"], tournament["location"],
                               tournament["start_date"],
                               tournament["end_date"],
                               tournament["description"],
                               tournament["number_of_rounds"],
                               tournament["number_of_players"]),
                    tournament["number_of_players"]
                )
                time.sleep(2)
                self.menu_view.clear_console()
            elif user_choice == "3":
                self.menu_view.clear_console()
                last_tournament = load_last_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE)
                last_round = last_tournament["rounds"]
                if len(last_round) == 0:
                    round_number = 0
                else:
                    round_number = len(last_round)
                self.tournament_controller.generate_round(
                    last_tournament["number_of_rounds"], round_number,
                    last_tournament["players"])
                time.sleep(2)
                self.menu_view.clear_console()
                while True:
                    round_choice = self.menu_view.round_prompt()
                    if round_choice == "11":
                        self.menu_view.clear_console()
                        round_detail = self.round_controller.start_round()
                        time.sleep(2)
                        self.menu_view.clear_console()
                        self.report_view.display_round_details(round_detail)
                    elif round_choice == "13":
                        self.menu_view.clear_console()
                        round_detail = self.round_controller.end_round()
                        time.sleep(2)
                        self.menu_view.clear_console()
                        self.report_view.display_round_details(round_detail)
                        self.menu_view.clear_console()
                        last_tournament = load_last_tournament(
                            PATH_DATA_TOURNAMENTS_JSON_FILE)
                        last_round = last_tournament["rounds"][-1]
                        index = 0
                        while index < len(last_round["matchs"]):
                            self.report_view.display_round_details(last_round)
                            match_id = index + 1
                            match = self.menu_view.match_prompt(match_id)
                            self.match_controller.save_score(
                                last_tournament,
                                user_match_id=match_id,
                                score1=match["score1"],
                                score2=match["score2"])
                            self.menu_view.clear_console()
                            index += 1
                        # self.tournament_controller.update_player_points()
                        time.sleep(2)
                        self.menu_view.clear_console()
                        break
                    elif round_choice == "15":
                        self.menu_view.clear_console()
                        break
            elif user_choice.upper() == "Q":
                print("Au revoir et à bientôt 👋.")
                break
            else:
                print("Votre choix est invalide.")
