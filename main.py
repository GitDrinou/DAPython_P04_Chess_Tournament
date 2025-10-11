"""Entry point of the application."""
import json
import os

from controllers.application import ApplicationController
from controllers.match import MatchController
from controllers.player import PlayerController
from controllers.report import ReportController
from controllers.round import RoundController
from controllers.tournament import TournamentController
from core.constants import PATH_DATA
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

    player_controller = PlayerController()
    tournament_controller = TournamentController()
    round_controller = RoundController()
    match_controller = MatchController()
    report_controller = ReportController()
    main_view = MenusView()
    prompt_view = PromptView()
    display_view = DisplayTableView()
    application_controller = ApplicationController(player_controller,
                                                   tournament_controller,
                                                   round_controller,
                                                   match_controller,
                                                   report_controller,
                                                   main_view, prompt_view,
                                                   display_view)
    application_controller.run()


if __name__ == "__main__":
    init_json_file()
    main()
