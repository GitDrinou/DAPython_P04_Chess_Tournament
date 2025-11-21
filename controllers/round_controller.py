from core.constants import MESSAGES, PATH_DATA_TOURNAMENTS_JSON_FILE
from core.exceptions import RoundEndError, MatchScoreError
from models.match_model import MatchModel
from models.round_model import RoundModel
from models.tournament_model import TournamentModel
from utils.console_utils import clear_and_wait
from utils.file_utils import update_tournament
from utils.tournament_utils import load_tournament
from views.menu_view import MenusView
from views.prompt_view import PromptView
from views.table_view import DisplayTableView


class RoundController:
    """Round controller class"""
    def __init__(self):
        self.tournament = TournamentModel()
        self.round = RoundModel()
        self.display_view = DisplayTableView()
        self.prompt_view = PromptView()
        self.match = MatchModel()
        self.menu_view = MenusView()

    def handle_round_end(self, selected_tournament, selected_round):
        """Handle a round end request
            Args:
                selected_tournament (str): identifier of the tournament
                selected_round (int): identifier of the selected round
        """
        try:
            round_ = self.round.end_up(
                int(selected_tournament),
                selected_round
            )

            if not round_:
                raise RoundEndError(MESSAGES["failure_end_of_round"])

            self.display_view.display_a_round(round_)
            tournament = load_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                                         selected_tournament)

            self._check_round_started(tournament)
            last_round = tournament["rounds"][-1]
            for match_id, match in enumerate(last_round["matchs"], start=1):
                if len(match["match"]) == 1:
                    continue
                match_score = self.prompt_view.match_prompt(match_id)
                if not match_score:
                    raise MatchScoreError(MESSAGES["failure_invalid_score"],
                                          match_id=match_id)

                try:
                    self.match.save_scores(
                        tournament, last_round["round_id"],
                        match_id=match_id, score1=match_score["score1"],
                        score2=match_score["score2"])
                except Exception as e:
                    raise MatchScoreError(
                        f"{MESSAGES['failure_saved_score']}: {str(e)}",
                        match_id=match_id)

            self.tournament.update_players_points(
                int(selected_tournament),
                last_round["round_id"]
            )

            return True

        except RoundEndError:
            raise
        except Exception as e:
            raise RoundEndError(f"{MESSAGES['failure_saved_round']}: {str(e)}")

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
