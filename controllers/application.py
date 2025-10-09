from datetime import datetime

from models.player import Player
from models.tournament import Tournament
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, \
    PATH_DATA_PLAYERS_JSON_FILE, MESSAGES
from utils.file_utils import load_tournament, read_json_file
from utils.console_utils import clear_and_wait


class ApplicationController:
    """ Application class controller"""
    def __init__(self, player_controller, tournament_controller,
                 round_controller, match_controller, report_controller,
                 menu_view, prompt_view, display_view):
        """ Initialize the application controller """
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.round_controller = round_controller
        self.match_controller = match_controller
        self.report_controller = report_controller
        self.menu_view = menu_view
        self.prompt_view = prompt_view
        self.display_view = display_view

    def run(self):
        """ Main method of the application controller """

        while True:
            clear_and_wait(delay=0, console_view=self.menu_view)
            user_choice = self.menu_view.show_main_menu()

            if user_choice == "1":
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournament = self.prompt_view.tournament_prompt()
                clear_and_wait(delay=0, console_view=self.menu_view)
                self.tournament_controller.create(
                    Tournament(tournament["name"], tournament["location"],
                               tournament["start_date"],
                               tournament["end_date"],
                               tournament["description"],
                               tournament["number_of_rounds"]))
                clear_and_wait(delay=5)
            elif user_choice == "2":
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    selection = self.prompt_view.select_tournament_prompt()
                    if not selection == 0:
                        self.tournament_choice(selection)
                else:
                    clear_and_wait(message=MESSAGES["tournament_detail"])
            elif user_choice == "3":
                clear_and_wait(delay=0, console_view=self.menu_view)
                self.report_choice()
            elif user_choice == "4":
                clear_and_wait(message=MESSAGES["exit_application"],
                               level="INFO", console_view=self.menu_view,
                               clear_before=True)
                break
            else:
                clear_and_wait(message=MESSAGES["invalid_choice"], delay=3,
                               console_view=self.menu_view, clear_before=True)

    def tournament_choice(self, selection):
        """Display conditions for tournament choice"""

        while True:
            clear_and_wait(delay=0, console_view=self.menu_view)
            selected_tournament = load_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE, selection)
            self.display_view.display_players(selected_tournament)
            tournament_id = selected_tournament["tournament_id"]
            tournament_choice = self.menu_view.show_tournament_menu(
                tournament_id)
            tournament_id = selected_tournament["tournament_id"]
            if tournament_choice is not None:
                if tournament_choice == "1":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    if len(selected_tournament["rounds"]) == 0:
                        player = self.prompt_view.player_prompt()
                        self.player_controller.add(Player(
                            player["national_id"], player["lastname"],
                            player["firstname"], player["birthdate"]),
                            tournament_id)
                        clear_and_wait(delay=2)
                    else:
                        clear_and_wait(message=MESSAGES["register_players"],
                                       console_view=self.menu_view)
                elif tournament_choice == "2":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    if len(selected_tournament["rounds"]) == 0 and len(
                            selected_tournament["players"]) > 0:
                        self.display_view.display_players(
                            selected_tournament)
                        national_id = self.prompt_view.delete_player_prompt()
                        self.tournament_controller.delete_a_player(
                            selected_tournament["tournament_id"],
                            national_id)
                        clear_and_wait(delay=2, console_view=self.menu_view)
                    else:
                        clear_and_wait(message=MESSAGES["delete_player"],
                                       console_view=self.menu_view)
                elif tournament_choice == "3":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    last_round = selected_tournament["rounds"]
                    today = datetime.today().date()
                    start_date = selected_tournament["start_date"]
                    start_date = datetime.strptime(start_date,
                                                   "%d/%m/%Y")
                    if (len(selected_tournament["players"]) < 4 or len(
                            selected_tournament["players"]) % 2 != 0 or
                            start_date.date() > today):
                        clear_and_wait(message=MESSAGES["generate_round"],
                                       console_view=self.menu_view,
                                       clear_before=True)
                    else:
                        if len(last_round) == 0:
                            round_number = 0
                        else:
                            round_number = len(last_round)
                        finished_rounds = self.round_controller.is_finished(
                            selected_tournament["rounds"])
                        self.display_view.display_rounds(
                            selected_tournament["rounds"], finished_rounds)
                        selected_round = (
                            self.prompt_view.select_round_prompt())
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        if selected_round >= 0:
                            generation = (
                                self.tournament_controller.generate_a_round(
                                    round_number, selected_tournament[
                                        "players"], selected_tournament[
                                        "tournament_id"], selected_round))
                            if generation is not None:
                                self.menu_view.clear_console()
                                if (int(selected_tournament[
                                            "number_of_rounds"]) >=
                                        round_number):
                                    tournament_id = selected_tournament[
                                        "tournament_id"]
                                    self.round_choice(tournament_id)
                            else:
                                clear_and_wait(console_view=self.menu_view)
                        else:
                            clear_and_wait(delay=0,
                                           console_view=self.menu_view)
                elif tournament_choice == "4":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    break
                elif tournament_choice == "5":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    break
                else:
                    clear_and_wait(message=MESSAGES["invalid_choice"], delay=3,
                                   console_view=self.menu_view,
                                   clear_before=True)
            else:
                clear_and_wait(console_view=self.menu_view)
                break

    def round_choice(self, tournament_id):
        """ Display conditions for round choice"""

        while True:
            round_choice = (self.menu_view.show_round_menu())
            if round_choice == "1":
                clear_and_wait(delay=0, console_view=self.menu_view)
                round_detail = self.round_controller.start_up(tournament_id)
                clear_and_wait(delay=0, console_view=self.menu_view)
                self.display_view.display_a_round(round_detail)
            elif round_choice == "2":
                clear_and_wait(delay=0, console_view=self.menu_view)
                round_detail = self.round_controller.end_up(tournament_id)
                clear_and_wait(delay=0, console_view=self.menu_view)
                self.display_view.display_a_round(round_detail)
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournament = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE, tournament_id)
                last_round = tournament["rounds"][-1]
                if last_round["round_start_date"] == "":
                    break
                index = 0
                while index < len(last_round["matchs"]):
                    self.display_view.display_a_round(last_round)
                    match_id = index + 1
                    match = self.prompt_view.match_prompt(match_id)
                    if match is not None:
                        self.match_controller.save_score(
                            tournament, last_round["round_id"],
                            user_match_id=match_id, score1=match["score1"],
                            score2=match["score2"])
                        self.menu_view.clear_console()
                        index += 1
                self.tournament_controller.update_player_points(
                    tournament_id, last_round["round_id"])
                clear_and_wait(console_view=self.menu_view)
                break
            elif round_choice == "3":
                clear_and_wait(delay=0, console_view=self.menu_view)
                break
            else:
                clear_and_wait(message=MESSAGES["invalid_choice"], delay=3,
                               console_view=self.menu_view, clear_before=True)

    def report_choice(self):
        """Display conditions for report choice"""

        while True:
            report_choice = self.menu_view.show_report_menu()
            data_players = read_json_file(PATH_DATA_PLAYERS_JSON_FILE)
            data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
            if report_choice == "1":
                clear_and_wait(delay=0, console_view=self.menu_view)
                players = sorted(data_players["players"], key=lambda x: (x[
                    "last_name"]))
                self.report_controller.players(players)
                clear_and_wait(delay=10, console_view=self.menu_view)
            elif report_choice == "2":
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournaments = data_tournaments["tournaments"]
                self.report_controller.tournaments(tournaments)
                clear_and_wait(delay=10, console_view=self.menu_view)
            elif report_choice == "3":
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE, all_tournaments=True)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    tournament_id = self.prompt_view.select_tournament_prompt()
                    if tournament_id is not None:
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        tournaments = data_tournaments["tournaments"]
                        tournament_report = []
                        for tournament in tournaments:
                            if tournament["tournament_id"] == int(
                                    tournament_id):
                                tournament_report.append(tournament)
                                break
                        self.report_controller.tournaments(tournament_report)
                        clear_and_wait(delay=10, console_view=self.menu_view)
                else:
                    clear_and_wait(message=MESSAGES["tournament_detail"],
                                   console_view=self.menu_view,
                                   clear_before=True)
            elif report_choice == "4":
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE, all_tournaments=True)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    tournament_id = self.prompt_view.select_tournament_prompt()
                    if tournament_id is not None:
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        tournaments = data_tournaments["tournaments"]
                        tournament_report = {}
                        for tournament in tournaments:
                            if tournament["tournament_id"] == int(
                                    tournament_id):
                                tournament_report = tournament
                                break
                        self.report_controller.players(
                            tournament_report["players"], True,
                            tournament_report["name"])
                        clear_and_wait(delay=10, console_view=self.menu_view)
                else:
                    clear_and_wait(message=MESSAGES["tournament_detail"],
                                   console_view=self.menu_view,
                                   clear_before=True)
            elif report_choice == "5":
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE, all_tournaments=True)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    tournament_id = self.prompt_view.select_tournament_prompt()
                    if tournament_id is not None:
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        tournaments = data_tournaments["tournaments"]
                        tournament_report = {}
                        for tournament in tournaments:
                            if tournament["tournament_id"] == int(
                                    tournament_id):
                                tournament_report = tournament
                                break
                        self.report_controller.tournament_round(
                            tournament_report)
                        clear_and_wait(delay=10, console_view=self.menu_view)
                else:
                    clear_and_wait(message=MESSAGES["tournament_detail"],
                                   console_view=self.menu_view,
                                   clear_before=True)
            elif report_choice == "6":
                clear_and_wait(delay=0, console_view=self.menu_view)
                break
            else:
                clear_and_wait(message=MESSAGES["invalid_choice"], delay=3,
                               console_view=self.menu_view, clear_before=True)
