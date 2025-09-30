# Chess Tournament Manager

# Version
1.0.0 (beta)

## Technical overview
This offline standalone Python application is designed to manage a chess tournament system. 
It is launched from the console (e.g., `python main.py`) and is compatible across Windows, macOS, and Linux operating systems. 
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
You have just to follow them.

### Application menus

#### Principal menu
1. create a new tournament
2. begin or continue a specific tournament
3. to generate HTML reports

#### Tournament menu
1. register players
2. delete players
3. generate a round
4. pause the tournament

### Extractions folders

