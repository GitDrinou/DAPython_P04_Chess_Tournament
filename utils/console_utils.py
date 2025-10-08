class ConsoleDisplayer:
    """Class to manage console print messages"""

    @staticmethod
    def log(message, level=None):
        levels = {
            "INFO": "[INFO]",
            "WARNING": "[ATTENTION]",
            "ERROR": "[ERREUR]",
        }

        print(f"\n\t{levels.get(level,'[ℹ️]')}\n\t{message}")

    @staticmethod
    def display_menu(title, options, **kwargs):
        """Display a dynamic menu with user options and optional value
        Args:
            title (str): title of the menu
            options (list): list of options
            **kwargs: optional variable(s) to add in a manu option
        """

        print(f"\n{title}")
        print("*" * 50)
        for i, option in enumerate(options, start=1):
            formatted_option = option.format(**kwargs)
            print(f"[{i}] {formatted_option}")
        print("*" * 50)
        choice = input("Choisissez une option: ")

        return choice
