import os

from utils.console_utils import ConsoleDisplayer
from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from utils.file_utils import read_json_file
from utils.tournament_utils import tournament_is_finished


class MenusView:
    """Class view with all different menus :
    - Main,
    - Tournament,
    - Round
    - Report"""

    @staticmethod
    def clear_console():
        """Clear the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_main_menu():
        """Method to display the main menu with title"""
        print("-" * 70)
        print("G E S T I O N N A I R E   D E   T O U R N O I S   D ' É C H "
              "E C S")
        print("-" * 70)
        options = [
            "Créer un nouveau tournoi",
            "Démarrer ou reprendre la gestion d'un tournoi",
            "Générer les rapports",
            "Quitter l'application"
        ]

        choice = ConsoleDisplayer.display_menu(
            title="Menu principal",
            options=options
        )
        return choice

    @staticmethod
    def show_tournament_menu(tournament_id):
        """Display the current tournament menu"""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )
        if tournament:
            current_round_number = tournament["round_number"]
            number_pf_rounds = tournament["number_of_rounds"]

            if not tournament_is_finished(tournament):

                options = [
                    "Inscrire un joueur au tournoi",
                    "Supprimer un joueur du tournoi",
                    f"Générer ou continuer un tour (tour "
                    f"{current_round_number}/{number_pf_rounds})",
                    "Mettre en pause le tournoi",
                    "Revenir au menu principal"
                ]

                choice = ConsoleDisplayer.display_menu(
                    title="Gestion d'un tournoi",
                    options=options,
                    current_round_number=current_round_number,
                    number_pf_rounds=number_pf_rounds
                )
                return choice
            else:
                return ConsoleDisplayer.log(MESSAGES["congratulations"],
                                            level="INFO")
        else:
            return None

    @staticmethod
    def show_round_menu():
        """Display the round menu for the current tournament"""

        options = [
            "Démarrer le tour",
            "Terminer le tour et saisir les scores des matchs",
            "Revenir au menu principal de l'application"
        ]

        choice = ConsoleDisplayer.display_menu(
            title="Gestion d'un tour",
            options=options
        )

        return choice

    @staticmethod
    def show_report_menu():
        """Display the report menu"""

        options = [
            "Liste des joueurs par ordre alphabétique",
            "Liste de tous les tournois",
            "Nom et dates d'un tournoi",
            "Liste des joueurs d'un tournoi par ordre alphabétique",
            "Liste de tous les tours du tournoi et de tous les matchs du tour",
            "Revenir au menu principal de l'application"
        ]

        choice = ConsoleDisplayer.display_menu(
            title="Génération de rapports",
            options=options
        )

        return choice
