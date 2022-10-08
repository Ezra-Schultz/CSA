from nltk.corpus import words
import pyautogui
import random
import time
import requests

pyautogui.hotkey('winleft', '1')
time.sleep(.1)
wordlist = [words.words()[random.randrange(0, len(words.words()))] + ' ' for word in range(len(words.words()))]
for i in range(1000):
    pyautogui.typewrite(words.words()[random.randrange(0, len(words.words()))] + ' ', 0.000000000000001)
    [pyautogui.typewrite(word, 10e-15) for word in wordlist]