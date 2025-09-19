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
        print("3. Générer un tour")
        print("Q. Quitter l'application")
        print("*************************************************")

    @staticmethod
    def prompt_choice():
        """Prompt the user to select an option"""
        return input("Choisissez une option: ")

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

    @staticmethod
    def round_prompt():
        """Display the submenu for a specific theme"""
        print("GESTION D'UN TOUR:")
        print("*************************************************")
        print("11. Démarrer le tour")
        print("12. Mettre en pause le tour")
        print("13. Terminer le tour")
        print("14. Inscrire les scores des matchs du tour")
        print("15. Revenir au menu principal de l'application")
        print("*************************************************")
        round_choice = input("Choisissez une option: ")

        return round_choice

    @staticmethod
    def match_prompt(match_id):
        """Prompt the user to enter the match's scores"""
        print(f"INSCRIRE LES SCORES DU MATCH N°{match_id}")
        print("*************************************************")
        score1 = input("Saisissez le score du joueur 1 - Score 1 (0 ou 1): ")
        score2 = input("Saisissez le score du joueur 2 - Score 2 (0 ou 1): ")

        return {
            "score1": score1,
            "score2": score2
        }
