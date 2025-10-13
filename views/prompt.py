from datetime import datetime

from utils.console_utils import ConsoleDisplayer
from core.constants import MESSAGES
from utils.date_utils import validate_date, checks_dates
from utils.player_utils import check_format_national_id, check_player_is_exist


class PromptView:
    """Prompt view class"""

    @staticmethod
    def birthdate_player_prompt():
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
            national_id = ConsoleDisplayer.display_prompt(
                text="Saisissez l'identifiant national du joueur",
                title="INSCRIPTION D'UN JOUEUR"
            )

            if check_format_national_id(national_id):
                player = check_player_is_exist(national_id)
                if player is not None:
                    birthdate = datetime.strptime(player["birth_date"],
                                                  "%d/%m/%Y")
                    player = {
                        "national_id": national_id,
                        "lastname": player["last_name"],
                        "firstname": player["first_name"],
                        "birthdate": birthdate.strftime("%d/%m/%Y"),
                    }
                    break
                else:
                    lastname = ConsoleDisplayer.display_prompt(
                        text="Saisissez le nom de famille du joueur")
                    firstname = ConsoleDisplayer.display_prompt(
                        text="Saisissez le prénom du joueur")
                    birthdate = self.birthdate_player_prompt()
                    player = {
                        "national_id": national_id,
                        "lastname": lastname,
                        "firstname": firstname,
                        "birthdate": birthdate.strftime("%d/%m/%Y"),
                    }
                    break
            else:
                ConsoleDisplayer.log(MESSAGES["invalid_national_id"],
                                     level="WARNING")

        return player

    @staticmethod
    def dates_tournament_prompt():
        """Prompt the user to enter date of tournament"""

        while True:
            start_date = ConsoleDisplayer.display_prompt(
                text="Saisissez la date de début du tournoi "
                     "(format attendu: JJ/MM/AAAA)")
            end_date = ConsoleDisplayer.display_prompt(
                text="Saisissez la date de fin du tournoi "
                     "(format attendu: JJ/MM/AAAA)")

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

        name = ConsoleDisplayer.display_prompt(
            text="Saisissez le nom du tournoi",
            title="CRÉATION D'UN NOUVEAU TOURNOI")
        location = ConsoleDisplayer.display_prompt(
            text="Saisissez la localisation du tournoi")
        description = ConsoleDisplayer.display_prompt(
            text="Saisissez une description du tournoi")
        number_of_rounds = ConsoleDisplayer.display_prompt(
            text="Saisissez le nombre de tours (par défaut 4)")

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
    def select_tournament_prompt():
        """Prompt the user to select a tournament"""

        while True:

            tournament_id = ConsoleDisplayer.display_prompt(
                text="Saisissez l'identifiant du tournoi parmi la liste "
                     "ci-dessus\nou pour revenir au menu précédent, tapez sur "
                     "la touche R de votre clavier.",
                title="SÉLECTION D'UN TOURNOI"
            )

            try:
                if not tournament_id.upper() == "R":
                    tournament_id = int(tournament_id)
                    break
                else:
                    tournament_id = 0
                    break
            except ValueError:
                ConsoleDisplayer.log(MESSAGES["invalid_choice"],
                                     level="WARNING")

        return tournament_id

    @staticmethod
    def select_round_prompt():
        """Prompt the user to select a round"""
        while True:
            round_id = ConsoleDisplayer.display_prompt(
                text="Les différentes possibilités:\n\t- saisir "
                     "l'identifiant du tour en cours\n\t- taper sur la "
                     "touche ENTREE de votre clavier pour générer un nouveau "
                     "tour\n\t- taper sur la tour R de votre clavier pour "
                     "revenir au menu précédent\nChoisissez une option",
                title="SÉLECTIONNER UN TOUR"
            )

            try:
                if round_id == "":
                    round_id = 0
                    break
                elif round_id.upper() == "R":
                    round_id = -1
                    break
                else:
                    round_id = int(round_id)
                    break
            except ValueError:
                print("La valeur n'existe pas.")

        return round_id

    @staticmethod
    def match_prompt(match_id):
        """Prompt the user to enter the match's scores"""
        while True:

            print(f"\nINSCRIRE LES SCORES DU MATCH N°{match_id}")
            print("*" * 70)
            print("Instructions:")
            print("\t- [1] pour le vainqueur du match")
            print("\t- [0] pour le perdant du match")
            print("\t- En cas de match nul, saisissez [1] pour les 2 scores")
            print("*" * 70)

            score1 = ConsoleDisplayer.display_prompt(
                text="Saisissez le score du joueur 1 | Score 1")
            score2 = ConsoleDisplayer.display_prompt(
                text="Saisissez le score du joueur 2 | Score 2")

            expected_values = ["0", "1"]
            if score1 in expected_values and score2 in expected_values:
                scores = {
                    "score1": score1,
                    "score2": score2
                }
                break
            else:
                ConsoleDisplayer.log(MESSAGES["invalid_choice"],
                                     level="WARNING")

        return scores

    @staticmethod
    def delete_player_prompt():
        """Prompt the user to delete a player"""

        national_id = ConsoleDisplayer.display_prompt(
            text="Saisissez l'identifiant du joueur",
            title="DÉSINSCRIRE UN JOUEUR"
        )

        return national_id
