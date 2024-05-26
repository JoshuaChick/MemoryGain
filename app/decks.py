"""
This module is for managing decks. It contains functions for manipulating decks.txt.
"""

import tempfile
import re
import os
import cards


temp_path = tempfile.gettempdir()


def decks_on_device():
    """
    Checks if decks.txt is on the device, if not it is added.
    """
    memorygaindir_found = os.path.exists(f'{temp_path}\\..\\MemoryGain')
    decks_found = os.path.exists(f'{temp_path}\\..\\MemoryGain\\decks.txt')

    if not memorygaindir_found:
        os.system(f'md {temp_path}\\..\\MemoryGain')

    if not decks_found:
        with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'w') as decks_file:
            decks_file.write('')


def check_deck_exists(deck):
    """
    Checks if a deck exists. If it does True is returned, if not, False is returned.
    """
    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'r') as decks_file:
        deck_lines = decks_file.readlines()
        if (deck + '\n') in deck_lines:
            return True

    return False


def get_deck_lines():
    """
    Returns a list with all the lines in decks.txt (each line corresponds to a deck).
    """
    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'r') as decks_text:
        lines = decks_text.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n', '')
        return lines


def del_deck(deck):
    """
    Deletes a deck from decks.txt and the cards belonging to that deck in cards.txt.
    """
    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'r') as decks_file:
        deck_lines = decks_file.readlines()
        index = deck_lines.index(deck + '\n')
        deck_lines.pop(index)

    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'w') as decks_file:
        decks_file.writelines(deck_lines)

    cards.del_deck_cards(deck)


def add_deck(deck):
    """
    Inserts a deck into decks.txt, in alphabetical order. Return False is the deck already exists. Otherwise returns True.
    """
    if check_deck_exists(deck):
        return False

    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'a') as decks_file:
        decks_file.write(deck + '\n')

    # Re-writes the decks in alphabetical order so the deck buttons will also be in order and have their index.
    # match to the corresponding line in decks.txt.
    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'r') as decks_file:
        deck_lines = decks_file.readlines()
        deck_lines.sort(key=str.lower)

    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'w') as decks_file:
        decks_file.writelines(deck_lines)

    return True


def rename_deck(old_name, new_name):
    """
    Renames a deck and all cards that belong to it. Returns True if successful. Returns False is name already exists.
    """
    if check_deck_exists(new_name):
        return False

    deck_lines = get_deck_lines()
    for i in range(len(deck_lines)):
        if deck_lines[i] == old_name:
            deck_lines[i] = new_name + '\n'
            continue
        deck_lines[i] = deck_lines[i] + '\n'

    deck_lines.sort()

    with open(f'{temp_path}\\..\\MemoryGain\\decks.txt', 'w') as decks_file:
        decks_file.writelines(deck_lines)

    cards.change_deck(old_name, new_name)

    return True
