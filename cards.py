"""
This module is for managing cards. It contains functions for manipulating cards.csv.
"""

import tempfile
import re
import datetime
import os
import csv
import stats
import settings
import stats
import linear_regression


temp_path = tempfile.gettempdir()
# Fields for cards.csv.
fields = ['Deck', 'Question', 'Answer', 'Ease', 'Due', 'Interval', 'Phase']


def cards_on_device():
    """
    Checks if cards.csv is on device, if not it is added. decks.decks_on_device() must be called first to make
    the MemoryGain dir.
    """
    # Due to the way cards were stored in the test version of MemoryGain, it reformats old cards to the new format.
    old_cards = []

    if os.path.exists(f'{temp_path}\\..\\MemoryGain\\cards.txt'):
        with open(f'{temp_path}\\..\\MemoryGain\\cards.txt') as old_cards_file:
            old_cards = old_cards_file.read().split('DECK^^$=')
            old_cards.pop(0)

        os.system(f'del {temp_path}\\..\\MemoryGain\\cards.txt')

    cards_found = os.path.exists(f'{temp_path}\\..\\MemoryGain\\cards.csv')

    if not cards_found:
        with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'w', newline='') as cards_file:
            writer = csv.writer(cards_file)
            writer.writerow(fields)

    for old_card in old_cards:
        deck = old_card.split('QUESTION^^$=')[0]
        question = old_card.split('QUESTION^^$=')[1].split('ANSWER^^$=')[0]
        answer = old_card.split('ANSWER^^$=')[1].split('EASE^^$=')[0]
        add_card(deck, question, answer)


