import json
import requests
import time

ROSTERS_FILE = "rosters.json"

SEARCH_URL = "https://statsapi.mlb.com/api/v1/people/search?names={}"

def lookup_player_id(name):
    url = SEARCH_URL.format(name.replace(" ", "%20"))
    response = requests.get(url)

    if response.status_code != 200:
        return "none"

    data = response.json()
    people = data.get("people", [])

    # No matches
    if len(people) == 0:
        return 0

    # Multiple matches
    if len(people) > 1:
        return -1

    # Exactly one match
    return people[0].get("id")


def update_rosters_with_ids():
    with open(ROSTERS_FILE, "r", encoding="utf-8") as f:
        rosters = json.load(f)

    for team in rosters["teams"]:
        for player in team["players"]:
            name = player["name"]

            # Skip if already has ID
            if "mlb_id" in player:
                continue

            mlb_id = lookup_player_id(name)
            player["mlb_id"] = mlb_id

            print(f"{name} → {mlb_id}")

            # Be polite to the API
            time.sleep(0.25)

    # Save updated file
    with open(ROSTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(rosters, f, indent=2)

    print("\nUpdated rosters.json with MLB player IDs!")


if __name__ == "__main__":
    update_rosters_with_ids()
