"""Entry point of the application."""
import json
import os

from controllers.round import RoundController
# from controllers.player import PlayerController
# from controllers.tournament import TournamentController
# from models.player import Player
# from models.tournament import Tournament
from utils.constants import (PATH_DATA_TOURNAMENTS_JSON_FILE,
                             PATH_DATA_PLAYERS_JSON_FILE)
from utils.file_utils import (read_file, load_last_tournament,
                              update_last_tournament)


def initialize():
    """Initialize the application."""

    if not os.path.isfile(PATH_DATA_PLAYERS_JSON_FILE):
        default_data = {"players": [], }
        with open(PATH_DATA_PLAYERS_JSON_FILE, "w",
                  encoding="utf-8") as json_file:
            json.dump(default_data, json_file, indent=4)

    if not os.path.isfile(PATH_DATA_TOURNAMENTS_JSON_FILE):
        default_data = {"tournaments": [],}
        with open(PATH_DATA_TOURNAMENTS_JSON_FILE, "w", encoding="utf-8") as json_file:
            json.dump(default_data, json_file, indent=4)


def main():
    """Main entry point of the application."""
    # # Ajout d'un nouveau joueur dans la base JSON
    # print("Ajouter un nouveau joueur:")
    # last_name = input("Saisissez son nom de famille: ")
    # first_name = input("Saisissez son prénom: ")
    #
    # # # add player to players
    # player_controller = PlayerController()
    # player_controller.add_player(Player(last_name, first_name))

    data_players = read_file(PATH_DATA_PLAYERS_JSON_FILE)
    # data_tournaments = read_file(PATH_DATA_TOURNAMENTS_JSON_FILE)

    total_players = len(data_players["players"])
    if total_players == 0:
        print("Vous n'avez pas de joueurs enregistrés dans votre base. "
              "Veuillez en saisir en utilisant l'option indiquée dans le "
              "menu.")
    else:
        # print("Ajouter un nouveau tournoi:")
        # tournament_name = input("Saisissez le nom du tournoi:")
        # tournament_location = input("Saisissez la localisation du tournoi:")
        # tournament_start_date = input("Saisissez la date de début du
        # tournoi: ")
        # tournament_end_date = input("Saisissez la date de fin du tournoi:")
        # tournament_description = input("Saisissez la description du
        # tournoi: ")
        # tournament_number_of_rounds = input("Saisissez le nombre de tours
        # (si"
        #                                     "différent des 4 tours minimums "
        #                                     "par défaut:")
        # tournament_number_of_players = input(f"Saisissez le nombre de "
        #                                      f"joueurs inscrits au tournoi ("
        #                                      f"maximum de {total_players} "
        #                                      f"joueurs) :")
        # #  Add a new tournament
        # tournament_controller = TournamentController()
        # tournament_detail = tournament_controller.add_new_tournament(
        #       Tournament(tournament_name, tournament_location,
        #                  tournament_start_date, tournament_end_date,
        #                  tournament_description, tournament_number_of_rounds
        #                  ),
        #       tournament_number_of_players)
        #
        # tournament_controller_round = TournamentController()
        # round_detail = tournament_controller_round.generate_round(
        #     tournament_detail["number_of_rounds"], 0,
        #     tournament_detail["players"])
        #
        # save_to_json("tournaments",
        #              tournament_id=tournament_detail["tournament_id"],
        #              name=tournament_detail["name"],
        #              location=tournament_detail["location"],
        #              start_date=tournament_detail["start_date"],
        #              end_date=tournament_detail["end_date"],
        #              description=tournament_detail["description"],
        #              number_of_rounds=tournament_detail["number_of_rounds"],
        #              round_number=tournament_detail["round_number"],
        #              players=tournament_detail["players"],
        #              rounds=[round_detail]
        #              )

        last_tournament = load_last_tournament(
            PATH_DATA_TOURNAMENTS_JSON_FILE, "tournaments")
        last_round = last_tournament["rounds"][-1]
        round_controller = RoundController()
        round_start = round_controller.start_round()
        round_number = last_round["name"][-1]
        last_tournament["round_number"] = round_number
        last_round["round_start_date"] = round_start
        update_last_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE, last_tournament)


if __name__ == "__main__":
    initialize()
    main()
