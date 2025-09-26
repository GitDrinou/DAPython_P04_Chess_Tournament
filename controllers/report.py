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
                                padding: 10px 20px;
                            }
                            th {background-color: rgb(235, 235, 235);}
                            td {text-align: center;}
                            p {font-weight: bold;}
                        </style>
                    </head>
                   <body>
                      <h1>{{ title }}</h1>
                      <table>
                        <thead>
                            <tr>
                                <th>Id</th>
                                <th>Nom</th>
                                <th>Date de début</th>
                                <th>Date de fin</th>
                                <th>Nombre de tours</th>
                                <th>Description</th>
                                <th>Joueurs</th>
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
