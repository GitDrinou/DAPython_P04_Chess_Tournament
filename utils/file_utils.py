import json

from utils.constants import PATH_DATA_JSON_FILE


def read_file(path_file):
    """Read a file and return a list"""
    with open(path_file, "r") as f:
        data = json.load(f)
        if data:
            return data
        else:
            return None


def write_file(path_file, data):
    """Write data to a file"""
    with open(path_file, "w") as f:
        json.dump(data, f, indent=4)


def save_to_json(key, *args, **kwargs):
    """Save specific data to the json file"""

    data = read_file(PATH_DATA_JSON_FILE)

    if key == "tournaments":
        data["tournaments"].append({
            "tournament_id": kwargs["tournament_id"],
            "name": kwargs["name"].upper(),
            "location": kwargs["location"].capitalize(),
            "start_date": str(kwargs["start_date"]),
            "end_date": str(kwargs["end_date"]),
            "description": kwargs["description"],
            "number_of_rounds": kwargs["number_of_rounds"],
            "round_number": kwargs["round_number"],
            "players": kwargs["random_players"]
        })
    else:
        data["players"].append({
            "national_id": kwargs["national_id"],
            "last_name": kwargs["last_name"].upper(),
            "first_name": kwargs["first_name"].capitalize(),
        })

    write_file(PATH_DATA_JSON_FILE, data)
