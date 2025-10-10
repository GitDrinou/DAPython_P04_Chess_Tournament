from utils.console_utils import ConsoleDisplayer
from core.constants import PATH_DATA_TOURNAMENTS_JSON_FILE, MESSAGES
from utils.file_utils import save_to_json, update_tournament, read_json_file
from utils.player_utils import check_player_is_exist


class PlayerController:

    @staticmethod
    def add(player, tournament_id):
        """Add a player to the tournament"""

        data_tournaments = read_json_file(PATH_DATA_TOURNAMENTS_JSON_FILE)
        tournaments = data_tournaments["tournaments"]
        tournament = next(
            (t for t in tournaments if t["tournament_id"] == tournament_id),
            None
        )

        if tournament:
            tournament["players"].append({
                "national_id": player.national_id,
                "last_name": player.last_name.upper(),
                "first_name": player.first_name.capitalize(),
                "birth_date": player.birth_date,
                "points": 0.0
            })

            update_tournament(
                PATH_DATA_TOURNAMENTS_JSON_FILE,
                tournament["tournament_id"],
                tournament
            )

            if not check_player_is_exist(player.national_id):
                save_to_json("players",
                             national_id=player.national_id,
                             last_name=player.last_name.upper(),
                             first_name=player.first_name.capitalize(),
                             birth_date=player.birth_date)

            ConsoleDisplayer.log(MESSAGES["player_registered"], level="INFO")
