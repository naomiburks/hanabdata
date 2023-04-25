"""Processes games."""

from datetime import datetime
from hanabdata.tools.io import read
from hanabdata.tools.io.update import update_chunk, update_user

def get_player_and_seed_info():
    """Gets dict of all players in downloaded games."""
    current = datetime.now()
    player_dict = {}
    seed_dict = {}
    chunk_list = sorted([int(y) for y in read.get_file_names("./data/preprocessed/games")])
    for chunk in chunk_list:
        try:
            data = read.read_chunk(chunk)
        except ValueError:
            update_chunk(chunk)
            data = read.read_chunk(chunk)
        for game in data:
            if game is None or game == "Error":
                continue
            for player in game["players"]:
                # TODO: make helper function
                if player not in player_dict:
                    player_dict[player] = {
                        "num_games": 1,
                        "last_game": game["id"]
                    }
                else:
                    player_dict[player]["num_games"] += 1
                    player_dict[player]["last_game"] = game["id"]
            seed = game["seed"]
            if seed not in seed_dict:
                seed_dict[seed] = {
                    "num_games": 1,
                    "last_game": game["id"]
                }
            else:
                seed_dict[seed]["num_games"] += 1
                seed_dict[seed]["last_game"] = game["id"]
        if (datetime.now() - current).total_seconds() > 20:
            print(f"Finished processing chunk {chunk}.")
            current = datetime.now()
    read._write_json("./data/player_dict.json", player_dict)
    read._write_json("./data/seed_dict.json", seed_dict)

def analyze_player_info():
    """Analyzes existing player info."""
    data = read._read_json("./data/player_dict.json")

    # laughing emoji
    exactly_one, two_to_nine, ten_to_forty_nine, fifty_to_ninety_nine, hundred_to_nine_nine_nine, thousand_plus = 0, 0, 0, 0, 0, 0
    for player in data:
        num_games = data[player]["num_games"]
        if num_games == 1:
            exactly_one += 1
        elif num_games < 10:
            assert num_games > 0
            two_to_nine += 1
        elif num_games < 50:
            ten_to_forty_nine += 1
        elif num_games < 100:
            fifty_to_ninety_nine += 1
        elif num_games < 1000:
            hundred_to_nine_nine_nine += 1
        else:
            assert num_games >= 1000
            thousand_plus += 1
    print(f"There are {exactly_one} players with one game played.")
    print(f"There are {two_to_nine} players with 2 to 9 completed games.")
    print(f"There are {ten_to_forty_nine} players with 10 to 49 completed games.")
    print(f"There are {fifty_to_ninety_nine} players with 50 to 99 completed games.")
    print(f"There are {hundred_to_nine_nine_nine} players with 100 to 999 completed games.")
    print(f"There are {thousand_plus} players with 1000+ completed games.")

def update_players(req_num_games: int):
    """Updates all players with at least req_num_games completed."""
    data = read._read_json("./data/player_dict.json")
    for player in data:
        if data[player]["num_games"] >= req_num_games:
            update_user(player, False)

if __name__ == '__main__':
    # get_player_and_seed_info()
    analyze_player_info()
    update_players(100)
