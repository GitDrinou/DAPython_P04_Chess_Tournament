import json


class PlayerController:
    """Controller class for the player"""
    def __init__(self, players):
        """Initialise the controller with the a list of players"""
        self.players = players

    def add_player(self, player):
        """Add a player to the tournament"""
        self.players.append(player)

    def read_players_from_file(self):
        """Read players from JSON file"""
        try:
            with open("./data/tournaments/tournaments.json", "r") as players_file:
                data = json.load(players_file)
                data["players"] = self.players
                return data
        except FileNotFoundError:
            print("No players data found.")

    def write_players_to_file(self):
        """Write player to JSON file"""

        if self.read_players_from_file():
            """If JSON file exists, write to file"""

            players_for_json = []
            for player in self.players:
                players_for_json.append(player.to_dict())

            data = self.read_players_from_file()
            data["players"] = players_for_json

            with (open("./data/tournaments/tournaments.json", "w") as
                  players_file):
                json.dump(data, players_file, indent=4)
        else:
            print("No players data found.")

