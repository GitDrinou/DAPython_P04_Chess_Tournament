"""Entry point of the application."""
from models.player import Player


def main():
    """Main entry point of the application."""
    player1 = Player("A12345", "DOE","John")
    player2 = Player("A67890", "DOE","Jane")

    players = [player1, player2]
    for player in players:
        print(player)


if __name__ == "__main__":
    main()