"""Entry point of the application."""
from datetime import datetime

from models.match import Match
from models.player import Player
from models.round import Round


def main():
    """Main entry point of the application."""

    # Static data player
    player1 = Player("A12345", "DOE","John")
    player2 = Player("A67890", "DOE","Jane")
    player3 = Player("B67890", "SMITH","Luke")
    player4 = Player("H45264", "HALL","Bob")

    players = [player1, player2, player3, player4]
    round_players = players

    match1 = Match(player1, 0, player2, 0)
    match2 = Match(player3, 0, player4, 0)

    round1 = Round("Round 1", datetime.today(), datetime.today(),
                   round_players, matches=[match1, match2])

    # Output
    print("Joueurs de la base club:")
    for player in players:
        print(f"\t{player}")
    print(round1)


if __name__ == "__main__":
    main()