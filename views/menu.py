import os


class MenuView:
    """Menu View class"""

    @staticmethod
    def show_menu():
        """Display the menu for the user"""
        print("Bienvenue sur le gestionnaire de tournoi.")
        print("Menu:")
        print("1. Ajouter un nouveau joueur")
        print("Tapez 'Q' pour quitter l'application")

    @staticmethod
    def prompt_choice():
        """Prompt the user to select an option"""
        return input("Choisissez une option: ")

    @staticmethod
    def clear_console():
        """Clear the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def player_prompt():
        """Prompt the user to enter player's lastname and firstname"""
        print("\nAJOUTER UN NOUVEAU JOUEUR")
        print("----------------------------")
        lastname = input("Saisissez le nom de famille du joueur: ")
        firstname = input("Saisissez le prénom du joueur: ")
        return {"lastname": lastname, "firstname": firstname}
