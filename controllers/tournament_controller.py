from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, DEFAULT_SCORE, \
    MESSAGES
from core.exceptions import PlayerRegistrationError, PlayerDeletionError
from models.player_model import PlayerModel
from models.tournament_model import TournamentModel
from utils.console_utils import ConsoleDisplayer, clear_and_wait
from utils.file_utils import read_json_file, update_tournament
from utils.tournament_helpers import get_tournament_details
from views.menu_view import MenusView
from views.prompt_view import PromptView
from views.table_view import DisplayTableView


class TournamentController():
    def __init__(self):
        self.tournament = TournamentModel()
        self.menu_view = MenusView()
        self.prompt_view = PromptView()
        self.player_model = PlayerModel()
        self.display_view = DisplayTableView()

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
