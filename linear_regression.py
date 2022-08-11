"""
Contains functions related to performing linear regression on two lists.
"""

import math
import cards


def get_pearson_correlation_coefficient(x, y):
    """
    Returns correlation coefficient of two lists x, y.
    r = sum((x - mean_x) * (y - mean_y)) / sqrt(sum((x - mean_x)^2) * sum((y - mean_y)^2))
    """
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = 0

    for i in range(len(x)):
        numerator += (x[i] - mean_x) * (y[i] - mean_y)

    sum_squares_x = 0

    for i in range(len(x)):
        sum_squares_x += (x[i] - mean_x)**2

    sum_squares_y = 0

    for i in range(len(y)):
        sum_squares_y += (y[i] - mean_y)**2

    denominator = (sum_squares_x * sum_squares_y)**.5

    return numerator / denominator


def get_sample_std_dev(x):
    """
    Returns sample std dev. x must have a length greater than 1 as the denominator will be length - 1.
    sample_std_dev = sqrt(sum(x - mean_x)^2 / length_x - 1)
    """
    mean_x = sum(x) / len(x)

    sum_squares_x = 0

    for num in x:
        sum_squares_x += (num - mean_x)**2

    return (sum_squares_x / (len(x) - 1))**.5


def get_linear_reg():
    """
    Performs linear regression on cards character count and ease factor. Character count is x-axis, and ease factor is
    y-axis. Returns False if there is less than 100 cards or if the relationship is positive (as experiments would
    indicate that the more chars the more frequently the card should be reviewed). Else returns a function in the form
    y = a + bx.
    """
    x_chars = []
    y_ease_factors = []

    cards_var = cards.search_for_cards('')
    if len(cards_var) <= 100:
        return False

    for card in cards_var:
        x_chars.append(len(card['Answer']))
        y_ease_factors.append(float(card['Ease']))

    if get_pearson_correlation_coefficient(x_chars, y_ease_factors) > 0:
        return False

    b = get_pearson_correlation_coefficient(x_chars, y_ease_factors) * get_sample_std_dev(y_ease_factors) / get_sample_std_dev(x_chars)
    a = (sum(y_ease_factors) / len(y_ease_factors)) - (b*(sum(x_chars) / len(x_chars)))

    def linear_reg(chars):
        return a + (b*chars)

    return linear_reg




















