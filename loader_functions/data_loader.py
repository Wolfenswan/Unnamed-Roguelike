import os
import shelve

def save_game(game):
    save_file = 'savegame.save'  # TODO make dependent on player name
    save_folder = 'savegames'   # TODO move into cfg/constants

    if not os.path.isdir(f'./{save_folder}'):
        os.mkdir(f'./{save_folder}')

    with shelve.open(os.path.join(save_folder, save_file), 'n') as data_file:
        data_file['game'] = game

def load_game():
    save_file = 'savegame.save'
    save_path = 'savegames'
    if not os.path.isfile(os.path.join(f'./{save_path}', save_file)):
        raise FileNotFoundError

    with shelve.open(os.path.join(save_path, save_file), 'r') as data_file:
        game = data_file['game']

    return game