def get_num_to_study(deck=False):
    """
    Find out how many cards need to be studied today. Returns int. By default will count all cards, however if a deck
    is specified, it only counts cards due that belong to that deck.
    """
    amt_to_study = 0

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        if not deck:
            for card in dict_reader:
                if card['Due'][:10] <= datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'):
                    amt_to_study += 1
        else:
            for card in dict_reader:
                if (card['Due'][:10] <= datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')) and (card['Deck'] == deck):
                    amt_to_study += 1

    return amt_to_study


def del_deck_cards(deck):
    """
    Deletes all cards in a deck.
    """
    cards_not_in_deck = []

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        # Skips header row.
        next(dict_reader)
        for card in dict_reader:
            if card['Deck'] != deck:
                cards_not_in_deck.append(card)

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'w', newline='') as cards_file:
        dict_writer = csv.DictWriter(cards_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(cards_not_in_deck)


def get_card(deck=False):
    """
    Returns False if no cards are due sometime today. Else it returns a dictionary with the details of the most overdue card.
    deck is an optional parameter that specifies the deck to get the card from, if no cards are due in that deck it returns a
    card from another deck (if one is due, otherwise returns False) (this is done so cards in the same deck are studied together).
    """
    card_due = False
    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        # Skips header.
        next(dict_reader)
        for card in dict_reader:
            if card['Due'][:10] <= datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'):
                card_due = True
                break

    if not card_due:
        return False

    else:
        with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
            dict_reader = csv.DictReader(cards_file, fieldnames=fields)
            # Skips header.
            next(dict_reader)

            # Gets only those due today and sorts them in ascending order, according to due date.
            cards_today = []
            for card in dict_reader:
                if card['Due'][:10] <= datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'):
                    cards_today.append(card)

            cards_today_asc = sorted(cards_today, key=lambda card: card['Due'])

        card_from_deck = False

        if deck:
            for card in cards_today_asc:
                if card['Deck'] == deck:
                    card_from_deck = card
                    break

        if card_from_deck:
            return card_from_deck

        else:
            return cards_today_asc[0]


def correct_ans(current_card):
    """
    Updates the current card in cards.csv when the correct button is pressed. No return.
    """
    if int(current_card['Interval']) >= 1440:
        stats.add_to_correct_1440()

    cards = []

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        # Skips header row.
        next(dict_reader)
        for card in dict_reader:
            cards.append(card)

    for i in range(len(cards)):
        if cards[i]['Question'] == current_card['Question']:
            if cards[i]['Interval'] == '0':
                cards[i]['Due'] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
                cards[i]['Interval'] = '10'

            elif cards[i]['Interval'] == '10':
                cards[i]['Due'] = str(datetime.datetime.now() + datetime.timedelta(minutes=1440))
                cards[i]['Interval'] = '1440'

            else:
                if (type(stats.get_retention_1440(30)) == float) and (stats.get_retention_1440(30) >= settings.get_target_retention_rate()):
                    cards[i]['Ease'] = str(float(cards[i]['Ease']) + 0.1)
                    if float(cards[i]['Ease']) > 5:
                        cards[i]['Ease'] = '5.0'
                    cards[i]['Interval'] = str(int(int(cards[i]['Interval']) * float(cards[i]['Ease'])))
                    cards[i]['Due'] = str(datetime.datetime.now() + datetime.timedelta(minutes=int(cards[i]['Interval'])))
                else:
                    cards[i]['Interval'] = str(int(int(cards[i]['Interval']) * float(cards[i]['Ease'])))
                    cards[i]['Due'] = str(datetime.datetime.now() + datetime.timedelta(minutes=int(cards[i]['Interval'])))

            # Phase 1 is when first learning.
            # Phase 2 is when the user clicks correct on the card for the first time or after clicking correct for the
            # first time, after forgetting.
            # Phase 3 is when the user clicks correct on card that they have gotten correct on the last viewing.

            if cards[i]['Phase'] == '1':
                cards[i]['Phase'] = '2'

            elif cards[i]['Phase'] == '2':
                cards[i]['Phase'] = '3'

            elif cards[i]['Phase'] == 'again 1':
                cards[i]['Phase'] = '2'

            elif cards[i]['Phase'] == 'again 2':
                cards[i]['Phase'] = '2'

            elif cards[i]['Phase'] == 'again 3':
                cards[i]['Phase'] = '2'

            # Can break after it finds the card with a matching question as each question is unique.
            break

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'w', newline='') as cards_file:
        dict_writer = csv.DictWriter(cards_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(cards)


def again_ans(current_card):
    """
    Updates the current card in cards.csv when the again button is pressed. No return.
    """
    if int(current_card['Interval']) >= 1440:
        stats.add_to_again_1440()

    cards = []

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        # Skips header row.
        next(dict_reader)
        for card in dict_reader:
            cards.append(card)

    for i in range(len(cards)):
        if cards[i]['Question'] == current_card['Question']:
            if (not cards[i]['Interval'] == '0') and (not cards[i]['Interval'] == '10'):
                cards[i]['Ease'] = str(float(cards[i]['Ease']) - 0.3)
                if float(cards[i]['Ease']) < 1.3:
                    cards[i]['Ease'] = '1.3'

            cards[i]['Due'] = str(datetime.datetime.now() + datetime.timedelta(minutes=3))
            cards[i]['Interval'] = '0'

            if cards[i]['Phase'] == '1':
                cards[i]['Phase'] = 'again 1'

            elif cards[i]['Phase'] == '2':
                cards[i]['Phase'] = 'again 2'

            elif cards[i]['Phase'] == '3':
                cards[i]['Phase'] = 'again 3'

            # Can break after it finds the card with a matching question as each question is unique.
            break

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'w', newline='') as cards_file:
        dict_writer = csv.DictWriter(cards_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(cards)


def del_card(current_card):
    """
    Finds and deletes a card from cards.txt. No return.
    """
    cards = []

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        # Skips header row.
        next(dict_reader)
        for card in dict_reader:
            # Each question is unique, so this will not ignore multiple cards.
            if card['Question'] == current_card['Question']:
                continue
            cards.append(card)

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'w', newline='') as cards_file:
        dict_writer = csv.DictWriter(cards_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(cards)


def write_card_edit_save(current_card, new_qst, new_ans):
    """
    When the save button is clicked from the edit page, this function updates the card in cards.csv.
    """
    cards = []

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        # Skips header row.
        next(dict_reader)
        for card in dict_reader:
            cards.append(card)

        for i in range(len(cards)):
            if cards[i]['Deck'] == current_card['Deck'] and cards[i]['Question'] == current_card['Question']:
                cards[i]['Question'] = new_qst
                cards[i]['Answer'] = new_ans
                # Can break after it finds the card with a matching deck and question as each deck and question pair is unique.
                break

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'w', newline='') as cards_file:
        dict_writer = csv.DictWriter(cards_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(cards)


def search_for_cards(query):
    """
    Returns a list of cards with the query.
    """
    query = query.lower()
    cards = []

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        # Skips header row.
        next(dict_reader)
        for card in dict_reader:
            if (query in card['Question'].lower()) or (query in card['Answer'].lower()):
                cards.append(card)

    return cards


def check_qst_exists(qst):
    """
    Checks if a question already exists in a card. Returns True if it does, and returns False if it does not.
    """
    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        next(dict_reader)
        for card in dict_reader:
            if card['Question'] == qst:
                return True

    return False


def add_card(deck, qst, ans):
    """
    Appends a card to cards.csv. Return True if successful. Return False is duplicate question
    """
    if check_qst_exists(qst):
        return False

    linear_reg = linear_regression.get_linear_reg()
    if linear_reg:
        ef = linear_reg(len(ans))
        # Maximum EF is 5.0. Minimum is 1.3.
        if ef >= 5:
            card = {
                'Deck': deck,
                'Question': qst,
                'Answer': ans,
                'Ease': '5.0',
                'Due': str(datetime.datetime.now()),
                'Interval': '0',
                'Phase': '1'
            }
        elif ef <= 1.3:
            card = {
                'Deck': deck,
                'Question': qst,
                'Answer': ans,
                'Ease': '1.3',
                'Due': str(datetime.datetime.now()),
                'Interval': '0',
                'Phase': '1'
            }
        else:
            card = {
                'Deck': deck,
                'Question': qst,
                'Answer': ans,
                'Ease': str(ef),
                'Due': str(datetime.datetime.now()),
                'Interval': '0',
                'Phase': '1'
            }
    else:
        card = {
            'Deck': deck,
            'Question': qst,
            'Answer': ans,
            'Ease': '2.5',
            'Due': str(datetime.datetime.now()),
            'Interval': '0',
            'Phase': '1'
        }

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'a', newline='') as cards_file:
        dict_writer = csv.DictWriter(cards_file, fieldnames=fields)
        dict_writer.writerow(card)

    return True


def change_deck(old_deck_name, new_deck_name, qst=False):
    """
    Changes the deck as set of cards belongs to. If qst is not False it will only change the deck of the card with that
    question (note: each question is unique).
    """
    cards_to_update = []
    cards_not_to_update = []
    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'r') as cards_file:
        dict_reader = csv.DictReader(cards_file, fieldnames=fields)
        next(dict_reader)
        if qst:
            for card in dict_reader:
                if card['Deck'] == old_deck_name and card['Question'] == qst:
                    cards_to_update.append(card)
                else:
                    cards_not_to_update.append(card)
        else:
            for card in dict_reader:
                if card['Deck'] == old_deck_name:
                    cards_to_update.append(card)
                else:
                    cards_not_to_update.append(card)

    for card in cards_to_update:
        card['Deck'] = new_deck_name

    with open(f'{temp_path}\\..\\MemoryGain\\cards.csv', 'w', newline='') as cards_file:
        dict_writer = csv.DictWriter(cards_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(cards_to_update)
        dict_writer.writerows(cards_not_to_update)


if __name__ == '__main__':
    cards_on_device()














