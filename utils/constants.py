PATH_DATA_PLAYERS_JSON_FILE = "./data/tournaments/players.json"
PATH_DATA_TOURNAMENTS_JSON_FILE = "./data/tournaments/tournaments.json"
PATH_REPORTS_FILES = "./reports/html/"
MESSAGES = {
    "tournament_detail": """
    ===================================================
    Vous n'avez pas de tournoi en cours ou en attente.
    Veuillez créer un nouveau tournoi.
    ===================================================
    """,
    "invalid_choice": """
    ====================================
    Votre choix est invalide.
    Veuillez renouveler votre saisie.
    ====================================
    """,
    "register_players": """
    ================================================
    Le tournoi a déjà démarré.
    Vous ne pouvez plus inscrire de nouveaux joueurs
    ================================================
    """,
    "delete_player": """
    ============================================================
    Vous ne pouvez pas supprimer de joueur:
    - soit parce que le tournoi a déjà démarré,
    - soit parce qu'il n'y a pas de joueurs inscrits au tournoi
    ============================================================
    """,
    "generate_round": """
    =============================================================
    Vous ne pouvez pas générer de tour:
    - soit le nombre de joueurs inscrits est inférieur à 4
    - soit le total de joueurs inscrits est un nombre impair
    - soit la date du tournoi est dans le futur.
    =============================================================
    """,
    "no_generate_round": """
    =============================================================
    Vous ne pouvez pas générer de "nouveau tour.
    Le tour précédent n'est pas terminé.
    Veuillez sélectionner le tour en cours afin de le terminer.
    =============================================================
    """,
    "round_already_ended": """
    ====================================================================
    Le tour que vous avez sélectionné est terminé et les scores ont
    déjà été enregistrés.
    Veuillez sélectionner un tour en cours ou générer un nouveau tour.
    ====================================================================
    """,
    "all_rounds_reached": """
    ==============================================================
    Vous avez atteint le nombre de tours maximum pour ce tournoi.
    Vous ne pouvez plus générer de nouveaux tours.
    ==============================================================
    """,
    "exit_application": """
    ============================
    Vous quittez l'application.
    Au revoir et à bientôt 👋.
    ============================
    """,
    "congratulations": """
    =================================================================
    🎉 🎉  L E  T O U R N O I  E S T  T E R M I N É. 🎉 🎉
    Félicitations au vainqueur 🏆!
    Vous allez être redirigé dans un instant vers le menu principal.
    =================================================================
    """,
    "round_generated": """
    \t========================================================
    \tLe tour a été généré avec succès.
    \tVous allez être redirigé vers le menu de gestion du tour.
    \t========================================================
    """,
    "round_started": """
    ============================================
    Le tour a démarré.
    Les joueurs peuvent commencer leurs matchs.
    ============================================
    """,
    "error_on_save": """
    =================================================
    Une erreur est survenue lors de l'enregistrement.
    Renouvelez votre action.
    =================================================
    """,
    "player_registered": """
    \t======================================
    \tCe joueur est bien inscrit au tournoi.
    \t=======================================
    """,
    "tournament_created": """
    ===============================================
    Le nouveau tournoi a été créé avec succès.
    Vous allez être redirigé vers le menu principal.
    ===============================================
    """,
    "invalid_end_date": """
    =================================================================
    La date de fin doit être égale ou postérieure à la date de début.
    Veuillez entrer une date valide.
    ==================================================================
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
    """,
    "points_updated": """
    =============================================================
    Les points ont été mis à jour.
    Vous allez être redirigé vers le menu de gestion du tournoi.
    =============================================================
    """,
    "player_deleted": """
    =========================================
    Le joueur a bien été supprimé du tournoi.
    =========================================
    """,
    "invalid_national_id": """
    ===================================================
    Le format de l'identitifant national est incorrect.
    Format attendu : 1 lettre + 5 chiffres
    ===================================================
    """
}
