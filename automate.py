# Import dependencies
import decrypt
import tkinter as tk
import math
import random
import pycipher

# Import sub-dependencies
from itertools import permutations
# from interface import keys_top, keystested, key_updater, bestfitness, \
#     cipher_output, restore, pb, stopper, selected_period, key, bestkey
from interface import bestfitness
from analyse import quadgram_score, chisqr, indice_coincidence

# Initialise quad-gram fitness testing
fitness = quadgram_score()

def crack_vigenere(ctext,pbprogress):
    global top10keys
    top10keys = ["" for x in range(10)]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    best_overall = -99e9
    count = 0
    for keylength in range(1, 16):
        parentkey = "A" * keylength
        parentscore = fitness.score(decrypt.vigenere(ctext, parentkey))
        parentkey = list(parentkey)
        best_starter_score = parentscore
        best_starter = "".join(parentkey)
        for i in range(keylength):
            for letter in alphabet:
                parentkey = list(parentkey)
                child = parentkey
                child[i] = letter
                child = "".join(child)
                childscore = fitness.score(decrypt.vigenere(ctext, child))
                if childscore > best_starter_score:
                    best_starter_score = childscore
                    best_starter = child
                if childscore > best_overall:
                    bestfitness.config(text=str(round(childscore)))
                    top10keys.append(child)
                    key_updater(top10keys)
                    best_overall = childscore
                    best_key = child
                    cipher_output.delete('1.0',tk.END)
                    cipher_output.insert(tk.INSERT,restore(decrypt.vigenere(ctext, best_key)))
                    cipher_output.update()
                count += 1
                keystested.config(text=str(count))
                pbprogress.set(int((count/3120)*100))
                pb.update()
            parentkey = best_starter

def crack_beaufort(ctext,pbprogress):
    global top10keys
    top10keys = ["" for x in range(10)]
    ctext = decrypt.atbash(ctext)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    best_overall = -99e9
    count = 0
    for keylength in range(1, 16):
        parentkey = "A" * keylength
        parentscore = fitness.score(decrypt.vigenere(ctext, parentkey))
        parentkey = list(parentkey)
        best_starter_score = parentscore
        best_starter = "".join(parentkey)
        for i in range(keylength):
            for letter in alphabet:
                parentkey = list(parentkey)
                child = parentkey
                child[i] = letter
                child = "".join(child)
                childscore = fitness.score(decrypt.vigenere(ctext, child))
                if childscore > best_starter_score:
                    best_starter_score = childscore
                    best_starter = child
                if childscore > best_overall:
                    bestfitness.config(text=str(round(childscore)))
                    top10keys.append(decrypt.atbash(child))
                    key_updater(top10keys)
                    best_overall = childscore
                    best_key = child
                    cipher_output.delete('1.0',tk.END)
                    cipher_output.insert(tk.INSERT,restore(decrypt.vigenere(ctext, best_key)))
                    cipher_output.update()
                count += 1
                keystested.config(text=str(count))
                pbprogress.set(int((count/3120)*100))
                pb.update()
            parentkey = best_starter

def crack_caesar(ctext,pbprogress):

    shifted = []
    stringsqr = []
    for i in range(26):
        shifted.append(decrypt.caesar(ctext, 26 - i))
        stringsqr.append(chisqr(shifted[i]))  # Calculate Chi^2 Statistics
        keystested.config(text=str(i+1))
    bestfitness.config(text=str(round(min(stringsqr))))
    key = stringsqr.index(min(stringsqr))  # Key will be shift with lowest Chi^2 Statistic
    decrypted = decrypt.caesar(ctext, 26 - key)
    pbprogress.set(100)
    bestkeys = []
    allkeys = stringsqr[:]
    for i in range(10):
        bestkeys.append(allkeys.index(min(stringsqr)))
        stringsqr.remove(min(stringsqr))
        keys_top[i].config(text=str(bestkeys[i]),font="Courier 11")
    pb.update()
    cipher_output.delete('1.0',tk.END)
    cipher_output.insert(tk.INSERT,restore(decrypted))
    cipher_output.update()

