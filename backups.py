"""
This module is for creating and restoring backups.
"""

import tempfile
import os
import datetime


temp_path = tempfile.gettempdir()


def delete_old_backups():
    """
    Deletes non-user made backups that are over 7 days old.
    """
    names = get_backup_names()
    for name in names:
        # YY-mm-dd is the format of how non-user made backups are saved, and get_backup_names() will return
        # YY-mm-dd <auto> for backups made automatically (can tell they are non-user backups due to automatic file in
        # dir).
        if '<auto>' in name:
            date = name.split('<')[0].strip()
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
            seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
            seven_days_ago = seven_days_ago.strftime('%Y-%m-%d')
            if date_obj < seven_days_ago:
                os.system(f'rd /s /q {temp_path}\\..\\MemoryGain\\backups\\{date}')


def backups_on_device():
    """
    Checks if <...>/MemoryGain/backups/manual and <...>/MemoryGain/backups/manual are on device, if not they are added.
    decks.decks_on_device() must be called first to make the MemoryGain dir.
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
    # For auto-creation of backups:
    else:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        # Checks for automatic file (as manual backups of same name will not have this file).
        if os.path.exists(f'{temp_path}\\..\\MemoryGain\\backups\\{date}\\automatic'):
            return False
        os.system(f'md {temp_path}\\..\\MemoryGain\\backups\\{date}')
        os.system(f'copy {temp_path}\\..\\MemoryGain\\* {temp_path}\\..\\MemoryGain\\backups\\{date}')
        os.system(f'n>{temp_path}\\..\\MemoryGain\\backups\\{date}\\automatic')

    return True


def restore_backup(name):
    # Handles restoring a backup that was made automatically.
    if '<auto>' in name:
        os.system(f'copy {temp_path}\\..\\MemoryGain\\backups\\{name.split("<")[0].strip()}\\* {temp_path}\\..\\MemoryGain\\')
        os.system(f'del {temp_path}\\..\\MemoryGain\\automatic')
    else:
        os.system(f'copy {temp_path}\\..\\MemoryGain\\backups\\{name}\\* {temp_path}\\..\\MemoryGain\\')


def del_backup(name):
    if '<auto>' in name:
        os.system(f'rd /s /q {temp_path}\\..\\MemoryGain\\backups\\{name.split("<")[0].strip()}')
    else:
        os.system(f'rd /s /q {temp_path}\\..\\MemoryGain\\backups\\{name}')


def get_backup_names():
    """
    Returns a list of the names of backup folders in .../MemoryGain/backups/.
    """
    names = os.listdir(f'{temp_path}\\..\\MemoryGain\\backups')
    names.reverse()
    # If a backup was made automatically, <auto> is appended to the name (as '<' and '>' are not allowed to be used in
    # folder names the user cannot manually make folders that have <auto>).
    for i in range(len(names)):
        if os.path.exists(f'{temp_path}\\..\\MemoryGain\\backups\\{names[i]}\\automatic'):
            names[i] = names[i] + ' <auto>'

    return names








