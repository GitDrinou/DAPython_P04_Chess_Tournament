import time
from datetime import datetime

from models.player import Player
from models.tournament import Tournament
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, \
    PATH_DATA_PLAYERS_JSON_FILE
from utils.file_utils import load_tournament, read_json_file
from views.messages import message_create_tournament, \
    message_quit_application, message_invalid_choice, \
    message_tournament_started, message_delete_player, message_generate_round


class ApplicationController:
    """ Application class controller"""
    def __init__(self, player_controller, tournament_controller,
                 round_controller, match_controller,
                 report_controller, menu_view, prompt_view, display_view):
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
            self.menu_view.clear_console()
            self.menu_view.show_main_menu()
            user_choice = self.prompt_view.prompt_choice()

            if user_choice == "1":
                self.menu_view.clear_console()
                tournament = self.prompt_view.tournament_prompt()
                self.tournament_controller.create(
                    Tournament(tournament["name"], tournament["location"],
                               tournament["start_date"],
                               tournament["end_date"],
                               tournament["description"],
                               tournament["number_of_rounds"]))
                time.sleep(2)
                self.menu_view.clear_console()
            elif user_choice == "2":
                self.menu_view.clear_console()
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    selection = self.prompt_view.select_tournament_prompt()
                    if not selection == 0:
                        self.tournament_choice(selection)
                else:
                    self.menu_view.clear_console()
                    print(message_create_tournament)
                    time.sleep(2)
                    self.menu_view.clear_console()
            elif user_choice == "3":
                self.menu_view.clear_console()
                self.report_choice()
            elif user_choice.upper() == "Q":
                self.menu_view.clear_console()
                print(message_quit_application)
                break
            else:
                self.menu_view.clear_console()
                print(message_invalid_choice)
                time.sleep(2)
                self.menu_view.clear_console()

    def tournament_choice(self, selection):
        """Display conditions for tournament choice"""

        while True:
            self.menu_view.clear_console()
            selected_tournament = load_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE, selection)
            self.display_view.display_players(selected_tournament)
            tournament_id = selected_tournament["tournament_id"]
            tournament_choice = self.menu_view.show_tournament_menu(
                tournament_id)
            tournament_id = selected_tournament["tournament_id"]
            if tournament_choice is not None:
                if tournament_choice == "1":
                    self.menu_view.clear_console()
                    if len(selected_tournament["rounds"]) == 0:
                        player = self.prompt_view.player_prompt()
                        self.player_controller.add(Player(
                            player["national_id"], player["lastname"],
                            player["firstname"], player["birthdate"]),
                            tournament_id)
                        time.sleep(2)
                        self.menu_view.clear_console()
                    else:
                        print(message_tournament_started)
                        time.sleep(3)
                        self.menu_view.clear_console()
                elif tournament_choice == "2":
                    self.menu_view.clear_console()
                    if len(selected_tournament["rounds"]) == 0 and len(
                            selected_tournament["players"]) > 0:
                        self.display_view.display_players(
                            selected_tournament)
                        national_id = self.prompt_view.delete_player_prompt()
                        self.tournament_controller.delete_a_player(
                            selected_tournament["tournament_id"],
                            national_id)
                        time.sleep(2)
                        self.menu_view.clear_console()
                    else:
                        print(message_delete_player)
                        time.sleep(3)
                        self.menu_view.clear_console()
                elif tournament_choice == "3":
                    self.menu_view.clear_console()
                    last_round = selected_tournament["rounds"]
                    today = datetime.today().date()
                    start_date = selected_tournament["start_date"]
                    start_date = datetime.strptime(start_date, "%d/%m/%Y")
                    if (len(selected_tournament["players"]) < 4 or len(
                            selected_tournament["players"]) % 2 != 0 or
                            start_date.date() > today):
                        self.menu_view.clear_console()
                        print(message_generate_round)
                        time.sleep(10)
                        self.menu_view.clear_console()
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
                        if not selected_round == -1:
                            generation = (
                                self.tournament_controller.generate_a_round(
                                    selected_tournament["number_of_rounds"],
                                    round_number, selected_tournament[
                                        "players"], selected_tournament[
                                        "tournament_id"], selected_round))
                            if generation is not None:
                                time.sleep(2)
                                self.menu_view.clear_console()
                                if (int(selected_tournament[
                                            "number_of_rounds"]) >=
                                        round_number):
                                    tournament_id = selected_tournament[
                                        "tournament_id"]
                                    self.round_choice(tournament_id)
                            else:
                                time.sleep(6)
                                self.menu_view.clear_console()
                        else:
                            self.menu_view.clear_console()
                elif tournament_choice == "4":
                    self.menu_view.clear_console()
                    break
                elif tournament_choice.upper() == "R":
                    self.menu_view.clear_console()
                    break
                else:
                    self.menu_view.clear_console()
                    print(message_invalid_choice)
                    time.sleep(2)
                    self.menu_view.clear_console()
            else:
                time.sleep(5)
                self.menu_view.clear_console()
                break

    def round_choice(self, tournament_id):
        """ Display conditions for round choice"""

        while True:
            round_choice = (self.menu_view.show_round_menu())
            if round_choice == "1":
                self.menu_view.clear_console()
                round_detail = self.round_controller.start_up(tournament_id)
                time.sleep(2)
                self.menu_view.clear_console()
                self.display_view.display_a_round(round_detail)
            elif round_choice == "2":
                self.menu_view.clear_console()
                round_detail = self.round_controller.end_up(tournament_id)
                time.sleep(2)
                self.menu_view.clear_console()
                self.display_view.display_a_round(round_detail)
                self.menu_view.clear_console()
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
                time.sleep(2)
                self.menu_view.clear_console()
                break
            elif round_choice.upper() == "R":
                self.menu_view.clear_console()
                break
            else:
                self.menu_view.clear_console()
                print(message_invalid_choice)
                time.sleep(2)
                self.menu_view.clear_console()

    def report_choice(self):
        """Display conditions for report choice"""

        while True:
            report_choice = self.menu_view.show_report_menu()
            data_players = read_json_file(PATH_DATA_PLAYERS_JSON_FILE)
            data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
            if report_choice == "1":
                self.menu_view.clear_console()
                players = sorted(data_players["players"], key=lambda x: (x[
                    "last_name"]))
                self.report_controller.players(players)
                time.sleep(10)
                self.menu_view.clear_console()
            elif report_choice == "2":
                self.menu_view.clear_console()
                tournaments = data_tournaments["tournaments"]
                self.report_controller.tournaments(tournaments)
                time.sleep(10)
                self.menu_view.clear_console()
            elif report_choice == "3":
                self.menu_view.clear_console()
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE, all_tournaments=True)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    tournament_id = self.prompt_view.select_tournament_prompt()
                    if tournament_id is not None:
                        self.menu_view.clear_console()
                        tournaments = data_tournaments["tournaments"]
                        tournament_report = []
                        for tournament in tournaments:
                            if tournament["tournament_id"] == int(
                                    tournament_id):
                                tournament_report.append(tournament)
                                break
                        self.report_controller.tournaments(tournament_report)
                        time.sleep(10)
                        self.menu_view.clear_console()
                else:
                    self.menu_view.clear_console()
                    print(message_create_tournament)
                    time.sleep(2)
                    self.menu_view.clear_console()
            elif report_choice == "4":
                self.menu_view.clear_console()
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE, all_tournaments=True)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    tournament_id = self.prompt_view.select_tournament_prompt()
                    if tournament_id is not None:
                        self.menu_view.clear_console()
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
                        time.sleep(10)
                        self.menu_view.clear_console()
                else:
                    self.menu_view.clear_console()
                    print(message_create_tournament)
                    time.sleep(2)
                    self.menu_view.clear_console()
            elif report_choice == "5":
                self.menu_view.clear_console()
                tournaments = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE, all_tournaments=True)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    tournament_id = self.prompt_view.select_tournament_prompt()
                    if tournament_id is not None:
                        self.menu_view.clear_console()
                        tournaments = data_tournaments["tournaments"]
                        tournament_report = {}
                        for tournament in tournaments:
                            if tournament["tournament_id"] == int(
                                    tournament_id):
                                tournament_report = tournament
                                break
                        self.report_controller.tournament_round(
                            tournament_report)
                        time.sleep(10)
                        self.menu_view.clear_console()
                else:
                    self.menu_view.clear_console()
                    print(message_create_tournament)
                    time.sleep(2)
                    self.menu_view.clear_console()
            elif report_choice.upper() == "R":
                self.menu_view.clear_console()
                break
            else:
                self.menu_view.clear_console()
                print(message_invalid_choice)
                time.sleep(2)
                self.menu_view.clear_console()
