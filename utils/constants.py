PATH_DATA_PLAYERS_JSON_FILE = "./data/tournaments/players.json"
PATH_DATA_TOURNAMENTS_JSON_FILE = "./data/tournaments/tournaments.json"
PATH_REPORTS_FILES = "./reports/html/"

MESSAGES = {
    "tournament_detail": """
    \t===================================================
    \tVous n'avez pas de tournoi en cours ou en attente.
    \tVeuillez créer un nouveau tournoi.
    \t===================================================
    """,
    "invalid_choice": """
    \t====================================
    \tVotre choix est invalide.
    \tVeuillez renouveler votre sélection.
    \t====================================
    """,
    "register_players": """
    \t================================================
    \tLe tournoi a déjà démarré.
    \tVous ne pouvez plus inscrire de nouveaux joueurs
    \t================================================
    """,
    "delete_player": """
    \t============================================================
    \tVous ne pouvez pas supprimer de joueur:
    \t- soit parce que le tournoi a déjà démarré,
    \t- soit parce qu'il n'y a pas de joueurs inscrits au tournoi
    \t============================================================
    """,
    "generate_round": """
    \t=============================================================
    \tVous ne pouvez pas générer de tour:
    \t- soit le nombre de joueurs inscrits est inférieur à 4
    \t- soit le total de joueurs inscrits est un nombre impair
    \t- soit la date du tournoi est dans le futur.
    \t=============================================================
    """,
    "no_generate_round": """
    \t=============================================================
    \tVous ne pouvez pas générer de "nouveau tour.
    \tLe tour précédent n'est pas terminé.
    \tVeuillez sélectionner le tour en cours afin de le terminer.
    \t=============================================================
    """,
    "round_already_ended": """
    \t====================================================================
    \tLe tour que vous avez sélectionné est terminé et les scores ont
    \tdéjà été enregistrés.
    \tVeuillez sélectionner un tour en cours ou générer un nouveau tour.
    \t====================================================================
    """,
    "all_rounds_reached": """
    \t==============================================================
    \tVous avez atteint le nombre de tours maximum pour ce tournoi.
    \tVous ne pouvez plus générer de nouveaux tours.
    \t==============================================================
    """,
    "exit_application": """
    \t============================
    \tVous quittez l'application.
    \tAu revoir et à bientôt 👋.
    \t============================
    """,
    "congratulations": """
    \t=================================================================
    \t🎉 🎉  L E  T O U R N O I  E S T  T E R M I N É. 🎉 🎉
    \tFélicitations au vainqueur 🏆!
    \tVous allez être redirigé dans un instant vers le menu principal.
    \t=================================================================
    """,
    "round_generated": """
    \t========================================================
    \tLe tour a été généré avec succès.
    \tVous allez être redirigé vers le menu de gestion du tour.
    \t========================================================
    """,
    "round_started": """
    \t============================================
    \tLe tour a démarré.
    \tLes joueurs peuvent commencer leurs matchs.
    \t============================================
    """,
    "error_on_save": """
    \t=================================================
    \tUne erreur est survenue lors de l'enregistrement.
    \tRenouvelez votre action.
    \t=================================================
    """,
    "player_registered": """
    \t======================================
    \tCe joueur est bien inscrit au tournoi.
    \t=======================================
    """,
    "tournament_created": """
    \t===============================================
    \tLe nouveau tournoi a été créé avec succès.
    \tVous allez être redirigé vers le menu principal.
    \t===============================================
    """,
    "invalid_end_date": """
    \t=================================================================
    \tLa date de fin doit être égale ou postérieure à la date de début.
    \tVeuillez entrer une date valide.
    \t==================================================================
    """,
    "round_not_started": """
    \t=============================================================
    \tLe tour n'a pas encore démarré.
    \tVous ne pouvez pas terminer ce tour avant de l'avoir démarré.
    \t=============================================================
    """,
    "round_ended": """
    \t=============================================================
    \tLe tour est terminé.
    \tVous allez à présent être invité à enregistrer les scores
    \tpour chaque matchs du tour.
    \t=============================================================
    """,
    "points_updated": """
    \t=============================================================
    \tLes points ont été mis à jour.
    \tVous allez être redirigé vers le menu de gestion du tournoi.
    \t=============================================================
    """,
    "player_deleted": """
    \t=========================================
    \tLe joueur a bien été supprimé du tournoi.
    \t=========================================
    """
}
