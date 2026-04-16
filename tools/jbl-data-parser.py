import json
import re

INPUT_FILE = "rosters.txt"

POSITION_MAP = {
    "STARTERS": "Starter",
    "RELIEVERS": "Reliever",
    "CATCHERS": "Catcher",
    "DESIGNATED HITTERS": "Designated Hitter",
    "INFIELDERS": "Infielders",
    "OUTFIELDERS": "Outfielders"
}

def parse_rosters():
    teams = []
    current_division = None
    current_team = None
    current_position_group = None

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:

        # Detect division
        if line in ("EASTERN DIVISION", "WESTERN DIVISION"):
            current_division = line.replace(" DIVISION", "")
            continue

        # Detect team header: "BANFF BISON (BA)"
        team_match = re.match(r"(.+?)\s+\((\w{2})\)", line)
        if team_match:
            team_name, team_code = team_match.groups()
            current_team = {
                "team_name": team_name,
                "team_code": team_code,
                "division": current_division,
                "players": []
            }
            teams.append(current_team)
            continue

        # Detect position group
        if line in POSITION_MAP:
            current_position_group = POSITION_MAP[line]
            continue

        # Otherwise it's a player name
        if current_team and current_position_group:
            # Remove trailing symbols like # or $
            clean_name = re.sub(r"[#$]+$", "", line).strip()

            current_team["players"].append({
                "name": clean_name,
                "position": current_position_group
            })

    return teams


if __name__ == "__main__":
    output = {"teams": parse_rosters()}

    with open("rosters.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("rosters.json created successfully!")
