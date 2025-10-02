def tournament_is_finished(tournament):
    """Check if tournament is finished"""

    rounds = tournament["rounds"]
    rounds_ended = True
    for round_detail in rounds:
        if round_detail["round_end_date"] == "":
            rounds_ended = False
            break

    if rounds_ended:
        return print("\n🎉 🎉 Le tournoi est terminé. Félicitations au "
                     "vainqueur 🏆!\n........................................"
                     "................")
    else:
        return None
