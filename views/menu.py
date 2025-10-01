import os

from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.date_utils import validate_date, checks_dates
from utils.file_utils import read_json_file
from utils.player_utils import check_format_national_id, check_player_is_exist


class MenuView:
    """Menu View class"""

    @staticmethod
    def show_menu():
        """Display the menu for the user"""
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
    def prompt_choice():
        """Prompt the user to select an option"""
        return input("Choisissez une option: ")

    @staticmethod
    def clear_console():
        """Clear the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def date_player_prompt():
        """Prompt the user to enter the player's birthdate"""

        while True:
            birth_date = input("Saisissez la date de naissance du joueur ("
                               "format attendu: JJ/MM/AAAA): ")

            birth_date = validate_date(birth_date)

            if birth_date:
                break

        return birth_date

    def player_prompt(self):
        """Prompt the user to enter player's lastname and firstname"""
        while True:
            print("\nINSCRIPTION DE JOUEURS")
            print("=====================================================")
            national_id = input("Saisissez l'identifiant national du joueur: ")

            if check_format_national_id(national_id) is not None:
                player = check_player_is_exist(national_id)
                if player is not None:
                    national_id = player["national_id"],
                    lastname = player["last_name"]
                    firstname = player["first_name"]
                    birthdate = player["birthdate"]
                    player = {
                        "national_id": national_id,
                        "lastname": lastname,
                        "firstname": firstname,
                        "birthdate": birthdate.strftime("%d/%m/%Y")
                    }
                    break
                else:
                    lastname = input("Saisissez le nom de famille du joueur: ")
                    firstname = input("Saisissez le prénom du joueur: ")
                    birthdate = self.date_player_prompt()
                    player = {
                        "national_id": national_id,
                        "lastname": lastname,
                        "firstname": firstname,
                        "birthdate": birthdate.strftime("%d/%m/%Y")
                    }
                    break
            else:
                print("Le format de l'identitifant national est incorrect."
                      "\nFormat attendu : 1 lettre + 5 chiffres")

        return player

    @staticmethod
    def dates_tournament_prompt():
        """Prompt the user to enter date of tournament"""

        while True:
            start_date = input("Saisissez la date de début du tournoi (format "
                               "attendu: JJ/MM/AAAA): ")
            end_date = input("Saisissez la date de fin du tournoi (format "
                             "attendu: JJ/MM/AAAA): ")

            start_date = validate_date(start_date)
            end_date = validate_date(end_date)

            if (start_date and end_date) and checks_dates(start_date,
                                                          end_date):
                break

        return {
            "start_date": start_date,
            "end_date": end_date
        }

    def tournament_prompt(self):
        """Prompt the user to enter tournament's details"""

        print("\nCREATION D'UN NOUVEAU TOURNOI")
        print("=====================================================")
        name = input("Saisissez le nom du tournoi: ")
        location = input("Saisissez la localisation du tournoi: ")
        description = input("Saisissez une description du tournoi: ")
        number_of_rounds = input("Saisissez le nombre de tours (par défaut: "
                                 "4): ")

        dates = self.dates_tournament_prompt()

        return {
            "name": name,
            "location": location,
            "start_date": dates["start_date"],
            "end_date": dates["end_date"],
            "description": description,
            "number_of_rounds": number_of_rounds
        }

    @staticmethod
    def tournament_menu_prompt():
        """Display the submenu for the current tournament"""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data_tournaments["tournaments"][-1]
        current_round_number = last_tournament["round_number"]
        number_pf_rounds = last_tournament["number_of_rounds"]
        if current_round_number == number_pf_rounds:
            print("\n🎉 🎉 Le tournoi est terminé. Félicitations au vainqueur "
                  "🏆!")
            print("\n........................................................")
        print("\nGESTION DU TOURNOI")
        print("=====================================================")
        print("1. Inscrire des joueurs au tournoi")
        print(f"2. Générer ou continuer un tour (tour {current_round_number}"
              f"/{number_pf_rounds})")
        print("3. Mettre en pause le tournoi")
        print("R. Revenir au menu principal de l'application")
        print("=====================================================")
        tournament_choice = input("Choisissez une option: ")

        return tournament_choice

    @staticmethod
    def select_tournament_prompt():
        """Prompt the user to select a tournament"""
        while True:
            print("\nSÉLECTIONNER UN TOURNOI")
            print("=====================================================")
            tournament_id = input("Saisissez l'identifiant du tournoi: ")

            try:
                tournament_id = int(tournament_id)
                break
            except ValueError:
                print("La valeur n'existe pas.")

        return tournament_id

    @staticmethod
    def select_round_prompt():
        """Prompt the user to select a round"""
        while True:
            print("\nSÉLECTIONNER UN TOUR")
            print("=====================================================")
            round_id = input("Saisissez l'identifiant du tour ou tapez "
                             "ENTREE pour générer un nouveau tour: ")

            if round_id == "":
                round_id = 0
                break
            else:
                try:
                    round_id = int(round_id)
                    break
                except ValueError:
                    print("La valeur n'existe pas.")

        return round_id

    @staticmethod
    def round_prompt():
        """Display the submenu for a specific theme"""
        print("\nGESTION D'UN TOUR:")
        print("=====================================================")
        print("1. Démarrer le tour")
        print("2. Terminer le tour et inscrire les scores des matchs")
        print("R. Revenir au menu principal de l'application")
        print("=====================================================")
        round_choice = input("Choisissez une option: ")

        return round_choice

    @staticmethod
    def match_prompt(match_id):
        """Prompt the user to enter the match's scores"""
        print(f"\nINSCRIRE LES SCORES DU MATCH N°{match_id}")
        print("=====================================================")
        score1 = input("Saisissez le score du joueur 1 - Score 1 (0 ou 1): ")
        score2 = input("Saisissez le score du joueur 2 - Score 2 (0 ou 1): ")

        return {
            "score1": score1,
            "score2": score2
        }

    @staticmethod
    def delete_player_prompt():
        """Prompt the user to delete a player"""
        print("\nSUPPRIMER UN JOUEUR")
        print("=====================================================")
        national_id = input("Saisissez l'identifiant du joueur: ")

        return national_id

    @staticmethod
    def reports_prompt():
        """Prompt the user to generate reports"""
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

    @staticmethod
    def report_tournament_prompt():
        """Prompt the user to enter the tournament id"""
        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]

        tournament_id = input("Saisissez l'identifiant du tournoi: ")

        is_exist = False

        print(type(tournament_id))
        for tournament in tournaments:
            if tournament["tournament_id"] == int(tournament_id):
                is_exist = True

        if is_exist:
            return tournament_id
        else:
            print("\n........................................................")
            print("\nL'identifiant du tournoi n'existe pas.")
            return None
