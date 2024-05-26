# MemoryGain
MemoryGain is a flashcards app that aims to apply various algorithms to aid human learning, with a focus on machine learning.

# TO RUN

(Currently only works on Windows)

```
git clone https://github.com/JoshuaChick/MemoryGain
```
```
cd MemoryGain
```
```
python MemoryGain.py
```

# Studying

Every card in MemoryGain has a due date and time. When you go to study, MemoryGain will give you all the cards that are due anytime that day. It will present the cards from most-overdue to least-overdue.


# Spaced Repetition

The main aim of MemoryGain is to find the optimal amount of time to space out repetitions of your cards, as to try to maximize your retention while minimizing the amount of time you spend studying. The way MemoryGain determines intervals is loosely based-off of the SM-2 learning algorithm (https://www.supermemo.com/en/archives1990-2015/english/ol/sm2), with a few improvements.


# Retention

Your retention rate in MemoryGain is defined as the amount of times you have correctly answered your cards (with an interval of 1 day or more at the time of answering) divided by the total amount of answers you have given (also only for cards with an interval of 1 day or more at the time of answering).


# Ease Factor

Every card has an ease factor. This ease factor is used to determine the spacing between repetitions. While you have 100 or less cards, the ease factor for new cards will be 2.5. However, if you have over 100 cards, linear regression will be performed with the character count of your cards on the x-axis and their ease factor on the y-axis to determine the new ease factor (as there is a negative correlation between character count and the ease factor required to reliably remember the card). If you get a card correct (which has an interval of 1 day or more at the time of answering, and the retention rate for the past 30 days is greater than or equal to your target retention rate) 0.1 is added to that card's ease factor. If you get a card wrong (which has an interval of 1 day or more at the time of answering) 0.3 is taken away from the ease factor. The greatest allowed ease factor is 5 and the smallest allowed ease factor is 1.3.


# Interval

When a card is either made or forgotten it will have an interval of 0. When this card is correctly answered it will be given an interval of 10 minutes. When a card with an interval of 10 minutes is answered correctly it will be given an interval of 1 day. When a card with an interval of 1 day or more is correctly answered the interval will equal the current interval times the ease factor.
