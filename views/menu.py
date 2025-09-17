import os

from utils.constants import PATH_DATA_PLAYERS_JSON_FILE
from utils.file_utils import read_file


class MenuView:
    """Menu View class"""
    data_players = read_file(PATH_DATA_PLAYERS_JSON_FILE)

    @staticmethod
    def show_menu():
        """Display the menu for the user"""
        print("Menu de l'application:")
        print("*************************************************")
        print("1. Ajouter un nouveau joueur")
        print("2. Ajouter un nouveau tournoi")
        print("*************************************************")

    @staticmethod
    def prompt_choice():
        """Prompt the user to select an option"""
        return input("Choisissez une option ou tapez 'Q' pour quitter "
                     "l'application: ")

    @staticmethod
    def clear_console():
        """Clear the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def player_prompt():
        """Prompt the user to enter player's lastname and firstname"""
        print("\nAJOUTER UN NOUVEAU JOUEUR")
        print("----------------------------")
        lastname = input("Saisissez le nom de famille du joueur: ")
        firstname = input("Saisissez le prénom du joueur: ")
        return {"lastname": lastname, "firstname": firstname}

    def tournament_prompt(self):
        """Prompt the user to enter tournament's details"""
        total_players = len(self.data_players["players"])
        print("\nAJOUTER UN NOUVEAU TOURNOI")
        print("----------------------------")
        name = input("Saisissez le nom du tournoi: ")
        location = input("Saisissez la localisation du tournoi: ")
        start_date = input("Saisissez la date de début du tournoi (format "
                           "attendu: JJ/MM/AAAA): ")
        end_date = input("Saisissez la date de fin du tournoi (format "
                         "attendu: JJ/MM/AAAA): ")
        description = input("Saisissez une description du tournoi: ")
        number_of_rounds = input("Saisissez le nombre de tours (par défaut: "
                                 "4): ")
        number_of_players = input(f"Saisissez le nombre de joueurs inscrits "
                                  f"au tournoi (maximum de {total_players} "
                                  f"joueurs) : ")
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "number_of_rounds": number_of_rounds,
            "number_of_players": number_of_players
        }
