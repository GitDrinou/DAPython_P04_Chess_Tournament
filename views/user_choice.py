from controllers.round_controller import RoundController
from core.constants import MESSAGES
from core.exceptions import RoundStartError, RoundEndError, MatchScoreError
from models.round_model import RoundModel
from models.tournament_model import TournamentModel
from utils.console_utils import clear_and_wait
from views.menu_view import MenusView
from views.table_view import DisplayTableView


class UserChoice:
    """User choice class"""
    def __init__(self):
        self.menu_view = MenusView()
        self.tournament = TournamentModel()
        self.round = RoundModel()
        self.display_view = DisplayTableView()
        self.round_controller = RoundController()

    def handle_round_choice(self, selected_tournament, selected_round):
        """Handle a round choice request
            Args:
                selected_tournament (str): identifier of the tournament
                selected_round (int): identifier of the selected round
        """
        while True:
            try:
                round_choice = self.menu_view.show_round_menu()
                if round_choice == "1":
                    # Start the round
                    try:
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        round_ = self.round.start_up(
                            int(selected_tournament),
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
                        clear_and_wait(delay=0, console_view=self.menu_view)
                        if self.round_controller.handle_round_end(
                                selected_tournament, selected_round):
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
