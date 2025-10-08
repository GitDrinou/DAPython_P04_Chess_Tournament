"""Entry point of the application."""
import json
import os

from controllers.application import ApplicationController
from controllers.match import MatchController
from controllers.player import PlayerController
from controllers.report import ReportController
from controllers.round import RoundController
from controllers.tournament import TournamentController
from utils.constants import (PATH_DATA_TOURNAMENTS_JSON_FILE,
                             PATH_DATA_PLAYERS_JSON_FILE)
from views.menu import MenusView
from views.display_table import DisplayTableView
from views.prompt import PromptView


def initialize():
    """Initialize the application."""

    if not os.path.isfile(PATH_DATA_PLAYERS_JSON_FILE):
        default_data = {"players": [], }
        with open(PATH_DATA_PLAYERS_JSON_FILE, "w",
                  encoding="utf-8") as json_file:
            json.dump(default_data, json_file, indent=4)

    if not os.path.isfile(PATH_DATA_TOURNAMENTS_JSON_FILE):
        default_data = {"tournaments": [], }
        with (open(PATH_DATA_TOURNAMENTS_JSON_FILE, "w", encoding="utf-8")
              as json_file):
            json.dump(default_data, json_file, indent=4)


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
    initialize()
    main()