def crack_coltrans(ctext,pbprogress):

    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    max_score = -99 * (10 ** 9)
    count = 0
    top10keys = ["" for x in range(10)]
    for i in range(2, 8):
        current_alphabet = alphabet[:i]
        current_alphabet = "".join(current_alphabet)
        perms = [''.join(p) for p in permutations(current_alphabet)]
        for j in range(len(perms)):
            deciphered = pycipher.ColTrans(perms[j]).decipher(ctext)
            score = fitness.score(deciphered)
            if score > max_score:
                top10keys.append(perms[j])
                key_updater(top10keys)
                bestfitness.config(text=str(round(score)))
                max_score = score
                cipher_output.delete('1.0', tk.END)
                cipher_output.insert(tk.INSERT, restore(deciphered))
                cipher_output.update()
            count += 1
            pbprogress.set(round((count/5912)*100))
            pb.update()
            keystested.config(text=str(count))

def crack_polybius(ctext,pbprogress):
    chars = "".join(list(set(ctext)))
    maxkeys = math.factorial(len(chars))
    perms = [''.join(p) for p in permutations(chars)]
    best_score = -99e9
    top10keys = ["" for x in range(10)]
    count = 0
    for key in perms:
        # NOTE: Pycipher has issues if cipher is made up of digits
        deciphered = pycipher.PolybiusSquare("ABCDEFGHIKLMNOPQRSTUVWXYZ", len(chars), key).decipher(ctext)
        score = fitness.score(deciphered)
        if score > best_score:
            bestfitness.config(text=str(round(score)))
            top10keys.append(key)
            key_updater(top10keys)
            best_score = score
            best_decryption = deciphered
            cipher_output.delete('1.0', tk.END)
            cipher_output.insert(tk.INSERT, restore(best_decryption))
            cipher_output.update()
        count += 1
        keystested.config(text=str(count))
        pbprogress.set(round((count/maxkeys)*100))
        pb.update()

def crack_2x2hill(ctext,pbprogress):
    padded = len(ctext)
    if len(ctext) % 2 != 0:
        ctext = ctext + "X"
        padded = 1
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    combinations = []
    for i in range(26):
        for j in range(26):
            combinations.append([i, j])
    cvectors = []
    for i in range(0, len(ctext), 2):
        cvectors.append([alphabet.index(ctext[i+j]) for j in range(2)])
    decryption_score = []
    totalloops = len(combinations)
    count = 0
    for combo in combinations:
        current_decryption = []
        for block in cvectors:
            current_decryption.append(chr(((block[0] * combo[0] + block[1] * combo[1]) % 26) + 65))
        cipher_output.delete('1.0', tk.END)
        cipher_output.insert(tk.INSERT, restore("".join(current_decryption)))
        cipher_output.update()
        count += 1
        keystested.config(text=str(count))
        pbprogress.set(round((count/totalloops)*100))
        pb.update()
        decryption_score.append(chisqr("".join(current_decryption)))
        bestfitness.config(text=str(round(decryption_score[-1])))
    decryption_score_copy = decryption_score[:]
    best_1 = combinations[decryption_score_copy.index(min(decryption_score))]
    decryption_score.remove(min(decryption_score))
    best_2 = combinations[decryption_score_copy.index(min(decryption_score))]
    for i in range(2):
        best_1[i] = str(best_1[i])
        best_2[i] = str(best_2[i])
    key1 = " ".join(best_1) + " " + " ".join(best_2)
    key2 = " ".join(best_2) + " " + " ".join(best_1)
    decry1 = decrypt.hill2x2(ctext, key1)
    decry2 = decrypt.hill2x2(ctext, key2)
    s1 = fitness.score(decry1)
    s2 = fitness.score(decry2)
    print(padded)
    if s1 > s2:
        cipher_output.delete('1.0', tk.END)
        if padded == 1:
            complete = restore(decry1[:-1])
        else:
            complete = restore(decry1)
        cipher_output.insert(tk.INSERT, complete)
        cipher_output.update()
        keys_top[0].config(text=key1)
        keys_top[1].config(text=key2)
    else:
        cipher_output.delete('1.0', tk.END)
        if padded == 1:
            complete = restore(decry2[:-1])
        else:
            complete = restore(decry2)
        cipher_output.insert(tk.INSERT, complete)
        cipher_output.update()
        keys_top[0].config(text=key2)
        keys_top[1].config(text=key1)

