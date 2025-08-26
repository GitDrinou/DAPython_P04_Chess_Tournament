"""Entry point of the application."""
import json
import os
import random
from datetime import datetime

from controllers.player import PlayerController
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from utils.constants import PATH_DATA_JSON_FILE


def initialize():
    """Initialize the application."""
    default_json = {
        "players": [],
        "tournaments": [],
    }
    if not os.path.isfile(PATH_DATA_JSON_FILE):
        with open(PATH_DATA_JSON_FILE, "w", encoding="utf-8") as json_file:
            json.dump(default_json, json_file, indent=4)


def main():
    """Main entry point of the application."""

    # Static data player
    player1 = Player("A12345", "DOE", "John")
    player2 = Player("A67890", "DOE", "Jane")
    player3 = Player("B67890", "SMITH", "Luke")
    player4 = Player("H45264", "HALL", "Bob")
    player5 = Player("L98524", "JOHN", "Anna")
    player6 = Player("W57894", "BURTON", "Charles")
    player7 = Player("D98766", "JAMES", "Olivia")

    # add player to players
    player_controller = PlayerController()
    player_controller.add_player(player1)
    player_controller.add_player(player2)
    player_controller.add_player(player3)
    player_controller.add_player(player4)
    player_controller.add_player(player5)
    player_controller.add_player(player6)
    player_controller.add_player(player7)

    player_controller.write_players_to_file()
    json_players = player_controller.read_players_from_file()

    tournament_description = ("Tournoi de Paris 09. Inscriptions des "
                              "candidats en ligne ou sur place dès 8h00 à "
                              "l'entrée du bâtiment Hall A")

    tournament = Tournament("Tournoi Chess 75", "Paris 09", datetime.today(),
                            datetime.today(), tournament_description)

    random_players = random.sample(json_players["players"], 4)
    tournament.players.append(random_players)

    round1 = Round("Round 1", datetime.today(), datetime.today(),
                   random_players)
    tournament.rounds.append(round1)

    # Output
    print(json_players)
    print(tournament)


if __name__ == "__main__":
    initialize()
    main()
