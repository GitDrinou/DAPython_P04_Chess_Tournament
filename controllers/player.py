from utils.constants import PATH_DATA_TOURNAMENTS_JSON_FILE
from utils.file_utils import save_to_json, update_tournament, read_json_file
from utils.player_utils import check_player_is_exist


class PlayerController:

    @staticmethod
    def add(player):
        """Add a player to the tournament"""

        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        last_tournament = data_tournaments["tournaments"][-1]

        last_tournament["players"].append({
            "national_id": player.national_id.capitalize(),
            "last_name": player.last_name.upper(),
            "first_name": player.first_name.capitalize(),
            "points": 0.0
        })

        update_tournament(PATH_DATA_TOURNAMENTS_JSON_FILE,
                          last_tournament["tournament_id"],
                          last_tournament)

        if not check_player_is_exist(player.national_id):
            save_to_json("players",
                         national_id=player.national_id.capitalize(),
                         last_name=player.last_name.upper(),
                         first_name=player.first_name.capitalize())

        print("=====================================================")
        print("\nLe joueur a été inscrit au tournoi avec succès.")