def crack_3x3hill(ctext,pbprogress):
    padded = len(ctext)
    if len(ctext) % 3 == 1:
        ctext = ctext + "XX"
        padded = 2
    elif len(ctext) % 3 == 2:
        ctext = ctext + "X"
        padded = 1
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    combinations = []
    for i in range(26):
        for j in range(26):
            for k in range(26):
                combinations.append([i, j, k])
    print(combinations)
    cvectors = []
    for i in range(0, len(ctext), 3):
        cvectors.append([alphabet.index(ctext[i]), alphabet.index(ctext[i + 1]), alphabet.index(ctext[i+2])])
    print(cvectors)
    decryption_score = []
    totalloops = len(combinations)
    count = 0
    for combo in combinations:
        current_decryption = []
        for block in cvectors:
            current_decryption.append(chr(((block[0] * combo[0] + block[1] * combo[1] + block[2] * combo[2]) % 26) + 65))
        cipher_output.delete('1.0', tk.END)
        cipher_output.insert(tk.INSERT, restore("".join(current_decryption)))
        cipher_output.update()
        count += 1
        keystested.config(text=str(count))
        pbprogress.set(round((count/totalloops)*100))
        pb.update()
        decryption_score.append(chisqr("".join(current_decryption)))
        bestfitness.config(text=str(round(decryption_score[-1])))
    decryption_score_copy = decryption_score[:]
    best_1 = combinations[decryption_score_copy.index(min(decryption_score))]
    decryption_score.remove(min(decryption_score))
    best_2 = combinations[decryption_score_copy.index(min(decryption_score))]
    decryption_score.remove(min(decryption_score))
    best_3 = combinations[decryption_score_copy.index(min(decryption_score))]
    print(best_1)
    print(best_2)
    print(best_3)
    for i in range(3):
        best_1[i] = str(best_1[i])
        best_2[i] = str(best_2[i])
        best_3[i] = str(best_3[i])
    key1 = " ".join(best_1) + " " + " ".join(best_2) + " " + " ".join(best_3)
    key2 = " ".join(best_1) + " " + " ".join(best_3) + " " + " ".join(best_2)
    key3 = " ".join(best_2) + " " + " ".join(best_1) + " " + " ".join(best_3)
    key4 = " ".join(best_2) + " " + " ".join(best_3) + " " + " ".join(best_1)
    key5 = " ".join(best_3) + " " + " ".join(best_1) + " " + " ".join(best_2)
    key6 = " ".join(best_3) + " " + " ".join(best_2) + " " + " ".join(best_1)

    decry = []
    keylist = []
    for key in (key1,key2,key3,key4,key5,key6):
        keylist.append(key)
        decry.append(decrypt.hill3x3(ctext,key))
    s = []
    for decryption in decry:
        s.append(fitness.score(decryption))
    s2 = s[:]
    for i in range(6):
        x = s2.index(max(s))
        if i == 0:
            if padded == 1:
                complete = restore(decry[x][:-1])
            elif padded == 2:
                complete = restore(decry[x][:-2])
            else:
                complete = restore(decry[x])
            cipher_output.delete('1.0', tk.END)
            cipher_output.insert(tk.INSERT, complete)
            cipher_output.update()
        keys_top[i].config(text=keylist[x],font="Courier 7")
        if i != 5:
            s.remove(max(s))

def crack_substitution(ctext,pbprogress):
    stopper.config(state=tk.NORMAL)
    global stop
    stop = False
    pb.config(mode='indeterminate')
    pb.start()
    tested = 0
    maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    maxscore = -99e9
    parentscore, parentkey = maxscore, maxkey[:]
    # keep going until we are killed by the user
    i = 0
    while True:
        i += 1
        random.shuffle(parentkey)
        deciphered = decrypt.substitution(ctext,parentkey)
        parentscore = fitness.score(deciphered)
        count = 0
        while count < 1000:
            pb.update()
            a = random.randint(0, 25)
            b = random.randint(0, 25)
            child = parentkey[:]
            # swap two characters in the child
            child[a], child[b] = child[b], child[a]
            deciphered = decrypt.substitution(ctext,child)
            score = fitness.score(deciphered)
            # if the child was better, replace the parent with it
            if score > parentscore:
                parentscore = score
                parentkey = child[:]
                count = 0
            count = count + 1
            tested += 1
            keystested.config(text=str(tested))
            if stop == True: break
        # keep track of best score seen so far
        if parentscore > maxscore:
            maxscore, maxkey = parentscore, parentkey[:]
            bestfitness.config(text=str(round(maxscore)))
            current_keys = []
            for i in range(10):
                current_keys.append(keys_top[i].cget('text'))
            current_keys = current_keys[:-1]
            for i in range(1,10):
                keys_top[i].config(text=current_keys[i-1])
            keys_top[0].config(text="".join(maxkey)[:15])
            ss = decrypt.substitution(ctext,maxkey)
            cipher_output.delete('1.0', tk.END)
            cipher_output.insert(tk.INSERT, restore(ss))
            cipher_output.update()
        if stop == True: break
    stopper.config(state=tk.DISABLED)

