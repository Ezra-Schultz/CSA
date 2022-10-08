from nltk.corpus import words
import pyautogui
import random
import time
import requests

pyautogui.hotkey('winleft', '3')
time.sleep(.1)
# wordlist = [words.words()[random.randrange(0, len(words.words()))] + ' ' for word in range(len(words.words()))]
for i in range(29):
    word = list(words.words()[random.randrange(0, len(words.words()))])
    word[0] = word[0].upper()
    word = ''.join(word)
    pyautogui.typewrite(word, 10e-15)
    pyautogui.press('down')
    # [pyautogui.typewrite(word, 10e-15) for word in wordlist]
