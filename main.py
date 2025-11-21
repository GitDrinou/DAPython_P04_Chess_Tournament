"""Entry point of the application."""
import json
import os

from controllers.main_controller import MainController
from controllers.report_controller import ReportController
from controllers.tournament_controller import TournamentController
from core.constants import PATH_DATA
from models.match_model import MatchModel
from models.player_model import PlayerModel
from models.round_model import RoundModel
from models.tournament_model import TournamentModel
from views.menu_view import MenusView
from views.table_view import DisplayTableView
from views.prompt_view import PromptView


def init_json_file():
    """Initialize the json file"""

    data_dir = PATH_DATA
    os.makedirs(data_dir, exist_ok=True)

    files = {
        os.path.join(data_dir, "tournaments.json"): {
            "tournaments": []
        },
        os.path.join(data_dir, "players.json"): {
            "players": []
        }
    }

    for filepath, default_data in files.items():
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump(default_data, f, indent=4)


def main():
    """Main entry point of the application."""
    tournament_controller = TournamentController()
    tournament_model = TournamentModel()
    player_model = PlayerModel()
    round_model = RoundModel()
    match_model = MatchModel()
    report_controller = ReportController()
    main_view = MenusView()
    prompt_view = PromptView()
    display_view = DisplayTableView()
    application_controller = MainController(
        tournament_controller,
        tournament_model,
        player_model,
        round_model,
        match_model,
        report_controller,
        main_view, prompt_view,
        display_view)
    application_controller.run()


if __name__ == "__main__":
    init_json_file()
    main()
