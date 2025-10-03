from tabulate import tabulate


class DisplayTableView:
    """Report view class"""

    @staticmethod
    def display_a_round(round_detail):
        """Display a table with a round's details"""
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
            headers = ["Match n°", "Joueur 1", "Joueur 2", "Score1", "Score2"]

            print("--------------------------------------------------------")
            print(f">> {round_name}:")
            print(f"\tDébut: {start_round}")
            print(f"\tFin: {end_round}\n")

            print(tabulate(rows_round, headers=headers, tablefmt="github"))
            print("--------------------------------------------------------")

    @staticmethod
    def display_players(tournament):
        """Display a table with the tournament's players"""
        tournament_name = tournament["name"]
        start_date = tournament["start_date"]
        end_date = tournament["end_date"]
        total_players = len(tournament["players"])
        data_report = sorted(tournament["players"], key=lambda x: (-x[
            "points"], x["last_name"]))

        rows = []
        for entry in data_report:
            national_id = entry["national_id"]
            lastname = entry["last_name"]
            firstname = entry["first_name"]
            birthdate = entry["birth_date"]
            points = entry["points"]
            rows.append([national_id, lastname, firstname, birthdate, points])
        headers = ["Identifiant national", "Nom de famille", "Prénom",
                   "Date de naissance", "Points"]

        print("\n...........................................................")
        print(f">> {tournament_name}:\n")
        print(f"\tDu: {start_date}")
        print(f"\tAu: {end_date}\n")
        print(f"Nombre de joueurs inscrits: {total_players}\n")
        print(tabulate(rows, headers=headers, tablefmt="outline"))

    @staticmethod
    def display_tournaments(tournament):
        """Display a table with the all non-finished tournaments"""
        data_report = sorted(tournament, key=lambda x: x[
            "start_date"])

        rows = []
        for entry in data_report:
            tournament_id = entry["tournament_id"]
            name = entry["name"]
            start_date = entry["start_date"]
            round_number = entry["round_number"]
            total_players = len(entry["players"])
            rows.append([tournament_id, name, start_date, total_players,
                         round_number])
        headers = ["ID Tournoi", "Nom", "Date de début", "Total de joueurs",
                   "N° du tour"]

        print("\nLISTE DES TOURNOIS EN COURS OU A VENIR")
        print(tabulate(rows, headers=headers, tablefmt="outline"))

    def display_rounds(self, rounds, finished_rounds):
        """Display a table with all rounds for a tournaments"""
        data_report = rounds
        rows = []
        for entry in data_report:
            round_id = entry["round_id"]
            round_name = entry["name"]
            start_date = entry["round_start_date"]
            end_date = entry["round_end_date"]
            is_finished = self.round_terminated(round_id, finished_rounds)
            rows.append([round_id, round_name, start_date, end_date,
                         is_finished])

        headers = ["ID Tour", "Nom", "Date de début", "Date de fin",
                   "Scores enregistrés"]
        print("\n...........................................................")
        print(tabulate(rows, headers=headers, tablefmt="github"))
        print("\n...........................................................")

    @staticmethod
    def round_terminated(round_id, finished_rounds):
        """Check if a round terminates"""
        for item in finished_rounds:
            if item["round_id"] == round_id and item["is_finished"]:
                return "Oui"
        return ""
