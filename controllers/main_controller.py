from core.exceptions import (PlayerRegistrationError, PlayerDeletionError,
                             RoundGenerationError, InvalidTournamentError,
                             NoPlayersError, NoTournamentsError,
                             InvalidTournamentsSelectionError)
from models.tournament_model import TournamentModel
from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, \
    PATH_DATA_PLAYERS_JSON_FILE, MESSAGES
from utils.file_utils import read_json_file
from utils.console_utils import clear_and_wait
from utils.tournament_utils import load_tournament


class MainController:
    """ Main class controller for the application"""

    def __init__(self, tournament_controller, tournament_model,
                 round_model,
                 match_model, report_controller, menu_view, prompt_view,
                 display_view):
        """Initialize the main controller
            Args:
                tournament_controller (TournamentController)
                tournament_model (TournamentModel): Tournament model
                round_model (RoundModel): Round model
                match_model (MatchModel): Match model
                report_controller (ReportController)
                menu_view (MenuView)
                prompt_view (PromptView)
                display_view (DisplayView)
        """
        self.tournament_controller = tournament_controller
        self.tournament_model = tournament_model
        self.round_model = round_model
        self.match_model = match_model
        self.report_controller = report_controller
        self.menu_view = menu_view
        self.prompt_view = prompt_view
        self.display_view = display_view

    def run(self):
        """Method to run the application"""

        while True:
            clear_and_wait(delay=0, console_view=self.menu_view)
            user_choice = self.menu_view.show_main_menu()

            if user_choice == "1":
                # Create a tournament
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournament = self.prompt_view.tournament_prompt()
                clear_and_wait(delay=0, console_view=self.menu_view)
                self.tournament_model.create(
                    TournamentModel(
                        None,
                        tournament["name"],
                        tournament["location"],
                        tournament["start_date"],
                        tournament["end_date"],
                        tournament["description"],
                        tournament["number_of_rounds"]
                    )
                )
                clear_and_wait(console_view=self.menu_view)
            elif user_choice == "2":
                # Start a tournament or continue a started tournament
                clear_and_wait(delay=0, console_view=self.menu_view)
                tournaments = load_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE)
                if tournaments:
                    self.display_view.display_tournaments(tournaments)
                    tournament_id = self.prompt_view.select_tournament_prompt()
                    if tournament_id > 0:
                        self._handle_tournament_choice(tournament_id)
                else:
                    clear_and_wait(message=MESSAGES["no_tournament_ongoing"])
            elif user_choice == "3":
                # Generates reports
                clear_and_wait(delay=0, console_view=self.menu_view)
                self._handle_report_choice()
            elif user_choice == "4":
                # exit the application
                clear_and_wait(message=MESSAGES["exit_application"],
                               level="INFO", console_view=self.menu_view,
                               clear_before=True)
                break
            else:
                clear_and_wait(message=MESSAGES["invalid_choice"], delay=3,
                               console_view=self.menu_view, clear_before=True)

    def _handle_tournament_choice(self, tournament_id):
        """Handle a tournament choice request
            Args:
                tournament_id (str): identifier of the tournament
        """
        while True:
            clear_and_wait(delay=0, console_view=self.menu_view)
            try:
                selected_tournament = load_tournament(
                    PATH_DATA_TOURNAMENTS_JSON_FILE,
                    tournament_id
                )
                if not selected_tournament:
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    raise InvalidTournamentError(
                        MESSAGES["failure_selected_tournament"]
                    )

                self.display_view.display_players(selected_tournament)
                tournament_choice = self.menu_view.show_tournament_menu(
                    selected_tournament["tournament_id"])
                if tournament_choice is not None:
                    if tournament_choice == "1":
                        # Register a player
                        self.tournament_controller.handle_player_registration(
                            selected_tournament)
                    elif tournament_choice == "2":
                        # Deletion a specific player
                        self.tournament_controller.handle_player_deletion(
                            selected_tournament)
                    elif tournament_choice == "3":
                        # Generate a round or continue a started round
                        self.tournament_controller.handle_round_generation(
                            selected_tournament)
                        clear_and_wait(delay=2, console_view=self.menu_view)
                    elif tournament_choice in ["4", "5"]:
                        # [4] Pause the tournament [5] Return to the main menu
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        break
                    else:
                        clear_and_wait(MESSAGES["invalid_choice"],
                                       console_view=self.menu_view)
                else:
                    clear_and_wait(delay=10, console_view=self.menu_view)
                    break

            except PlayerRegistrationError as e:
                clear_and_wait(str(e), level="ERROR",
                               console_view=self.menu_view)
            except PlayerDeletionError as e:
                clear_and_wait(str(e), level="ERROR",
                               console_view=self.menu_view)
            except RoundGenerationError as e:
                clear_and_wait(str(e), level="ERROR",
                               console_view=self.menu_view)
            except InvalidTournamentError as e:
                clear_and_wait(str(e), level="ERROR",
                               console_view=self.menu_view)
                break
            except Exception as e:
                clear_and_wait(f"Erreur inattendue : {str(e)}",
                               level="ERROR",
                               console_view=self.menu_view)

    def _select_tournament_and_generate_report(self, report_type):
        """Select a tournament and generate a specific report.
            Args:
                report_type: (str) report type to generate ("tournament",
                "players", "round")
            Return:
               Bool: True if report is generated, False otherwise.
        """

        tournaments = load_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                      all_tournaments=True)
        if not tournaments:
            raise NoTournamentsError(MESSAGES["failure_no_tournaments"])

        self.display_view.display_tournaments(tournaments)
        tournament_id = self.prompt_view.select_tournament_prompt()

        if tournament_id is None:
            raise InvalidTournamentsSelectionError(
                MESSAGES["failure_selected_tournament"]
            )

        clear_and_wait(delay=0, console_view=self.menu_view)
        tournament_report = next(
            (t for t in read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)[
                "tournaments"] if t["tournament_id"] == int(tournament_id)),
            None
        )

        if not tournament_report:
            raise InvalidTournamentsSelectionError(
                MESSAGES["failure_no_tournaments_found"]
            )

        if report_type == "tournament":
            self.report_controller.tournaments(tournament_report, unique=True)
        elif report_type == "players":
            self.report_controller.players(tournament_report["players"], True,
                                           tournament_report["name"])
        elif report_type == "rounds":
            self.report_controller.tournament_rounds(tournament_report)

        return True

    def _handle_report_choice(self):
        """Handle a report choice request"""
        while True:
            try:
                report_choice = self.menu_view.show_report_menu()
                data_players = read_json_file(PATH_DATA_PLAYERS_JSON_FILE)
                data_tournaments = read_json_file(
                    PATH_DATA_TOURNAMENTS_JSON_FILE
                )

                if report_choice == "1":
                    # Players report
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    players = sorted(data_players["players"], key=lambda x: (x[
                        "last_name"]))
                    if not players:
                        raise NoPlayersError(
                            MESSAGES["failure_no_players_found"])
                    self.report_controller.players(players)
                    clear_and_wait(delay=5, console_view=self.menu_view)
                elif report_choice == "2":
                    # Tournaments report
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    tournaments = data_tournaments["tournaments"]
                    if not tournaments:
                        raise NoTournamentsError(
                            MESSAGES["failure_no_tournaments_found"]
                        )
                    self.report_controller.tournaments(tournaments)
                    clear_and_wait(delay=5, console_view=self.menu_view)
                elif report_choice == "3":
                    # Tournament detail
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    self._select_tournament_and_generate_report("tournament")
                    clear_and_wait(delay=10, console_view=self.menu_view)
                elif report_choice == "4":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    self._select_tournament_and_generate_report("players")
                    clear_and_wait(delay=5, console_view=self.menu_view)
                elif report_choice == "5":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    self._select_tournament_and_generate_report("rounds")
                    clear_and_wait(delay=5, console_view=self.menu_view)
                elif report_choice == "6":
                    clear_and_wait(delay=0, console_view=self.menu_view)
                    break
                else:
                    clear_and_wait(message=MESSAGES["invalid_choice"],
                                   delay=3, console_view=self.menu_view,
                                   clear_before=True)

            except NoPlayersError as e:
                clear_and_wait(str(e), level="WARNING",
                               console_view=self.menu_view)
            except NoTournamentsError as e:
                clear_and_wait(str(e), level="WARNING",
                               console_view=self.menu_view)
            except InvalidTournamentsSelectionError as e:
                clear_and_wait(str(e), level="WARNING",
                               console_view=self.menu_view)
            except Exception as e:
                clear_and_wait(
                    f"{MESSAGES['failure']}:{str(e)}",
                    level="ERROR",
                    console_view=self.menu_view)
