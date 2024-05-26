"""
This module is used for accessing and manipulating settings.csv.
"""

import tempfile
import os
import csv


temp_path = tempfile.gettempdir()
fields = ['Font Size', 'Target Retention Rate']


def settings_on_device():
    """
    Checks if settings.csv is on device, if not it is added. decks.decks_on_device() must be called first to make
    the MemoryGain dir.
    """
    settings_found = os.path.exists(f'{temp_path}\\..\\MemoryGain\\settings.csv')

    if not settings_found:
        with open(f'{temp_path}\\..\\MemoryGain\\settings.csv', 'w', newline='') as settings_file:
            writer = csv.writer(settings_file)
            writer.writerow(fields)
            writer.writerow(['10', '90'])


def get_target_retention_rate():
    """
    Returns the target retention rate specified in settings.csv as an int.
    """
    with open(f'{temp_path}\\..\\MemoryGain\\settings.csv', 'r') as settings_file:
        dict_reader = csv.DictReader(settings_file, fieldnames=fields)
        next(dict_reader)
        for row in dict_reader:
            return int(row['Target Retention Rate'])


def set_target_retention_rate(target_retention_rate):
    """
    Change the target retention rate in settings.csv.
    """
    font_size = get_font_size()
    with open(f'{temp_path}\\..\\MemoryGain\\settings.csv', 'w', newline='') as settings_file:
        dict_writer = csv.DictWriter(settings_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerow({'Font Size': f'{font_size}', 'Target Retention Rate': f'{target_retention_rate}'})


def set_font_size(font_size):
    """
    Change font size in settings.csv.
    """
    target_retention_rate = get_target_retention_rate()
    with open(f'{temp_path}\\..\\MemoryGain\\settings.csv', 'w', newline='') as settings_file:
        dict_writer = csv.DictWriter(settings_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerow({'Font Size': f'{font_size}', 'Target Retention Rate': f'{target_retention_rate}'})


def get_font_size():
    """
    Returns the font size specified in settings.csv as an int.
    """
    with open(f'{temp_path}\\..\\MemoryGain\\settings.csv', 'r') as settings_file:
        dict_reader = csv.DictReader(settings_file, fieldnames=fields)
        next(dict_reader)
        for row in dict_reader:
            return int(row['Font Size'])











