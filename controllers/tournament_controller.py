from core.constants import MESSAGES
from core.exceptions import PlayerRegistrationError, PlayerDeletionError, \
    RoundGenerationError, InvalidTournamentStateError
from models.player_model import PlayerModel
from models.round_model import RoundModel
from models.tournament_model import TournamentModel
from utils.console_utils import ConsoleDisplayer, clear_and_wait
from utils.round_helpers import validate_round_generation
from views.menu_view import MenusView
from views.prompt_view import PromptView
from views.table_view import DisplayTableView
from views.user_choice import UserChoice


class TournamentController:
    def __init__(self):
        self.tournament = TournamentModel()
        self.menu_view = MenusView()
        self.prompt_view = PromptView()
        self.player_model = PlayerModel()
        self.round = RoundModel()
        self.display_view = DisplayTableView()
        self.user = UserChoice()

    def handle_player_registration(self, selected_tournament):
        """Handle a player registration request
            Args:
                selected_tournament (tournament): data for a tournament
                selected by the user
        """
        clear_and_wait(delay=0, console_view=self.menu_view)
        if len(selected_tournament["rounds"]) > 0:
            raise PlayerRegistrationError(MESSAGES["no_registration_players"])

        player = self.prompt_view.player_prompt()
        try:
            new_player = PlayerModel(
                player["national_id"],
                player["last_name"],
                player["first_name"],
                player["birthdate"]
            )
            self.player_model.save_player_to_json(new_player)
            self.tournament.register_a_player(
                selected_tournament["tournament_id"],
                new_player.national_id,
            )
            clear_and_wait(delay=2)
        except Exception as e:
            raise PlayerRegistrationError(
                f"{MESSAGES['failure_registration']} : {str(e)}"
            )

    def handle_player_deletion(self, selected_tournament):
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
            self.tournament.unregister_a_player(
                tournament_id,
                national_id
            )
            clear_and_wait(delay=2)
        except Exception as e:
            raise PlayerDeletionError(
                f"{MESSAGES['failure_deletion']} : {str(e)}"
            )

    def handle_round_generation(self, selected_tournament):
        """Handle a round generation request
            Args:
                selected_tournament (tournament): data for a tournament
                selected by the user
        """
        clear_and_wait(delay=0, console_view=self.menu_view)
        rounds = selected_tournament["rounds"]
        validate_round_generation(selected_tournament)

        total_of_rounds = len(rounds)
        finished_rounds = self.round.is_finished(
            selected_tournament["rounds"])
        self.display_view.display_rounds(selected_tournament["rounds"],
                                         finished_rounds)

        selected_round = self.prompt_view.select_round_prompt()

        if selected_round < 0:
            return

        generation = (
            self.tournament.generate_a_round(
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
        self.user.handle_round_choice(
            selected_tournament["tournament_id"],
            selected_round
        )
