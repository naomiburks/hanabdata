"""Prompts user for seed and updates."""

from hanabdata.tools.io.update import update_seed

if __name__ == '__main__':
    seed = input('enter seed to update: ')
    update_seed(seed)
