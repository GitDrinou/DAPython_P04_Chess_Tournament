from datetime import datetime

from utils.console_utils import ConsoleDisplayer
from core.constants import MESSAGES


def validate_date(date_to_validate):
    """Function to validate the date entered by the user
        Args:
            date_to_validate (str): Date entered by the user
    """
    date_to_validate = date_to_validate.strip()
    try:
        return datetime.strptime(date_to_validate, "%d/%m/%Y")
    except ValueError:
        ConsoleDisplayer.log(
            message="La date est invalide. Veuillez entrer une date "
                    "valide.\nFormat attendu : JJ/MM/AAAA",
            level="ERROR"
        )


def checks_dates(start_date, end_date):
    """Function to check if the end date is equal or later than the start
    date
        Args:
            start_date (str): Start date entered by the user
            end_date (str): End date entered by the user
    """
    if end_date >= start_date:
        return start_date, end_date
    else:
        return ConsoleDisplayer.log(MESSAGES["invalid_end_date"],
                                    level="WARNING")
