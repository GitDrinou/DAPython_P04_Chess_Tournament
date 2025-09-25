from tabulate import tabulate


class ReportView:
    """Report view class"""

    @staticmethod
    def display_round_details(round_detail):
        """Display a pretty table with the round's details"""
        if round_detail:
            round_name = round_detail["name"]
            start_round = round_detail["round_start_date"]
            end_round = round_detail["round_end_date"]

            data_report = round_detail["matchs"]
            rows_round = []
            for entry in data_report:
                match_id = entry["match_id"]
                player1, score1 = entry["match"][0]
                player2, score2 = entry["match"][1]
                rows_round.append([match_id, player1, player2, score1, score2])
            headers = ["Match ID", "Player1", "Player2", "Score1", "Score2"]

            print("--------------------------------------------------------")
            print(f">>{round_name}:")
            print(f"\tDébut: {start_round}")
            print(f"\tFin: {end_round}\n")

            print(tabulate(rows_round, headers=headers, tablefmt="github"))
            print("--------------------------------------------------------\n")

    @staticmethod
    def display_tournament_players(tournament):
        """Display a pretty table with the tournament's players"""
        tournament_name = tournament["name"]
        data_report = tournament["players"]

        rows = []
        for entry in data_report:
            national_id = entry["national_id"]
            lastname = entry["last_name"]
            firstname = entry["first_name"]
            rows.append([national_id, lastname, firstname])
        headers = ["Identifiant national", "Nom de famille", "Prénom"]

        print("\n...........................................................")
        print(f">> {tournament_name}:\n")
        print(tabulate(rows, headers=headers, tablefmt="github"))
        print("...........................................................")
