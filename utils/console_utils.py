class ConsoleLogger:
    """Class to manage console print messages"""

    @staticmethod
    def log(message, level=None):
        levels = {
            "INFO": "[INFO]",
            "WARNING": "[ATTENTION]",
            "ERROR": "[ERREUR]",
        }

        print(f"\n\t{levels.get(level,'[ℹ️]')}\n\t{message}")
