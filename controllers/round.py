from datetime import datetime


class RoundController:
    """Round controller class"""

    @staticmethod
    def start_round():
        """Method that starts a round."""
        start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return start_date

    @staticmethod
    def end_round():
        """Method that ends a round."""
        end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return end_date
