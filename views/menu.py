import os

from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import read_json_file
from utils.tournament_utils import tournament_is_finished


class MenuView:
    """Menu View class"""

    @staticmethod
    def show_main_menu():
        """Display the main menu"""
        print("G E S T I O N N A I R E   D E   T O U R N O I S   D ' É C H "
              "E C S\n")
        print("Menu principal:")
        print("=====================================================")
        print("1. Créer un nouveau tournoi")
        print("2. Démarrer ou reprendre la gestion d'un tournoi")
        print("3. Générer les rapports")
        print("Q. Quitter l'application")
        print("=====================================================")

    @staticmethod
    def clear_console():
        """Clear the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_tournament_menu(tournament_id):
        """Display the current tournament menu"""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        for tournament in tournaments:
            if tournament["tournament_id"] == tournament_id:
                current_round_number = tournament["round_number"]
                number_pf_rounds = tournament["number_of_rounds"]
                if tournament_is_finished(tournament):
                    print("\nGESTION DU TOURNOI")
                    print("==================================================")
                    print("1. Inscrire des joueurs au tournoi")
                    print("2. Supprimer un joueur du tournoi")
                    print(f"3. Générer ou continuer un tour (tour"
                          f" {current_round_number}/{number_pf_rounds})")
                    print("4. Mettre en pause le tournoi")
                    print("R. Revenir au menu principal de l'application")
                    print("==================================================")
                    tournament_choice = input("Choisissez une option: ")

                    return tournament_choice
        return None

    @staticmethod
    def show_round_menu():
        """Display the round menu for the current tournament"""
        print("\nGESTION D'UN TOUR:")
        print("=====================================================")
        print("1. Démarrer le tour")
        print("2. Terminer le tour et inscrire les scores des matchs")
        print("R. Revenir au menu principal de l'application")
        print("=====================================================")
        round_choice = input("Choisissez une option: ")

        return round_choice

    @staticmethod
    def show_report_menu():
        """Display the report menu"""
        print("\nGENERATION DE RAPPORTS")
        print("=====================================================")
        print("1. Liste des joueurs par ordre alphabétique")
        print("2. Liste de tous les tournois")
        print("3. Nom et dates d’un tournoi")
        print("4. Liste des joueurs d'un tournoi par ordre alphabétique")
        print("5. Liste de tous les tours du tournoi et de tous les matchs "
              "du tour.")
        print("R. Revenir au menu principal de l'application")
        print("=====================================================")
        report_choice = input("Choisissez une option: ")

        return report_choice
