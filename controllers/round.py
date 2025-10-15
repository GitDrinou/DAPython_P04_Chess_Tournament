class RoundController:
    """Round controller class"""

    @staticmethod
    def is_finished(rounds):
        """Method that checks if a round is finished or not..
            Args:
                rounds (list): list of rounds
            Returns:
                list_finished_rounds (list): round list finished or not.
        """
        list_finished_rounds = []

        count_match = 0
        for round_detail in rounds:
            for match_detail in round_detail["matchs"]:
                player1_id, player1_score = match_detail["match"][0]
                player2_id, player2_score = match_detail["match"][1]
                player1_score = float(player1_score)
                player2_score = float(player2_score)

                if player1_score == 0.0 and player2_score == 0.0:
                    count_match += 1

            if (count_match == len(round_detail["matchs"])
                    or round_detail["round_end_date"] == ""):
                list_finished_rounds.append({
                    "round_id": round_detail["round_id"],
                    "is_finished": ""
                })
            else:
                list_finished_rounds.append({
                    "round_id": round_detail["round_id"],
                    "is_finished": "X"
                })

        return list_finished_rounds
