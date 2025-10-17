from datetime import datetime

from utils.console_utils import ConsoleDisplayer
from core.constants import MESSAGES, TITLES, INSTRUCTIONS, LOSE_VALUE, \
    WIN_VALUE
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
                text=INSTRUCTIONS["national_id_input"],
                title=TITLES["title_player_registration"],
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
                        text=INSTRUCTIONS["last_name_input"])
                    firstname = ConsoleDisplayer.display_prompt(
                        text=INSTRUCTIONS["first_name_input"])
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
                text=INSTRUCTIONS["tournament_start_input"])
            end_date = ConsoleDisplayer.display_prompt(
                text=INSTRUCTIONS["tournament_end_input"])

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
            text=INSTRUCTIONS["tournament_name_input"],
            title=TITLES["title_tournament_creation"])
        location = ConsoleDisplayer.display_prompt(
            text=INSTRUCTIONS["tournament_localisation_input"])
        description = ConsoleDisplayer.display_prompt(
            text=INSTRUCTIONS["tournament_description_input"])
        number_of_rounds = ConsoleDisplayer.display_prompt(
            text=INSTRUCTIONS["tournament_number_round_input"])

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
                text=INSTRUCTIONS["tournament_id_input"],
                title=TITLES["title_tournament_selection"]
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
                text=INSTRUCTIONS["round_id_input"],
                title=INSTRUCTIONS["title_round_selection"]
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
                ConsoleDisplayer.display_print(MESSAGES["value_not_exist"])

        return round_id

    @staticmethod
    def match_prompt(match_id):
        """Prompt the user to enter the match's scores"""
        while True:
            ConsoleDisplayer.display_print(
                f"{TITLES['title_match_score']}{match_id}")
            print("*" * 70)
            ConsoleDisplayer.display_print(MESSAGES["scores_instructions"])
            print("*" * 70)

            score1 = ConsoleDisplayer.display_prompt(
                text=INSTRUCTIONS["save_score1_input"])
            score2 = ConsoleDisplayer.display_prompt(
                text=INSTRUCTIONS["save_score2_input"])

            expected_values = [LOSE_VALUE, WIN_VALUE]
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
            text=INSTRUCTIONS["national_id_input"],
            title=TITLES["title_player_deletion"]
        )

        return national_id
