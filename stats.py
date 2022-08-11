"""
This module is for accessing and manipulating correct_dates_1440.txt, and again_dates_1440.txt.
The 1440 is to indicate that they are only for recording results for cards that had an interval of 1440 or more.
"""

import tempfile
import os
import csv
import datetime


temp_path = tempfile.gettempdir()


def stats_on_device():
    """
    Checks if files related to statistics are on the device, if not they are added. decks.decks_on_device() must be called first to make
    the MemoryGain dir.
    """
    correct_dates_found = os.path.exists(f'{temp_path}\\..\\MemoryGain\\correct_dates_1440.txt')
    again_dates_found = os.path.exists(f'{temp_path}\\..\\MemoryGain\\again_dates_1440.txt')

    if not correct_dates_found:
        with open(f'{temp_path}\\..\\MemoryGain\\correct_dates_1440.txt', 'w') as correct_dates_1440_file:
            correct_dates_1440_file.write('')

    if not again_dates_found:
        with open(f'{temp_path}\\..\\MemoryGain\\again_dates_1440.txt', 'w') as again_dates_1440_file:
            again_dates_1440_file.write('')


def add_to_correct_1440():
    """
    Adds a record to correct_dates_1440.txt.
    """
    with open(f'{temp_path}\\..\\MemoryGain\\correct_dates_1440.txt', 'a') as correct_dates_1440:
        correct_dates_1440.write(datetime.datetime.now().strftime('%Y-%m-%d') + '\n')


def add_to_again_1440():
    """
    Increments the 'Number Incorrect 1440 Minutes and Over' stat by 1.
    """
    with open(f'{temp_path}\\..\\MemoryGain\\again_dates_1440.txt', 'a') as correct_dates_1440:
        correct_dates_1440.write(datetime.datetime.now().strftime('%Y-%m-%d') + '\n')


def get_retention_1440(days=False):
    """
    Uses the records in correct_dates_1440.txt and again_dates_1440.txt to get the retention rate =
    (correct / total * 100)%. The days parameter is used to specify how many days in the past from which to get the
    results from, e.g. if days was 30 it would get the retention rate for the last 30 days. Returns
    correct / total * 100 or False if the total cards is 0.
    """
    if type(days) == bool:
        with open(f'{temp_path}\\..\\MemoryGain\\correct_dates_1440.txt', 'r') as correct_dates_1440:
            correct_dates_1440_lines = correct_dates_1440.readlines()
            correct = len(correct_dates_1440_lines)

        with open(f'{temp_path}\\..\\MemoryGain\\again_dates_1440.txt', 'r') as again_dates_1440:
            again_dates_1440_lines = again_dates_1440.readlines()
            total = correct + len(again_dates_1440_lines)
    else:
        cut_off_date = str((datetime.datetime.now() - datetime.timedelta(days)).strftime('%Y-%m-%d'))

        with open(f'{temp_path}\\..\\MemoryGain\\correct_dates_1440.txt', 'r') as correct_dates_1440:
            correct_dates_1440_lines = correct_dates_1440.readlines()
            correct_dates_after_cut_off = []

            for line in correct_dates_1440_lines:
                line = line.replace('\n', '')

                if line > cut_off_date:
                    correct_dates_after_cut_off.append(line)

            correct = len(correct_dates_after_cut_off)

        with open(f'{temp_path}\\..\\MemoryGain\\again_dates_1440.txt', 'r') as again_dates_1440:
            again_dates_1440_lines = again_dates_1440.readlines()
            again_dates_after_cut_off = []

            for line in again_dates_1440_lines:
                line = line.replace('\n', '')

                if line > cut_off_date:
                    again_dates_after_cut_off.append(line)

            total = correct + len(again_dates_after_cut_off)

    if total == 0:
        return False

    return float(correct / total * 100)







