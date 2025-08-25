import json


class PlayerController:
    def __init__(self, players):
        self.players = players

    def add_player(self, player):
        """Add a player to the tournament"""
        self.players.append(player)

    def write_players_to_file(self):
        """Write player to JSON file"""
        players_for_json = []
        for player in self.players:
            players_for_json.append(player.to_dict())

        with open("./data/players/players.json", "w") as players_file:
            json.dump(players_for_json, players_file)


