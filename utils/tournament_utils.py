def tournament_is_finished(tournament):
    """Check if tournament is finished"""
    number_of_pf_rounds = tournament["number_of_rounds"]
    round_number = tournament["round_number"]
    rounds = tournament["rounds"]
    rounds_ended = True
    for round_detail in rounds:
        if round_detail["round_end_date"] == "":
            rounds_ended = False
            break

    if rounds_ended and number_of_pf_rounds == round_number:
        return print("\n🎉 🎉 Le tournoi est terminé. Félicitations au "
                     "vainqueur 🏆!\n........................................"
                     "................")
    else:
        return None
