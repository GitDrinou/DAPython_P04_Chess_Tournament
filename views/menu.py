import os

from models.tournament import TournamentModel
from utils.console_utils import ConsoleDisplayer
from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES, TITLES, \
    SELECTIONS
from utils.file_utils import read_json_file
from utils.tournament_helpers import tournament_is_finished


class MenusView:
    """Class view with all different menus :
    - Main,
    - Tournament,
    - Round
    - Report"""
    def __init__(self):
        self.tournament_model = TournamentModel()

    @staticmethod
    def clear_console():
        """Clear the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_main_menu():
        """Method to display the main menu with title"""
        print("-" * 70)
        ConsoleDisplayer.display_print(TITLES["title_application"])
        print("-" * 70)
        options = [
            SELECTIONS["create_tournament"],
            SELECTIONS["start_or_continue_tournament"],
            SELECTIONS["generate_reports"],
            SELECTIONS["leave_application"]
        ]

        choice = ConsoleDisplayer.display_menu(
            title=TITLES["title_main_menu"],
            options=options
        )
        return choice

    @staticmethod
    def show_tournament_menu(tournament_id):
        """Display the current tournament menu
            Args:
                tournament_id (str): Identifier of the tournament
        """
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )
        if tournament:
            current_round_number = tournament["round_number"]
            number_pf_rounds = tournament["number_of_rounds"]

            if not tournament_is_finished(tournament):

                options = [
                    SELECTIONS["register_player"],
                    SELECTIONS["unregister_player"],
                    f"{SELECTIONS['generate_round']} "
                    f"{current_round_number}/{number_pf_rounds})",
                    SELECTIONS["pause_tournament"],
                    SELECTIONS["back_to_main_menu"]
                ]

                choice = ConsoleDisplayer.display_menu(
                    title=TITLES["title_tournament_menu"],
                    options=options,
                    current_round_number=current_round_number,
                    number_pf_rounds=number_pf_rounds
                )
                return choice
            else:
                return ConsoleDisplayer.log(MESSAGES["congratulations"],
                                            level="INFO")
        else:
            return None

    @staticmethod
    def show_round_menu():
        """Display the round menu for the current tournament"""

        options = [
            SELECTIONS["start_round"],
            SELECTIONS["end_round"],
            SELECTIONS["back_to_tournament_menu"]
        ]

        choice = ConsoleDisplayer.display_menu(
            title=TITLES["title_round_menu"],
            options=options
        )

        return choice

    @staticmethod
    def show_report_menu():
        """Display the report menu"""

        options = [
            SELECTIONS["players_list_report"],
            SELECTIONS["tournaments_list_report"],
            SELECTIONS["tournament_detail_report"],
            SELECTIONS["tournament_players_report"],
            SELECTIONS["tournament_rounds_report"],
            SELECTIONS["back_to_main_menu"]
        ]

        choice = ConsoleDisplayer.display_menu(
            title=TITLES["tile_reports_menu"],
            options=options
        )

        return choice
