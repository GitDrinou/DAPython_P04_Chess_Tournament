from datetime import datetime

from core.exceptions import (PlayerRegistrationError, PlayerDeletionError,
                             RoundGenerationError, InvalidTournamentStateError,
                             InvalidTournamentError, RoundEndError,
                             MatchScoreError, RoundStartError, NoPlayersError,
                             NoTournamentsError,
                             InvalidTournamentsSelectionError)
from models.player_model import PlayerModel
from models.tournament_model import TournamentModel
from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, \
    PATH_DATA_PLAYERS_JSON_FILE, MESSAGES, ALLOW_BYES
from utils.file_utils import read_json_file, update_tournament
from utils.console_utils import clear_and_wait, ConsoleDisplayer
from utils.tournament_utils import load_tournament


class MainController:
    """ Main class controller for the application"""

    def __init__(self, tournament_model, round_model,
                 match_model, report_controller, menu_view, prompt_view,
                 display_view):
        """Initialize the main controller
            Args:
                tournament_model (TournamentModel): Tournament model
                round_model (RoundModel): Round model
                match_model (MatchModel): Match model
                report_controller (ReportController)
                menu_view (MenuView)
                prompt_view (PromptView)
                display_view (DisplayView)
        """
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

    def _handle_player_registration(self, selected_tournament):
        """Handle a player registration request
            Args:
                selected_tournament (tournament): data for a tournament
                selected by the user
        """
        clear_and_wait(delay=0, console_view=self.menu_view)
        tournament_id = selected_tournament["tournament_id"]
        if len(selected_tournament["rounds"]) > 0:
            raise PlayerRegistrationError(MESSAGES["no_registration_players"])

        player = self.prompt_view.player_prompt()
        try:
            self.tournament_model.register_a_player(
                PlayerModel(
                    player["national_id"],
                    player["lastname"],
                    player["firstname"],
                    player["birthdate"]
                ),
                tournament_id
            )
            clear_and_wait(delay=2)
        except Exception as e:
            raise PlayerRegistrationError(
                f"{MESSAGES['failure_registration']} : {str(e)}"
            )

    def _handle_player_deletion(self, selected_tournament):
        """Handle a player deletion request
            Args:
                selected_tournament (tournament): data for a tournament
                selected by the user
        """
        clear_and_wait(delay=0, console_view=self.menu_view)
        if len(selected_tournament["rounds"]) > 0 or len(
                selected_tournament["players"]) == 0:
            raise PlayerDeletionError(MESSAGES["no_deletion_possible"])

        self.display_view.display_players(selected_tournament)
        national_id = self.prompt_view.delete_player_prompt()
        tournament_id = selected_tournament["tournament_id"]

        try:
            self.tournament_model.unregister_a_player(
                tournament_id,
                national_id
            )
            clear_and_wait(delay=2)
        except Exception as e:
            raise PlayerDeletionError(
                f"{MESSAGES['failure_deletion']} : {str(e)}"
            )

    @staticmethod
    def _validate_round_generation(selected_tournament):
        """Validate a round generation
            Args:
                selected_tournament (tournament): data for a tournament
        """
        number_of_rounds = int(selected_tournament["number_of_rounds"])

        if ALLOW_BYES:
            # If number of rounds is odd, players = rounds
            # if number of rounds id even, players = rounds - 1
            if number_of_rounds % 2 == 1:
                min_players = number_of_rounds
            else:
                min_players = number_of_rounds - 1
        else:
            # if no BYE, number of players must be even, and we round up
            # to the next even
            number_of_players = number_of_rounds - 1
            if number_of_players % 2 == 1:
                min_players = number_of_players
            else:
                min_players = number_of_players - 1

        if len(selected_tournament["players"]) > min_players:
            raise RoundGenerationError(
                f"{MESSAGES['invalide_number_of_players']} {min_players}"
            )

        today = datetime.today().date()
        start_date = datetime.strptime(selected_tournament["start_date"],
                                       "%d/%m/%Y")
        if start_date.date() > today:
            raise RoundGenerationError(MESSAGES["no_generate_due_to_date"])

    def _handle_round_generation(self, selected_tournament):
        """Handle a round generation request
            Args:
                selected_tournament (tournament): data for a tournament
                selected by the user
        """
        clear_and_wait(delay=0, console_view=self.menu_view)
        rounds = selected_tournament["rounds"]
        self._validate_round_generation(selected_tournament)

        total_of_rounds = len(rounds)
        finished_rounds = self.round_model.is_finished(
            selected_tournament["rounds"])
        self.display_view.display_rounds(selected_tournament["rounds"],
                                         finished_rounds)

        selected_round = self.prompt_view.select_round_prompt()

        if selected_round < 0:
            return

        generation = (
            self.tournament_model.generate_a_round(
                round_number=total_of_rounds,
                players=selected_tournament["players"],
                tournament_id=selected_tournament["tournament_id"],
                round_id=selected_round
            )
        )

        if generation == "round_already_ended":
            ConsoleDisplayer.log(MESSAGES["round_already_ended"],
                                 level="WARNING")
            return

        if generation is None:
            clear_and_wait(console_view=self.menu_view)
            raise RoundGenerationError(MESSAGES["no_generate_round"])

        if int(selected_tournament["number_of_rounds"]) < total_of_rounds:
            raise InvalidTournamentStateError(MESSAGES["all_rounds_reached"])

        clear_and_wait(delay=0, console_view=self.menu_view)
        self._handle_round_choice(selected_tournament["tournament_id"],
                                  selected_round)

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
                        self._handle_player_registration(selected_tournament)
                    elif tournament_choice == "2":
                        # Deletion a specific player
                        self._handle_player_deletion(selected_tournament)
                    elif tournament_choice == "3":
                        # Generate a round or continue a started round
                        self._handle_round_generation(selected_tournament)
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

    def _check_round_started(self, tournament):
        last_round = tournament["rounds"][-1]
        if last_round["round_start_date"] == "":
            clear_and_wait(delay=0, console_view=self.menu_view)
            last_round["round_end_date"] = ""
            update_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE,
                tournament["tournament_id"],
                tournament
            )
            raise RoundEndError(MESSAGES["round_not_started"])

    def _handle_round_end(self, tournament_id, selected_round):
        """Handle a round end request
            Args:
                tournament_id (str): identifier of the tournament
                selected_round (int): identifier of the selected round
        """
        try:
            round_ = self.round_model.end_up(
                tournament_id,
                selected_round
            )

            if not round_:
                raise RoundEndError(MESSAGES["failure_end_of_round"])

            self.display_view.display_a_round(round_)
            tournament = load_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                         tournament_id)

            self._check_round_started(tournament)
            last_round = tournament["rounds"][-1]
            for match_id, match in enumerate(last_round["matchs"], start=1):
                self.display_view.display_a_round(last_round)
                if len(match["match"]) == 1:
                    continue
                match_score = self.prompt_view.match_prompt(match_id)
                if not match_score:
                    raise MatchScoreError(MESSAGES["failure_invalid_score"],
                                          match_id=match_id)

                try:
                    self.match_model.save_scores(
                        tournament, last_round["round_id"],
                        match_id=match_id, score1=match_score["score1"],
                        score2=match_score["score2"])
                except Exception as e:
                    raise MatchScoreError(
                        f"{MESSAGES['failure_saved_score']}: {str(e)}",
                        match_id=match_id)

            self.tournament_model.update_players_points(
                int(tournament_id),
                last_round["round_id"]
            )

            return True

        except RoundEndError:
            raise
        except Exception as e:
            raise RoundEndError(f"{MESSAGES['failure_saved_round']}: {str(e)}")

    def _handle_round_choice(self, tournament_id, selected_round):
        """Handle a round choice request
            Args:
                tournament_id (str): identifier of the tournament
                selected_round (int): identifier of the selected round
        """
        while True:
            try:
                round_choice = self.menu_view.show_round_menu()
                if round_choice == "1":
                    # Start the round
                    try:
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        round_ = self.round_model.start_up(
                            tournament_id,
                            selected_round
                        )
                        if not round_:
                            raise RoundStartError(
                                MESSAGES["failure_started_round"]
                            )
                        clear_and_wait(delay=3, console_view=self.menu_view)
                        self.display_view.display_a_round(round_)
                    except RoundStartError as e:
                        clear_and_wait(str(e), level="ERROR",
                                       console_view=self.menu_view)
                elif round_choice == "2":
                    # Terminate the round
                    try:
                        if self._handle_round_end(tournament_id,
                                                  selected_round):
                            break
                    except RoundEndError as e:
                        clear_and_wait(str(e), level="ERROR",
                                       console_view=self.menu_view)
                    except MatchScoreError as e:
                        clear_and_wait(str(e), level="ERROR",
                                       console_view=self.menu_view)
                elif round_choice == "3":
                    # Return to the previous menu
                    break
                else:
                    clear_and_wait(message=MESSAGES["invalid_choice"], delay=3,
                                   console_view=self.menu_view,
                                   clear_before=True)

            except Exception as e:
                clear_and_wait(
                    f"Erreur inattendue : {str(e)}",
                    level="ERROR",
                    console_view=self.menu_view
                )

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
