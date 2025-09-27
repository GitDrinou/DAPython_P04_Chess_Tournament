import time

from models.player import Player
from models.tournament import Tournament
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, \
    PATH_DATA_PLAYERS_JSON_FILE
from utils.file_utils import load_tournament, read_json_file


class ApplicationController:
    """ Application class controller"""
    def __init__(self, player_controller, tournament_controller,
                 round_controller, match_controller,
                 report_controller, menu_view, display_view):
        """ Initialize the application controller """
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.round_controller = round_controller
        self.match_controller = match_controller
        self.report_controller = report_controller
        self.menu_view = menu_view
        self.display_view = display_view

    def run(self):
        """ Main method of the application controller """
        while True:
            self.menu_view.clear_console()
            self.menu_view.show_menu()
            user_choice = self.menu_view.prompt_choice()

            # user choice for main menu
            if user_choice == "1":
                self.menu_view.clear_console()
                tournament = self.menu_view.tournament_prompt()
                self.tournament_controller.add(
                    Tournament(tournament["name"], tournament["location"],
                               tournament["start_date"],
                               tournament["end_date"],
                               tournament["description"],
                               tournament["number_of_rounds"]))
                time.sleep(2)
                self.menu_view.clear_console()
            elif user_choice == "2":
                self.menu_view.clear_console()
                last_tournament = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE)
                if last_tournament["is_on_break"]:
                    self.tournament_controller.unpause(
                        last_tournament["tournament_id"])
                while True:
                    last_tournament = load_tournament(
                        PATH_DATA_TOURNAMENTS_JSON_FILE)
                    self.display_view.display_players(
                        last_tournament)
                    tournament_choice = self.menu_view.tournament_menu_prompt()

                    if tournament_choice == "1":
                        self.menu_view.clear_console()
                        if len(last_tournament["rounds"]) == 0:
                            player = self.menu_view.player_prompt()
                            self.player_controller.add(
                                Player(player["national_id"], player[
                                    "lastname"], player["firstname"]))
                            time.sleep(2)
                            self.menu_view.clear_console()
                        else:
                            print("\nLe tournoi a déjà démarré, vous ne "
                                  "pouvez plus inscrire de nouveaux "
                                  "joueurs.")
                            time.sleep(3)
                            self.menu_view.clear_console()
                    elif tournament_choice == "2":
                        self.menu_view.clear_console()
                        if len(last_tournament["rounds"]) == 0 and len(
                                last_tournament["players"]) > 0:
                            self.display_view.display_players(
                                last_tournament)
                            national_id = self.menu_view.delete_player_prompt()
                            self.tournament_controller.delete_a_player(
                                last_tournament["tournament_id"], national_id)
                            time.sleep(2)
                            self.menu_view.clear_console()
                        else:
                            print("\nVous ne pouvez pas supprimer de "
                                  "joueur, soit parce que le tournoi a déjà "
                                  "démarré, soit parce qu'il n'y a pas de "
                                  "joueurs inscrits au tournoi.")
                            time.sleep(3)
                            self.menu_view.clear_console()
                    elif tournament_choice == "3":
                        self.menu_view.clear_console()
                        last_round = last_tournament["rounds"]
                        if len(last_tournament["players"]) < 4 or len(
                                last_tournament["players"]) % 2 != 0:
                            self.menu_view.clear_console()
                            print("..........................................")
                            print("Vous n'avez pas assez de joueurs inscrits "
                                  "pour pouvoir générer un tour.\nVeuillez "
                                  "continuer à inscrire des joueurs au "
                                  "tournoi.\nLe minimum attendu est de 4 "
                                  "joueurs et le total doit être un nombre "
                                  "pair.")
                            print("..........................................")
                            time.sleep(3)
                            self.menu_view.clear_console()
                        else:
                            if len(last_round) == 0:
                                round_number = 0
                            else:
                                round_number = len(last_round)
                            self.tournament_controller.generate_round(
                                last_tournament["number_of_rounds"],
                                round_number,
                                last_tournament["players"])
                            time.sleep(2)
                            self.menu_view.clear_console()
                            if (int(last_tournament["number_of_rounds"]) >
                                    round_number):
                                while True:
                                    round_choice = (
                                        self.menu_view.round_prompt())
                                    if round_choice == "1":
                                        self.menu_view.clear_console()
                                        round_detail = (
                                            self.round_controller
                                            .start_up())
                                        time.sleep(2)
                                        self.menu_view.clear_console()
                                        self.display_view.display_round(
                                            round_detail)
                                    elif round_choice == "2":
                                        self.menu_view.clear_console()
                                        round_detail = (
                                            self.round_controller.end_up())
                                        time.sleep(2)
                                        self.menu_view.clear_console()
                                        (self.display_view
                                            .display_round(round_detail))
                                        self.menu_view.clear_console()
                                        last_tournament = (
                                            load_tournament(
                                                PATH_DATA_TOURNAMENTS_JSON_FILE
                                            ))
                                        last_round = last_tournament[
                                            "rounds"][-1]
                                        if (last_round["round_start_date"] ==
                                                ""):
                                            break
                                        index = 0
                                        while index < len(last_round[
                                                              "matchs"]):
                                            (self
                                             .display_view.
                                             display_round(last_round))
                                            match_id = index + 1
                                            match =\
                                                (self.menu_view
                                                    .match_prompt(match_id))
                                            self.match_controller.save_score(
                                                last_tournament,
                                                last_round["round_id"],
                                                user_match_id=match_id,
                                                score1=match["score1"],
                                                score2=match["score2"])
                                            self.menu_view.clear_console()
                                            index += 1
                                        (self.tournament_controller
                                            .update_player_points(
                                                last_round["round_id"]))
                                        time.sleep(2)
                                        self.menu_view.clear_console()
                                        break
                                    elif round_choice.upper() == "R":
                                        self.menu_view.clear_console()
                                        break
                    elif tournament_choice == "4":
                        self.menu_view.clear_console()
                        last_tournament = load_tournament(
                            PATH_DATA_TOURNAMENTS_JSON_FILE)
                        self.tournament_controller.pause(
                            last_tournament["tournament_id"])
                        time.sleep(2)
                        self.menu_view.clear_console()
                        break
                    elif tournament_choice == "R":
                        self.menu_view.clear_console()
                        break
            elif user_choice == "3":
                self.menu_view.clear_console()
                while True:
                    report_choice = self.menu_view.reports_prompt()
                    data_players = read_json_file(PATH_DATA_PLAYERS_JSON_FILE)
                    data_tournaments = read_json_file(
                        PATH_DATA_TOURNAMENTS_JSON_FILE)
                    if report_choice == "1":
                        self.menu_view.clear_console()
                        players = sorted(data_players["players"],
                                         key=lambda x: (x["last_name"]))
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
                        tournament_id \
                            = self.menu_view.report_tournament_prompt()
                        self.menu_view.clear_console()
                        tournaments = data_tournaments["tournaments"]
                        for tournament in tournaments:
                            if (tournament.get('tournament_id') ==
                                    tournament_id):
                                (self.report_controller
                                    .tournaments([tournament]))
                                break
                        time.sleep(10)
                        self.menu_view.clear_console()
                    elif report_choice == "4":
                        self.menu_view.clear_console()
                        tournament_id \
                            = self.menu_view.report_tournament_prompt()
                        self.menu_view.clear_console()
                        tournaments = data_tournaments["tournaments"]
                        for tournament in tournaments:
                            if (tournament.get('tournament_id') ==
                                    tournament_id):
                                (self.report_controller
                                 .players(tournament["players"], True,
                                          tournament["name"]))
                                break
                        time.sleep(10)
                        self.menu_view.clear_console()
                    elif report_choice.upper() == "R":
                        self.menu_view.clear_console()
                        break
            elif user_choice.upper() == "Q":
                print("Au revoir et à bientôt 👋.")
                break
            else:
                print("Votre choix est invalide.")
