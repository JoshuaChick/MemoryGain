"""
This module is for creating and restoring backups.
"""

import tempfile
import os
import datetime


temp_path = tempfile.gettempdir()


def backups_on_device():
    """
    Checks if <...>/MemoryGain/backups directory is on device, if not it is added. decks.decks_on_device()
    must be called first to make the MemoryGain dir.
    """
    backups_found = os.path.exists(f'{temp_path}\\..\\MemoryGain\\backups')
    if not backups_found:
        os.system(f'md {temp_path}\\..\\MemoryGain\\backups')


def create_back_up(name=False):
    """
    Makes a back up of again_dates_1440.txt, cards.csv, correct_dates_1440.txt, decks.txt, settings.csv, and stats.csv.
    Return False is the name already exists, otherwise returns True.
    """
    if name:
        if os.path.exists(f'{temp_path}\\..\\MemoryGain\\backups\\{name}'):
            return False
        os.system(f'md {temp_path}\\..\\MemoryGain\\backups\\{name}')
        os.system(f'copy {temp_path}\\..\\MemoryGain\\* {temp_path}\\..\\MemoryGain\\backups\\{name}')
    else:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        if os.path.exists(f'{temp_path}\\..\\MemoryGain\\backups\\{date}'):
            return False
        os.system(f'md {temp_path}\\..\\MemoryGain\\backups\\{date}')
        os.system(f'copy {temp_path}\\..\\MemoryGain\\* {temp_path}\\..\\MemoryGain\\backups\\{date}')

    return True


def restore_backup(name):
    os.system(f'copy {temp_path}\\..\\MemoryGain\\backups\\{name}\\* {temp_path}\\..\\MemoryGain\\')


def del_backup(name):
    os.system(f'rd /s /q {temp_path}\\..\\MemoryGain\\backups\\{name}')


def get_backup_names():
    """
    Returns a list of the names of backup folders in .../MemoryGain/backups/.
    """
    names = os.listdir(f'{temp_path}\\..\\MemoryGain\\backups')
    names.reverse()
    return names








