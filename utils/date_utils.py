from datetime import datetime


def validate_date(date_to_validate):
    """Function to validate the date entered by the user"""
    try:
        return datetime.strptime(date_to_validate, "%d/%m/%Y")
    except ValueError:
        print(f"La date {date_to_validate} est invalide. Veuillez entrer une "
              f"date valide.")


def checks_dates(start_date, end_date):
    """Function to check if the end date is equal or later than the start
    date"""
    if end_date >= start_date:
        return start_date, end_date
    else:
        return print("La date de fin doit être égale ou postérieure à la "
                     "date de début. Veuillez entrer une date valide.")
