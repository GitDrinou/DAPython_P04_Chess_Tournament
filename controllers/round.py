from datetime import datetime


class RoundController:
    """Round controller class"""

    @staticmethod
    def start_round():
        """Method that starts a round."""
        start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return start_date
