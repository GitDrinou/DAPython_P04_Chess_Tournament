PATH_DATA = "./data/tournaments/"
PATH_DATA_PLAYERS_JSON_FILE = "./data/tournaments/players.json"
PATH_DATA_TOURNAMENTS_JSON_FILE = "./data/tournaments/tournaments.json"
PATH_REPORTS_FILES = "./reports/html/"
DEFAULT_SCORE = 0.0
DEFAULT_BYE = "BYE"
DEFAULT_DELAY = 3
TAG_FINISHED = "X"
DEFAULT_NUMBER_OF_ROUNDS = 4
ALLOW_BYES = True
WIN_VALUE = "1"
LOSE_VALUE = "0"
POINT_WIN_VALUE = 1
POINT_LOSE_VALUE = 0
POINT_EQUALITY_VALUE = 0.5
ERROR_ROUND_ENDED = "round_already_ended"
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
    "have_win_point": "a un point automatique (BYE).",
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
    "invalide_number_of_players": "\nVous ne pouvez pas générer de tour.\nLe "
                                  "nombre minimum de joueurs doit être de ",
    "label_start_round": "\tDébut du tour: ",
    "label_start_tournament": "\tDu: ",
    "label_end_round": "\tFin du tour: ",
    "label_end_tournament": "\tAu: ",
    "label_total_players": "Nombre de joueurs inscrits: ",
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
    Il faut au moins 2 joueurs pour créer un tournoi.
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
    "number_of_players_is_odd": "Le nombre de joueur est impair:",
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
    "report_generated": """
    Le rapport a été généré avec succès.
    Vous pouvez le retrouver :
    - en allant dans le dossier "/reports" de l'application
    - ou en cliquant sur le lien ci-dessous:\n
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
    "scores_instructions": """
    Instructions:
    \t- [1] pour le vainqueur du match
    \t- [0] pour le perdant du match
    \t- En cas de match nul, saisissez [1] pour les 2 scores
    """,
    "value_not_exist": "La valeur n'existe pas.",
    "will_be_bye": " sera BYE pour ce tour."
}
TITLES = {
    "title_application": "G E S T I O N N A I R E   D E   T O U R N O I S   "
                         "D ' É C H E C S",
    "title_main_menu": "MENU PRINCIPAL",
    "title_tournament_menu": "MENU DE GESTION D'UN TOURNOI",
    "title_tournament_list": "\n** LISTE DES TOURNOIS EN COURS OU A VENIR **",
    "title_match_score": "\nINSCRIRE LES SCORES DU MATCH N°",
    "title_player_registration": "INSCRIPTION D'UN JOUEUR",
    "title_tournament_creation": "CRÉATION D'UN NOUVEAU TOURNOI",
    "title_tournament_selection": "SÉLECTION D'UN TOURNOI",
    "title_round_selection": "SÉLECTIONNER UN TOUR",
    "title_player_deletion": "DÉSINSCRIRE UN JOUEUR",
    "title_round_menu": "MENU DE GESTION D'UN TOUR",
    "tile_reports_menu": "MENU DE GÉNÉRATION DES RAPPORTS"
}
INSTRUCTIONS = {
    "national_id_input": "Saisissez l'identifiant national du joueur",
    "last_name_input": "Saisissez le nom de famille du joueur",
    "first_name_input": "Saisissez le prénom du joueur",
    "tournament_start_input": "Saisissez la date de début du tournoi (format "
    "attendu: JJ/MM/AAAA)",
    "tournament_end_input": "Saisissez la date de fin du tournoi (format "
    "attendu: JJ/MM/AAAA)",
    "tournament_name_input": "Saisissez le nom du tournoi",
    "tournament_localisation_input": "Saisissez la localisation du tournoi",
    "tournament_description_input": "Saisissez une description du tournoi",
    "tournament_number_round_input": "Saisissez le nombre de tours (par "
                                     "défaut 4)",
    "tournament_id_input": "Saisissez l'identifiant du tournoi parmi la "
                           "liste ci-dessus\nou pour revenir au menu "
                           "précédent, tapez sur la touche 'R' de votre "
                           "clavier",
    "round_id_input": "Les différentes possibilités:\n- saisir l'identifiant "
                      "du tour en cours\n- taper sur la touche ENTREE de "
                      "votre clavier pour générer un nouveau tour\n- taper "
                      "sur la tour 'R' de votre clavier pour revenir au menu "
                      "précédent.\nChoisissez une option: ",
    "save_score1_input": "Saisissez le score du joueur 1 | Score 1",
    "save_score2_input": "Saisissez le score du joueur 2 | Score 2",
}
SELECTIONS = {
    "create_tournament": "Créer un nouveau tournoi",
    "start_or_continue_tournament": "Démarrer ou reprendre la gestion d'un "
                                    "tournoi",
    "generate_reports": "Générer des rapports",
    "leave_application": "Quitter l'application",
    "register_player": "Inscrire un joueur au tournoi",
    "unregister_player": "Désinscrire un joueur du tournoi",
    "generate_round": "Générer ou continuer un tour (tour ",
    "pause_tournament": "Mettre en pause le tournoi",
    "back_to_main_menu": "Revenir au menu principal",
    "start_round": "Démarrer le tour",
    "end_round": "Terminer le tour et saisir les scores des matchs",
    "back_to_tournament_menu": "Revenir au menu de gestion du tournoi",
    "players_list_report": "Liste des joueurs par ordre alphabétique",
    "tournaments_list_report": "Liste de tous les tournois",
    "tournament_detail_report": "Nom et dates d'un tournoi",
    "tournament_players_report": "Liste des joueurs d'un tournoi par ordre "
                                 "alphabétique",
    "tournament_rounds_report": "Liste de tous les tours du tournoi et de "
                                "tous les matchs du tour",
}
