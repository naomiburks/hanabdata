"""Downloads games."""

from hanabdata.tools.io.read import get_file_names, read_chunk
from hanabdata.tools.io.update import update_game, update_chunk

def download(game_id: int):
    """Downloads game."""
    update_game(game_id)

def download_all(game_id: int, stop=False):
    """Downloads all games starting from game_id."""
    chunk = game_id // 1000
    while update_chunk(chunk, end_on_error=stop) is None:
        chunk += 1

def download_new():
    """Downloads all games newer than the newest game saved to file."""
    chunks = [int(f) for f in get_file_names("./data/preprocessed/games")]
    last_game_id = 1000 * max(chunks)
    download_all(last_game_id, True)

def get_last_game():
    """Returns last downloaded game in chunk."""
    chunk_path = "./data/preprocessed/games"
    chunk_num = max(int(f) for f in get_file_names(chunk_path))
    chunk_data = read_chunk(chunk_num)
    max_game_id = 0
    for game in chunk_data:
        if isinstance(game, dict):
            max_game_id = max(max_game_id, game["id"])
    return max_game_id

if __name__ == '__main__':
    print(f"Downloading all new games, starting from {get_last_game() + 1}.")
    download_new()
