import os
import shelve

def save_game(game):
    save_file = 'savegame'
    save_path = 'savegames'
    with shelve.open(os.path.join(save_path, save_file), 'n') as data_file:
        data_file['game'] = game

def load_game():
    save_file = 'savegame'
    save_path = 'savegames'
    if not os.path.isfile(os.path.join(save_path, save_file+'.dat')):
        raise FileNotFoundError

    with shelve.open(os.path.join(save_path, save_file), 'r') as data_file:
        game = data_file['game']

    return game