"""Entry point of the application."""
import json
import os

from controllers.main import MainController
from controllers.report import ReportController
from controllers.tournament import TournamentController
from core.constants import PATH_DATA
from models.round import RoundModel
from models.tournament import TournamentModel
from views.menu import MenusView
from views.display_table import DisplayTableView
from views.prompt import PromptView


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
    tournament_model = TournamentModel()
    tournament_controller = TournamentController()
    round_model = RoundModel()
    report_controller = ReportController()
    main_view = MenusView()
    prompt_view = PromptView()
    display_view = DisplayTableView()
    application_controller = MainController(tournament_model,
                                            tournament_controller,
                                            round_model,
                                            report_controller,
                                            main_view, prompt_view,
                                            display_view)
    application_controller.run()


if __name__ == "__main__":
    init_json_file()
    main()
