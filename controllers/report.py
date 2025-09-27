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

    def players(self, players):
        """Generate the report for all players with alphabetic order"""
        datas_to_display = {
            "title": "Liste des joueurs (par ordre alphabétique)",
            "players": players,
            "total": len(players),
        }
        template_html = """
        <html lang="fr">
            <head>
                <meta charset="utf-8">
                <title>{{ title }}</title>
                <style>
                    body {
                        font-family: Tahoma, sans-serif;
                        font-size: 1rem;
                        padding: 24px;
                    }
                    table {
                        border-collapse: collapse;
                        border: 2px solid rgb(200, 200, 200);
                        letter-spacing: 1px;
                    }
                    td,th {
                        border: 1px solid rgb(190, 190, 190);
                        padding: 10px 20px;
                    }
                    th {background-color: rgb(235, 235, 235);}
                    td {text-align: center;}
                    p {font-weight: bold;}
                </style>
            </head>
           <body>
              <h1>{{ title }}</h1>
              <p>Total de joueurs {{ total }}</p>
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
        file = PATH_REPORTS_FILES + "players_list.html"

        write_file(file, content)

        absolute_path_file = self.file_part + os.path.abspath(
            "reports/players_list.html")

        return print(f"\nLe rapport a été généré avec succès.\nVous pouvez "
                     f"le retrouver en cliquant sur le lien suivant:\n"
                     f"{absolute_path_file}\n"
                     f"ou en allant dans le dossier REPORTS de l'application.")

    def tournaments(self, tournaments):
        """Generate the report for all tournaments"""
        datas_to_display = {
            "title": "Liste des tournois",
            "tournaments": tournaments,
        }
        template_html = """
            <html lang="fr">
                <head>
                    <meta charset="utf-8">
                    <title>{{ title }}</title>
                    <style>
                        body {
                            font-family: Tahoma, sans-serif;
                            font-size: 1rem;
                            padding: 24px;
                        }
                        table {
                            border-collapse: collapse;
                            border: 2px solid rgb(200, 200, 200);
                            letter-spacing: 1px;
                        }
                        td,th {
                            border: 1px solid rgb(190, 190, 190);
                            padding: 5px 16px;
                        }
                        th {background-color: rgb(215, 215, 215);}
                        td {text-align: center;}
                        hr {
                            margin-top: 24px;
                            border: none;
                            border-top: 3px dotted black;
                        }
                        .round {background-color: rgb(235, 235, 235);}
                    </style>
                </head>
                <body>
                    <h1>{{ title }}</h1>
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
                                        <td rowspan="2" class="round">
                                            {{ round["name"] }}
                                        </td>
                                        <td rowspan="2" class="round">
                                            {{ round["round_start_date"] }}
                                        </td>
                                        <td rowspan="2" class="round">
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
        file = PATH_REPORTS_FILES + "tournaments_list.html"

        write_file(file, content)

        absolute_path_file = self.file_part + os.path.abspath(
            "reports/tournaments_list.html")

        return print(f"\nLe rapport a été généré avec succès.\nVous pouvez "
                     f"le retrouver en cliquant sur le lien suivant:\n"
                     f"{absolute_path_file}\n"
                     f"ou en allant dans le dossier REPORTS de l'application.")
