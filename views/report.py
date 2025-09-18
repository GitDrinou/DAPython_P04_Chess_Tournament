from tabulate import tabulate


class ReportView:
    """Report view class"""

    @staticmethod
    def display_round_details(round_detail):
        """Display a pretty table with the round's details"""
        round_name = round_detail["name"]
        start_round = round_detail["round_start_date"]
        end_round = round_detail["round_end_date"]

        data_report = round_detail["matchs"]
        rows = []
        for entry in data_report:
            match_id = entry["match_id"]
            player1, score1 = entry["match"][0]
            player2, score2 = entry["match"][1]
            rows.append([match_id, player1, player2, score1, score2])
        headers = ["Match ID", "Player1", "Player2", "Score1", "Score2"]

        print("---------------------------------------------------------")
        print(f">>{round_name}:")
        print(f"\tDébut: {start_round}")
        print(f"\tFin: {end_round}\n")

        print(tabulate(rows, headers=headers, tablefmt="github"))
        print("---------------------------------------------------------\n")
