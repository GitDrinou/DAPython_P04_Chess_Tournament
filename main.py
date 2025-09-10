"""Entry point of the application."""
import json
import os

from controllers.player import PlayerController
# from controllers.tournament import TournamentController
from models.player import Player
# from models.tournament import Tournament
from utils.constants import PATH_DATA_JSON_FILE
# from utils.file_utils import read_file


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
    # Ajout d'un nouveau joueur dans la base JSON
    print("Ajouter un nouveau joueur:")
    last_name = input("Saisissez son nom de famille: ")
    first_name = input("Saisissez son prénom: ")

    # # add player to players
    player_controller = PlayerController()
    player_controller.add_player(Player(last_name, first_name))

    # data = read_file(PATH_DATA_JSON_FILE)

    # total_players = len(data["players"])
    # if total_players == 0:
    #     print("Vous n'avez pas de joueurs enregistrés dans votre base. "
    #           "Veuillez en saisir en utilisant l'option indiquée dans le "
    #           "menu.")
    # else:
    #   print("Ajouter un nouveau tournoi:")
    #   tournament_name = input("Saisissez le nom du tournoi:")
    #   tournament_location = input("Saisissez la localisation du tournoi:")
    #   tournament_start_date = input("Saisissez la date de début du tournoi:")
    #   tournament_end_date = input("Saisissez la date de fin du tournoi:")
    #   tournament_description = input("Saisissez la description du tournoi:")
    #   tournament_number_of_rounds = input("Saisissez le nombre de tours (si "
    #                                       "différent des 4 tours minimums "
    #                                       "par défaut:")
    #   tournament_number_of_players = input(f"Saisissez le nombre de "
    #                                        f"joueurs inscrits au tournoi ("
    #                                        f"maximum de {total_players}) :")
    #
    #     # Add a new tournament
    #     tournament_controller = TournamentController()
    #     tournament_controller.add_new_tournament(
    #         Tournament(tournament_name, tournament_location,
    #                    tournament_start_date, tournament_end_date,
    #                    tournament_description, tournament_number_of_rounds),
    #         tournament_number_of_players)


if __name__ == "__main__":
    initialize()
    main()
