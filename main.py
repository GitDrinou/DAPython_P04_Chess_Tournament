"""Entry point of the application."""
from datetime import datetime

from controllers.player import PlayerController
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


def main():
    """Main entry point of the application."""

    # Static data player
    player1 = Player("A12345", "DOE","John")
    player2 = Player("A67890", "DOE","Jane")
    player3 = Player("B67890", "SMITH","Luke")
    player4 = Player("H45264", "HALL","Bob")
    player5 = Player("L98524", "JOHN","Anna")


    players = [player1, player2, player3, player4]
    round_players = players

    match1 = Match(player1, 0, player2, 0)
    match2 = Match(player3, 0, player4, 0)

    round1 = Round("Round 1", datetime.today(), datetime.today(),
                   round_players, matches=[match1, match2])

    tournament = Tournament("Tournoi Chess 75", "Paris 09", datetime.today(),
                            datetime.today(),"Tournoi de Paris 09. "
                                             "Inscriptions des candidats en "
                                             "ligne ou sur place dès 8h00 à "
                                             "l'entrée du bâtiment Hall A")

    tournament.rounds.append(round1)

    player_controller = PlayerController(players)
    player_controller.add_player(player5)
    player_controller.write_players_to_file()

    # Output
    print(tournament)


if __name__ == "__main__":
    main()