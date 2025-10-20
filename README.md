# Chess Tournament Manager

# Version
1.0.0

## Technical overview
This offline standalone Python application is designed to manage a chess tournament system. 
It is launched from the console and is compatible across Windows, macOS, and Linux operating systems. 
The program handles player and tournament management through JSON file storage, ensuring data persistence between sessions without the need for an online connection.

## Installation
1. Clone the project with the command: `git clone https://github.com/GitDrinou/DAPython_P04_Chess_Tournament`
2. Create a virtual environment by running the following lines in your terminal:
   - check if you have access to `venv`: `python -m venv --help`
   - create the environment: `python -m venv venv`
   - activate the environment:
      - for MacOS / Linux: `source venv/bin/activate`
      - for Windows: `venv\Scripts\activate`
3. Install the required packages: `pip install -r requirements.txt`

## Usage

To manage tournaments, the application display differents menus.\
You have just to follow them as needed.
The initial process of managing a tournament:
1. Create a tournament (name, dates, location,...)
2. Manage a tournament:
   1. register a player (national identifiant, lastname, ...)
   2. unregister a player by his national identifiant
   3. generate a round
      1. start a round
      2. terminate a round and save scores (player points updated)

You will be invited to generate differents reports:
- List of players by alphabetic order
- List of all tournaments
- Detail of a tournament
- List of a tournament players in alphabetic order
- List of a tournament round (and his matchs)

Launch the application with this command line : `python main.py`

## Code style and linting

This project follows the PEP8 coding style and uses flake8 as a linting tool 
to maintain code quality.

To launch and check the flake8 report:
1. open your terminal 
2. copy and paste this command line: `flake8 --format=html 
--htmldir=flake8_rapport`
3. the report is generated and saved on the folder `/flake8_rapport`
4. open your browser and open the file `ìndex.html` from the 
   **/flake8_rapport** folder of the application.

## Data persistence

Tournaments and players datas are saved on the `/data/tournaments` folder.
You will have two separate JSON files:
- `players.json`: list of all players registered in tournaments
- `tournaments.json`: list of all tournaments with (players, rounds and matchs)