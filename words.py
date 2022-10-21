from nltk.corpus import words
import pyautogui, random, time, requests

wordlist = []
for i in words.words():
    wordlist.append(i)
    print(i)

failed = []
success = []
for i in range(10):
    word = wordlist[random.randrange(0, len(wordlist))]
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    json = requests.get(url).json()

    try:
        json["title"]
        failed.append(word)
    except:
        json[0]
        success.append(word)
print(failed, len(failed))
print(success, len(success))
while failed != []:
    word = wordlist[random.randrange(0, len(wordlist))]
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    json = requests.get(url).json()
    try:
        json["title"]
    except:
        failed.pop(0)
        success.append(word)
    print(failed, success)
for i in success:
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + i
    json = requests.get(url).json()
    i = list(i)
    i[0] = i[0].upper()
    i = ''.join(i)
    print(i)
    for j in json[0]["meanings"][0]["definitions"]:
        print(j["definition"])
    print()
    