def crack_vigenere_affine(ctext,pbprogress):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    best_overall = -99e9
    coprime_26 = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]  # Removed 1 to save time
    period = selected_period.get()
    if key.get() == "":
        average = []
        for j in range(2, 16):
            sequence = []
            for k in range(j):
                text = list(ctext[k:])
                n = j
                output = []
                i = 0
                while i < len(text):
                    output.append(text[i])
                    i = i + int(n)
                phrase = "".join(output)
                sequence.append(indice_coincidence(phrase))  # Calculate each index of coincidence
            average.append(sum(sequence) / len(sequence))  # Calculate average IC for each period

        keylength = average.index(max(average)) + 2
    else: keylength = len(key.get())
    count = 0
    top10keys = ["" for x in range(10)]
    actualkey = key.get().upper()
    if period != "-":
        coprime_26 = [int(period)]
    print(coprime_26)
    totaltests = len(coprime_26)*keylength*26
    for a in coprime_26:
        if actualkey == "":
            parentkey = "A" * keylength
            print(a)
            parentscore = fitness.score(decrypt.vigenereaffine(ctext, parentkey, a))
            parentkey = list(parentkey)
            best_starter_score = parentscore
            best_starter = "".join(parentkey)
            for i in range(keylength):
                for letter in alphabet:
                    parentkey = list(parentkey)
                    child = parentkey
                    child[i] = letter
                    child = "".join(child)
                    childscore = fitness.score(decrypt.vigenereaffine(ctext, child, a))
                    if childscore > best_starter_score:
                        best_starter_score = childscore
                        best_starter = child
                    if childscore > best_overall:
                        bestfitness.config(text=str(round(childscore)))
                        top10keys.append(child)
                        key_updater(top10keys)
                        best_overall = childscore
                        best_key = child
                        best_a = a
                        cipher_output.delete('1.0', tk.END)
                        cipher_output.insert(tk.INSERT, restore(decrypt.vigenereaffine(ctext, best_key, best_a)))
                        cipher_output.update()
                    count += 1
                    keystested.config(text=str(count))
                    pbprogress.set(round((count/totaltests)*100))
                    pb.update()
                parentkey = best_starter
        else:
            bestkey.config(text=str(actualkey))
            parentscore = fitness.score(decrypt.vigenereaffine(ctext, actualkey, a))
            if parentscore > best_overall:
                best_overall = parentscore
                best_a = a
                cipher_output.delete('1.0', tk.END)
                cipher_output.insert(tk.INSERT, restore(decrypt.vigenereaffine(ctext, actualkey, best_a)))
                cipher_output.update()
            count += 1
            keystested.config(text=str(count))
            pbprogress.set(round((count/len(coprime_26))*100))
            pb.update()

def crack_vigenere_scytale(ctext,pbprogress):
    stopper.config(state=tk.NORMAL)
    global stop
    stop = False
    pb.config(mode='indeterminate')
    pb.start()
    top10keys = ["" for x in range(10)]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    best_overall = -99e9
    best_scytale = -99e9
    count = 0
    for scytale in range(1, 11):
        cipher = pycipher.ColTrans(alphabet[0:scytale + 1]).decipher(ctext)
        for keylength in range(1, 21):
            parentkey = "A" * keylength
            parentscore = fitness.score(decrypt.vigenere(cipher, parentkey))
            parentkey = list(parentkey)
            best_starter_score = parentscore
            best_starter = "".join(parentkey)
            for i in range(keylength):
                for letter in alphabet:
                    parentkey = list(parentkey)
                    child = parentkey
                    child[i] = letter
                    child = "".join(child)
                    childscore = fitness.score(decrypt.vigenere(cipher, child))
                    if childscore > best_starter_score:
                        best_starter_score = childscore
                        best_starter = child
                    if childscore > best_overall:
                        best_overall = childscore
                        best_key = child
                    pb.update()
                parentkey = best_starter
                count += 1
                keystested.config(text=str(count))
                if stop == True: break
            if stop == True: break
        if stop == True: break

        current_scytale = fitness.score(decrypt.vigenere(cipher, best_key))
        if current_scytale > best_scytale:
            top10keys.append(best_key)
            key_updater(top10keys)
            bestfitness.config(text=str(round(current_scytale)))
            best_scytale = current_scytale
            cipher_output.delete('1.0', tk.END)
            cipher_output.insert(tk.INSERT, restore(decrypt.vigenere(cipher,best_key)))
            cipher_output.update()
    stopper.config(state=tk.DISABLED)