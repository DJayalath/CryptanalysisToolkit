# Program to process and standardize encrypted cipher
import re

def process2(text):
    store_punctuation(text)
    encryptedText = (re.sub('[^A-Za-z0-9]+', '', text)).upper()
    return encryptedText
def store_punctuation(text):
    global punctuation
    punctuation = []
    global len_original
    len_original = len(text)
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    for i in range(len(text)):
        if text[i] not in alphabet:
            punctuation.append([text[i],i])
def restore_punctuation(text):
    global punctuation
    global len_original
    print(punctuation)
    text = list(text)
    for i in range(len(punctuation)):
        text.insert(punctuation[i][1],punctuation[i][0])
    return "".join(text)