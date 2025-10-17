PATH_DATA = "./data/tournaments/"
PATH_DATA_PLAYERS_JSON_FILE = "./data/tournaments/players.json"
PATH_DATA_TOURNAMENTS_JSON_FILE = "./data/tournaments/tournaments.json"
PATH_REPORTS_FILES = "./reports/html/"
MESSAGES = {
    "all_rounds_reached": """
    ==============================================================
    Vous avez atteint le nombre maximum de tours pour ce tournoi.
    Vous ne pouvez plus générer de nouveaux tours.
    ==============================================================
    """,
    "congratulations": """
    =================================================================
    🎉 🎉  L E  T O U R N O I  E S T  T E R M I N É. 🎉 🎉
    Félicitations au vainqueur 🏆!
    Vous allez être redirigé dans un instant vers le menu principal.
    =================================================================
    """,
    "exit_application": """
    ============================
    Vous quittez l'application.
    Au revoir et à bientôt 👋.
    ============================
    """,
    "failure_registration": "Échec lors de l'inscription",
    "failure_deletion": "Échec lors de la suppression",
    "failure_selected_tournament": "Sélection de tournoi invalide. Veuillez "
                                   "réessayer.",
    "failure_end_of_round": "Échec lors de la finalisation du tour",
    "failure_invalid_score": "Score invalide",
    "failure_saved_score": "Échec lors de l'enregistrement du score",
    "failure_saved_round": "Erreur inattendue lors de l'enregistrement du "
                           "tour",
    "failure_no_players_found": "Aucun joueur trouvé. Impossible de générer "
                                "le rapport.",
    "failure_no_tournaments_found": "Aucun tournoi trouvé. Impossible de "
                                    "générer le rapport",
    "failure_started_round": "Échec lors du démarrage du tour",
    "failure": "Erreur inattendue",
    "invalid_choice": """
    ====================================
    Votre choix est invalide.
    Veuillez réessayer.
    ====================================
    """,
    "invalid_end_date": """
    =================================================================
    La date de fin doit être égale ou postérieure à la date de début.
    Veuillez entrer une date de fin valide.
    ==================================================================
    """,
    "invalid_national_id": """
    ====================================================
    Le format de l'identitifant national est incorrect.
    Format attendu : 1 lettre + 5 chiffres (ex. A12345)
    ====================================================
    """,
    "no_deletion_possible": """
    ============================================================
    Vous ne pouvez pas supprimer de joueur:
    - soit parce que le tournoi a déjà démarré
    - soit parce qu'il n'y a pas de joueurs inscrits au tournoi
    ============================================================
    """,
    "no_generate_due_to_date": """
    =============================================================
    Vous ne pouvez pas générer de tour car la date du tournoi est
    supérieur à la date du jour.
    =============================================================
    """,
    "no_generate_due_to_players": """
    =============================================================
    Vous ne pouvez pas générer de tour:
    - soit le nombre de joueurs inscrits est inférieur à 4
    - soit le total de joueurs inscrits est un nombre impair
    =============================================================
    """,
    "no_generate_round": """
    =============================================================
    Vous ne pouvez pas générer de nouveau tour.
    Le tour précédent n'est pas terminé.
    Veuillez sélectionner le tour en cours afin de le terminer.
    =============================================================
    """,
    "no_possible_pairing": """
    ======================================================================
    Impossible de former des pairs sans doublon avec les joueurs restants.
    =======================================================================
    """,
    "no_registration_players": """
    ================================================
    Le tournoi a déjà démarré.
    Vous ne pouvez plus inscrire de nouveaux joueurs
    ================================================
    """,
    "player_unregistered": """
    ===========================================
    Le joueur a bien été désinscrit du tournoi.
    ===========================================
    """,
    "players_already_played_together": """
    =========================================
    Tous les joueurs ont déjà joué ensemble !
    =========================================
    """,
    "player_registered": """
    ======================================
    Le joueur est bien inscrit au tournoi.
    =======================================
    """,
    "points_updated": """
    =============================================================
    Les points ont été mis à jour.
    Vous allez être redirigé vers le menu de gestion du tournoi.
    =============================================================
    """,
    "round_already_ended": """
    ================================================================
    Le tour que vous avez sélectionné est terminé et les scores ont
    déjà été enregistrés.
    ================================================================
    """,
    "round_generated": """
    ========================================================
    Le tour a été généré avec succès.
    Vous allez être redirigé vers le menu de gestion du tour.
    ========================================================
    """,
    "round_started": """
    ============================================
    Le tour a démarré.
    Les joueurs peuvent commencer leurs matchs.
    ============================================
    """,
    "tournament_created": """
    ===============================================
    Le nouveau tournoi a été créé avec succès.
    Vous allez être redirigé vers le menu principal.
    ===============================================
    """,
    "no_tournament_ongoing": """
    ===================================================
    Vous n'avez pas de tournoi en cours ou en attente.
    Veuillez créer un nouveau tournoi.
    ===================================================
    """,
    "round_not_started": """
    =============================================================
    Le tour n'a pas encore démarré.
    Vous ne pouvez pas terminer ce tour avant de l'avoir démarré.
    =============================================================
    """,
    "round_ended": """
    =============================================================
    Le tour est terminé.
    Vous allez à présent être invité à enregistrer les scores
    pour chaque matchs du tour.
    =============================================================
    """
}
