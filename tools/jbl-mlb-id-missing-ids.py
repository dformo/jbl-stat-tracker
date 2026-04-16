import json

ROSTERS_FILE = "rosters.json"

def find_missing_ids():
    with open(ROSTERS_FILE, "r", encoding="utf-8") as f:
        rosters = json.load(f)

    missing = []

    for team in rosters["teams"]:
        team_name = team["team_name"]
        team_code = team["team_code"]

        for player in team["players"]:
            mlb_id = player.get("mlb_id")

            # Conditions for "bad" IDs
            if (
                mlb_id is None or
                mlb_id == "none" or
                mlb_id == "multi" or
                (isinstance(mlb_id, int) and mlb_id <= 0)
            ):
                missing.append({
                    "team": f"{team_name} ({team_code})",
                    "name": player["name"],
                    "mlb_id": mlb_id
                })

    return missing


if __name__ == "__main__":
    missing_players = find_missing_ids()

    print("\nPlayers with missing or invalid MLB IDs:\n")
    for p in missing_players:
        print(f"{p['team']}: {p['name']} → {p['mlb_id']}")

    print(f"\nTotal missing/invalid IDs: {len(missing_players)}")
