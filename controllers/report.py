import os
import platform

from jinja2 import Template
from utils.constants import PATH_REPORTS_FILES
from utils.file_utils import write_file


class ReportController:

    os_name = platform.system()
    if os_name == "Windows":
        file_part = "file://"
    else:
        file_part = "file:///"

    def players(self, players, tournament=False, tournament_name=""):
        """Generate the report for all players with alphabetic order (for a
        tournament or not)"""

        if tournament:
            title = "Liste des joueurs du tournoi<br>(par ordre alphabétique)"
            subtitle = tournament_name
            file = PATH_REPORTS_FILES + "tournament_players.html"
            absolute_path_file = self.file_part + os.path.abspath(
                "reports/html/tournament_players.html")
        else:
            title = "Liste des joueurs<br>(par ordre alphabétique)"
            subtitle = ""
            file = PATH_REPORTS_FILES + "players_list.html"
            absolute_path_file = self.file_part + os.path.abspath(
                "reports/html/players_list.html")

        datas_to_display = {
            "title": title,
            "players": players,
            "subtitle": subtitle,
            "css_path": self.file_part + os.path.abspath(
                "reports/report.css"),
            "img_path": self.file_part + os.path.abspath(
                "reports/logo-chess-club.png")
        }
        template_html = """
        <html lang="fr">
            <head>
                <meta charset="utf-8">
                <title>{{ title }} / {{ subtitle }}</title>
                <link rel="stylesheet" href="{{ css_path }}">
            </head>
            <body>
                <div class="container">
                    <img src="{{ img_path }}" alt="Logo Chess Club">
                    <h1>{{ title }}</h1>
                </div>
                <h2>{{ subtitle }}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Identifiant national</th>
                            <th>Nom de famille</th>
                            <th>Prénom</th>
                        </tr>
                    <thead>
                    <tbody>
                        {% for player in players %}
                            <tr>
                                <td>{{ player["national_id"] }}</td>
                                <td>{{ player["last_name"] }}</td>
                                <td>{{ player["first_name"] }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
        </html>
        """

        template = Template(template_html)
        content = template.render(**datas_to_display)

        write_file(file, content)

        return print(f"\nLe rapport a été généré avec succès.\nVous pouvez "
                     f"le retrouver en cliquant sur le lien suivant:\n"
                     f"{absolute_path_file}\n"
                     f"ou en allant dans le dossier REPORTS de l'application.")

    def tournaments(self, tournaments):
        """Generate the report for all tournaments or for a specific
        tournament"""
        if len(tournaments) == 1:
            title = "Détail du tournoi"
            file = PATH_REPORTS_FILES + "tournament_detail.html"
            absolute_path_file = self.file_part + os.path.abspath(
                PATH_REPORTS_FILES + "tournament_detail.html")
        else:
            title = "Liste des tournois"
            file = PATH_REPORTS_FILES + "tournaments_list.html"
            absolute_path_file = self.file_part + os.path.abspath(
                PATH_REPORTS_FILES + "tournaments_list.html")

        datas_to_display = {
            "title": title,
            "tournaments": tournaments,
            "css_path": self.file_part + os.path.abspath(
                "reports/report.css"),
            "img_path": self.file_part + os.path.abspath(
                "reports/logo-chess-club.png")
        }
        template_html = """
            <html lang="fr">
                <head>
                    <meta charset="utf-8">
                    <title>{{ title }}</title>
                    <link rel="stylesheet" href="{{ css_path }}">
                </head>
                <body>
                    <div class="container">
                        <img src="{{ img_path }}" alt="Logo Chess Club">
                        <h1>{{ title }}</h1>
                    </div>
                    {% for tournament in tournaments %}
                        <h2>{{ tournament["name"] }}</h2>
                        <p><b>Identifiant: {{ tournament["tournament_id"] }}
                        </b><br>
                        Lieu: {{ tournament["location"] }}<br>
                        Du {{ tournament["start_date"] }} au {{ tournament[
                        "end_date"] }}<br>
                        Nombre de tour: {{ tournament[
                        "number_of_rounds"] }}<br>
                        Description: {{ tournament["description"] }}</p>
                        <h3>JOUEURS :</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Identifiant national</th>
                                    <th>Nom de famille</th>
                                    <th>Prénom</th>
                                </tr>
                            <thead>
                            <tbody>
                                {% for player in tournament["players"] %}
                                    <tr>
                                        <td>{{ player["national_id"] }}</td>
                                        <td>{{ player["last_name"] }}</td>
                                        <td>{{ player["first_name"] }}</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        <h3>TOURS :</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Tour</th>
                                    <th>Début</th>
                                    <th>Fin</th>
                                    <th>Id Match</th>
                                    <th>Joueur 1</th>
                                    <th>Joueur 2</th>
                                    <th>Score 1</th>
                                    <th>Score 2</th>
                                </tr>
                            <thead>
                            <tbody>
                            {% for round in tournament["rounds"] %}
                                {% for match in round["matchs"] %}
                                    <tr>
                                    {% if loop.first %}
                                        <td rowspan="{{ round[
                                        "matchs"]|length }}" class="round">
                                            {{ round["name"] }}
                                        </td>
                                        <td rowspan="{{ round[
                                        "matchs"]|length }}" class="round">
                                            {{ round["round_start_date"] }}
                                        </td>
                                        <td rowspan="{{ round[
                                        "matchs"]|length }}" class="round">
                                            {{ round["round_end_date"] }}
                                        </td>
                                    {% endif %}
                                        <td>{{ match["match_id"] }}</td>
                                        <td>{{ match["match"][0][0] }}</td>
                                        <td>{{ match["match"][1][0] }}</td>
                                        <td>{{ match["match"][0][1] }}</td>
                                        <td>{{ match["match"][1][1] }}</td>
                                    </tr>
                                {% endfor %}
                            {% endfor %}
                            </tbody>
                        </table>
                        <hr>
                    {% endfor %}
                   </body>
                </html>
                """

        template = Template(template_html)
        content = template.render(**datas_to_display)

        write_file(file, content)

        return print(f"\nLe rapport a été généré avec succès.\nVous pouvez "
                     f"le retrouver en cliquant sur le lien suivant:\n"
                     f"{absolute_path_file}\n"
                     f"ou en allant dans le dossier REPORTS de l'application.")

    def tournament_round(self, tournament):
        """Generate the report for all rounds of a tournament"""
        title = "Détail des tours et matchs du tournoi"
        file = PATH_REPORTS_FILES + "tournament_rounds_detail.html"
        absolute_path_file = self.file_part + os.path.abspath(
            PATH_REPORTS_FILES + "tournament_rounds_detail.html")

        datas_to_display = {
            "title": title,
            "tournament": tournament,
            "css_path": self.file_part + os.path.abspath(
                "reports/report.css"),
            "img_path": self.file_part + os.path.abspath(
                "reports/logo-chess-club.png")
        }
        template_html = """
            <html lang="fr">
                <head>
                    <meta charset="utf-8">
                    <title>{{ title }}</title>
                    <link rel="stylesheet" href="{{ css_path }}">
                </head>
                <body>
                    <div class="container">
                        <img src="{{ img_path }}" alt="Logo Chess Club">
                        <h1>{{ title }}</h1>
                    </div>
                    <h2>{{ tournament["name"] }}</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Tour</th>
                                <th>Début</th>
                                <th>Fin</th>
                                <th>Id Match</th>
                                <th>Joueur 1</th>
                                <th>Joueur 2</th>
                                <th>Score 1</th>
                                <th>Score 2</th>
                            </tr>
                        <thead>
                        <tbody>
                        {% for round in tournament["rounds"] %}
                            {% for match in round["matchs"] %}
                                <tr>
                                {% if loop.first %}
                                    <td rowspan="{{ round[
                                        "matchs"]|length }}" class="round">
                                        {{ round["name"] }}
                                    </td>
                                    <td rowspan="{{ round[
                                        "matchs"]|length }}" class="round">
                                        {{ round["round_start_date"] }}
                                    </td>
                                    <td rowspan="{{ round[
                                        "matchs"]|length }}" class="round">
                                        {{ round["round_end_date"] }}
                                    </td>
                                {% endif %}
                                    <td>{{ match["match_id"] }}</td>
                                    <td>{{ match["match"][0][0] }}</td>
                                    <td>{{ match["match"][1][0] }}</td>
                                    <td>{{ match["match"][0][1] }}</td>
                                    <td>{{ match["match"][1][1] }}</td>
                                </tr>
                            {% endfor %}
                        {% endfor %}
                        </tbody>
                    </table>
                    <hr>
                   </body>
                </html>
                """

        template = Template(template_html)
        content = template.render(**datas_to_display)

        write_file(file, content)

        return print(f"\nLe rapport a été généré avec succès.\nVous pouvez "
                     f"le retrouver en cliquant sur le lien suivant:\n"
                     f"{absolute_path_file}\n"
                     f"ou en allant dans le dossier REPORTS de l'application.")
