# Import dependencies
import tkinter as tk
import math
import decrypt
import random
import pycipher
import re

# Import sub-dependencies
from itertools import permutations
from tkinter import ttk, messagebox
from graphing import freqanalysis, icgraph
from analyse import chisqr, indice_coincidence, quadgram_score

fitness = quadgram_score()


# Cipher class for ctext manipulation
class Cipher:

    def __init__(self):
        print(trunc.get())
        if trunc.get() != "":
            print("TEST")
            self.ciphertext = cipher_input.get('1.0', tk.END).replace('\n', '').replace('\r', '')[:int(trunc.get())]
            cipher_input.delete('1.0',tk.END)
            cipher_input.insert(tk.INSERT,self.ciphertext)
        else:
            self.ciphertext = cipher_input.get('1.0', tk.END).replace('\n', '').replace('\r', '')

    modified = False

    def get(self):
        return self.ciphertext

    def clean(self):
        return re.sub('[^A-Za-z0-9]+', '', self.ciphertext).upper()

    def store(self):
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        self.nonalphabetic = []
        self.case = []
        for i in range(len(self.ciphertext)):
            if self.ciphertext[i] not in alphabet:
                self.nonalphabetic.append([self.ciphertext[i], i])
            else:
                if self.ciphertext[i].islower() is True:
                    self.case.append(i)

    def restore(self,dtext):
        dtext = list(dtext)
        for i in range(len(self.nonalphabetic)):
            dtext.insert(self.nonalphabetic[i][1], self.nonalphabetic[i][0])
        for i in range(len(self.case)):
            dtext[self.case[i]] = dtext[self.case[i]].lower()
        return "".join(dtext)

    def reverse_words(self):
        if self.modified == False:
            self.store()
        raw = Cipher().get()
        words_spaces = []
        for i in range(len(raw)):
            if raw[i] in list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "):
                words_spaces.append(raw[i])
        words_spaces = "".join(words_spaces)
        reversed = []
        for word in words_spaces.split(' '):
            reversed.append(word[::-1])
        self.modified = True
        cipher_input.delete('1.0', tk.END)
        cipher_input.insert(tk.INSERT,self.restore("".join(reversed)))

    def reverse_string(self):
        if self.modified == False:
            self.store()
        raw = Cipher().get()
        cipher_input.delete('1.0', tk.END)
        cipher_input.insert(tk.END, raw[::-1])
        self.modified = True

    def reset(self):
        cipher_input.delete('1.0', tk.END)
        cipher_input.insert(tk.INSERT,self.get())

# Updates on cipher edit
def typing(event):

    # Set current cipher
    global global_cipher
    global_cipher = Cipher()

    # Calculate ctext IOC
    update_ic()
    # Predict Key length
    update_keylength()

def update_ic():

    char_count = len(global_cipher.clean())
    char_string = str(char_count)
    charcount.config(text=char_string)

    ic_score = round(indice_coincidence(global_cipher.clean()),4)
    if len(str(ic_score)) != 6:
        ic_score = str(ic_score)
        while len(ic_score) != 6:
            ic_score += "0"

    ic.config(text = str(ic_score))

# Periodic IC calculations
def update_keylength():

    ctext = global_cipher.clean()
    average = []
    for j in range(2, 21):
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
        average.append(sum(sequence) / len(sequence))

    periodic_calc = average
    highest_ic_fig = periodic_calc.index(max(periodic_calc)) + 2
    highest_ic = max(periodic_calc)
    periodic_calc.remove(max(periodic_calc))
    next_ic = max(periodic_calc)
    diff = round(((highest_ic - next_ic)/next_ic)*100,2)
    periodic.config(text=str(highest_ic_fig))
    difference.config(text="(" + str(diff) + "%)")

# def callback(event):
#
#     if "Hill" in selected_cipher.get():
#         scale.config(state=tk.NORMAL)
#
#     else:
#         scale.config(state=tk.DISABLED)
#         scale_label.destroy()
#
# #def callback_scale():



def set_cipherselection(v,cipher_list):
    if v.get() == 1:
        cipher_list.grid_forget()
        # Edit this one for effect
        cipher_list = ttk.OptionMenu(decryptionconfig,selected_cipher,"Vigenere","Vigenere","Beaufort","Caesar","Substitution","Columnar","Polybius","Hill (2x2)","Hill (3x3)")
        cipher_list.grid(row=1, column=1, padx=5, sticky="ew")
        cipher_list.grid_propagate(False)
    else:
        cipher_list.grid_forget()
        cipher_list = ttk.OptionMenu(decryptionconfig,selected_cipher,"Vigenere/Affine","Vigenere/Affine","Vigenere/Scytale")
        cipher_list.grid(row=1, column=1, padx=5, sticky="ew")
        cipher_list.grid_propagate(False)

def stop_cipher(pbprogress):
    pb.stop()
    global stop
    stop = True
    pb.config(mode='determinate')
    pbprogress.set(0)
    pb.update()

def key_updater(top10keys):
    top10keys = top10keys[-10:]
    for i in range(10):
        keys_top[9 - i].config(text=top10keys[i])

def solve_cipher(cipher,pbprogress):
    for i in range(10):
        keys_top[i].config(text="")
    bestkey.config(text="-")
    bestfitness.config(text="0")
    keystested.config(text="0")
    pbprogress.set(0)
    pb.update()

    # ctext_class = Cipher(cipher_input.get('1.0',tk.END))
    global global_cipher
    global_cipher = Cipher()
    ctext_class = global_cipher
    ctext_class.store()

    if cipher == "*Select Cipher":
        messagebox.showerror("Decryption","No cipher selected")
    elif cipher == "Vigenere":
        if key.get() == "":
            crack_vigenere(ctext_class)
        else:
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.vigenere(ctext_class.clean(),key.get().upper())))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Beaufort":
        if key.get() == "":
            crack_beaufort(ctext_class,pbprogress)
        else:
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.vigenere(decrypt.atbash(ctext_class.clean()),decrypt.atbash(key.get().upper()))))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Caesar":
        if key.get() == "":
            crack_caesar(ctext_class,pbprogress)
        else:
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.caesar(ctext_class.clean(),key.get().upper())))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Columnar":
        if key.get() == "":
            crack_coltrans(ctext_class,pbprogress)
        else:
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(pycipher.ColTrans(key.get().upper()).decipher(ctext_class.clean())))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Polybius":
        if key.get() == "":
            crack_polybius(ctext_class,pbprogress)
    elif cipher == "Hill (2x2)":
        if key.get() == "":
            crack_2x2hill(ctext_class,pbprogress)
        else:
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.hill2x2(ctext_class.clean(),key.get())))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Hill (3x3)":
        if key.get() == "":
            crack_3x3hill(ctext_class,pbprogress)
        else:
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.hill3x3(ctext_class.clean(),key.get())))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Substitution":
        if key.get() == "":
            crack_substitution(ctext_class,pbprogress)
        else:
            alpha = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")
            key_in_use = key.get().upper()
            if len(key_in_use) != 26:
                for letter in key_in_use:
                    alpha.remove(letter)
            key_in_use = key_in_use + "".join(alpha)
            print(key_in_use)
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.substitution(ctext_class.clean(),key_in_use)))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Vigenere/Affine":
        if key.get() == "" or selected_period.get() == "-":
            crack_vigenere_affine(ctext_class,pbprogress)
        else:
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.vigenereaffine(ctext_class.clean(),key.get().upper(),int(selected_period.get()))))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()
    elif cipher == "Vigenere/Scytale":
        if key.get() == "" and selected_period.get() == "-":
            crack_vigenere_scytale(ctext_class,pbprogress)
        elif selected_period.get() != "-":
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            crack_vigenere(pycipher.ColTrans(alphabet[0:int(selected_period.get())]).decipher(ctext_class.clean()),pbprogress)
        elif key.get() != "":
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            bestsofar = -99e9
            count = 0
            for scytale in range(1, 11):
                cipher2 = decrypt.vigenere(pycipher.ColTrans(alphabet[0:scytale + 1]).decipher(ctext_class.clean()),key.get().upper())
                print(cipher2)
                chill = fitness.score(cipher2)
                if chill > bestsofar:
                    bestsofar = chill
                    cipher_output.delete('1.0', tk.END)
                    cipher_output.insert(tk.INSERT, ctext_class.restore(cipher2))
                    cipher_output.update()
                count += 1
                keystested.config(text=str(count))
                pbprogress.set(round((count/10)*100))
                pb.update()

        else:
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            text = pycipher.ColTrans(alphabet[0:int(selected_period.get())]).decipher(ctext_class.clean())
            text = decrypt.vigenere(text,key.get().upper())
            cipher_output.delete('1.0',tk.END)
            cipher_output.insert(tk.INSERT,ctext_class.restore(text))
            cipher_output.update()
            pbprogress.set(100)
            pb.update()

    bestkey.config(text=keys_top[0].cget('text'))

# Master container
master = tk.Tk()
master.option_add("*Font", "Helvetica 11")
master.geometry('{}x{}'.format(700, 680))
master.title("Cryptanalysis Toolbox v2.0 by Dulhan Jayalath")

# Ciphertext input box
ttk.Label(master,text="Encrypted Text").grid(row=0,column=1,columnspan=10,pady=5)
scrollbar = ttk.Scrollbar(master)
scrollbar.grid(row=1,column=2,sticky=tk.NSEW)

cipher_input = tk.Text(master, wrap=tk.WORD, yscrollcommand=scrollbar.set,height=5,width=80)
cipher_input.grid(row=1,column=1,padx=(20,0))
cipher_input.bind('<KeyRelease>',typing)

scrollbar.config(command=cipher_input.yview)

# Text manipulation options
# def save_text():
#     global text_orig
#     text_orig = cipher_input.get('1.0', tk.END)
#     global modified
# def reverse_word_lettering():
#     global modified
#     if modified == False:
#         save_text()
#     text = cipher_input.get('1.0',tk.END).replace('\n','').replace('\r','').split(' ')
#     reversed_text = []
#     for word in text:
#         reversed_text.append(word[::-1])
#     cipher_input.delete('1.0',tk.END)
#     reversed_text = " ".join(reversed_text)
#     cipher_input.insert(tk.INSERT, reversed_text)
#     modified = True
# def reverse_string():
#     global modified
#     if modified == False:
#         save_text()
#     text = cipher_input.get('1.0', tk.END).replace('\n', '').replace('\r', '')
#     cipher_input.delete('1.0', tk.END)
#     cipher_input.insert(tk.INSERT, text[::-1])
#     modified = True
# def reset_string():
#     global text_orig
#     cipher_input.delete('1.0', tk.END)
#     cipher_input.insert(tk.INSERT, text_orig)
# def clear():
#     # global text_orig
#     # text_orig = ""
#     # global modified
#     # modified = False
#     cipher_input.delete('1.0', tk.END)


# Text Manipulation Buttons
manipulation_frame = ttk.Frame(master)
ttk.Button(manipulation_frame,text="Reverse Full String",command=lambda: global_cipher.reverse_string()).grid(row=0,column=0)
ttk.Button(manipulation_frame,text="Reverse Word Lettering",command=lambda: global_cipher.reverse_words()).grid(row=0,column=1,padx=2)
ttk.Button(manipulation_frame,text="Reset Full String",command=lambda: global_cipher.reset()).grid(row=0,column=2,padx=(0,2))
tk.Label(manipulation_frame,text="Truncation (Chars)",font="Helvetica 9").grid(row=0,column=4,padx=(63,0))
trunc = ttk.Entry(manipulation_frame,width=5)
trunc.grid(row=0,column=5,padx=5)
ttk.Button(manipulation_frame,text="Clear",command=lambda: cipher_input.delete('1.0', tk.END)).grid(row=0,column=3,padx=(0,2))
manipulation_frame.grid(row=2,column=1,sticky=tk.W,padx=(20,0),pady=5)

# Frame enclosing statistics, graphs and decryption label-frames
layer_frames = ttk.Frame(master)

# Statistics Frame
stats = ttk.LabelFrame(layer_frames,text="Statistics",width=200)

ttk.Label(stats,text="Index of Coincidence",font="Helvetica 8").grid(row=0,column=0,sticky=tk.W)#
ic = ttk.Label(stats,text="0.0000",font="Helvetica 8 bold")
ic.grid(row=0,column=2,sticky=tk.E)

ttk.Label(stats,text="Characters",font="Helvetica 8").grid(row=1,column=0,sticky=tk.W)
charcount = ttk.Label(stats,text="0",font="Helvetica 8 bold")
charcount.grid(row=1,column=2,sticky=tk.E)

ttk.Label(stats,text="Key-length (Confidence)",font="Helvetica 8").grid(row=2,column=0,sticky=tk.W)
periodic = ttk.Label(stats,text="0",font="Helvetica 8 bold")
periodic.grid(row=2,column=1,sticky=tk.E)

difference = ttk.Label(stats,text="(0.00%)",font="Helvetica 8 bold")
difference.grid(row=2,column=2,sticky=tk.W)

stats.grid(row=0,column=0,sticky=tk.NSEW,padx=(20,0),pady=5)
stats.grid_propagate(False)

# Graphs frame
graphs = ttk.LabelFrame(layer_frames,text="Graphs")

ttk.Button(graphs,text="Periodic IC",command=lambda: icgraph(global_cipher.clean()),width=20).grid(row=0,column=0,sticky=tk.W)
ttk.Button(graphs,text="Monogram Frequency",command=lambda: freqanalysis(global_cipher.clean()),width=20).grid(row=1,column=0,pady=5,sticky=tk.W)

graphs.grid(row=0,column=1,sticky=tk.NSEW,padx=10,pady=5)

layer_frames.grid(row=3,column=1,columnspan=10,sticky=tk.EW)

#Decrypted Text output
ttk.Label(master,text="Decrypted Text").grid(row=4,column=1,columnspan=10,pady=5)
scrollbar2 = ttk.Scrollbar(master)
scrollbar2.grid(row=5,column=2,sticky=tk.NSEW)

cipher_output = tk.Text(master, wrap=tk.WORD, yscrollcommand=scrollbar2.set,height=5,width=80)
cipher_output.grid(row=5,column=1,padx=(20,0))

scrollbar2.config(command=cipher_output.yview)
pbprogress = tk.IntVar(master)
pb = ttk.Progressbar(master, orient="horizontal",length=644, variable=pbprogress, mode="determinate")
pb.grid(row=6,column=1,pady=5,padx=(20,0),sticky=tk.W)

# Statistics after decryption
final_layer = tk.Frame(master)

decryptionstats = ttk.LabelFrame(final_layer,text="Results",width=134)
decryptionstats.grid(row=0,column=3,sticky=tk.NSEW,padx=5)
decryptionstats.grid_propagate(False)
ttk.Label(decryptionstats,text="Keys Tested",font="Helvetica 9 bold",anchor=tk.CENTER).grid(row=0,column=0,sticky="ew",padx=5,pady=(2.5,0))
keystested = ttk.Label(decryptionstats,text="0",font="Helvetica 12",anchor=tk.CENTER)
keystested.grid(row=1,column=0,sticky="ew",padx=5,pady=5)
ttk.Label(decryptionstats,text="Best Fitness",font="Helvetica 9 bold",anchor=tk.CENTER).grid(row=2,column=0,sticky="ew",padx=5,pady=(2.5,0))
bestfitness = ttk.Label(decryptionstats,text="0",font="Helvetica 12",anchor=tk.CENTER)
bestfitness.grid(row=3,column=0,sticky="ew",padx=5,pady=5)
ttk.Label(decryptionstats,text="Best Key",font="Helvetica 9 bold",anchor=tk.CENTER).grid(row=4,column=0,sticky="ew",padx=5,pady=(2.5,0))
bestkey = ttk.Label(decryptionstats,text="-",font="Helvetica 9",anchor=tk.CENTER)
bestkey.grid(row=5,column=0,sticky="ew",padx=5,pady=5)

top_10_keys = ttk.LabelFrame(final_layer,text="Top Keys",height=250,width=180)
keys_top = {}
for i in range(10):
    ttk.Label(top_10_keys,text=str(i+1) + ".").grid(row=i,column=0)
    keys_top[i] = ttk.Label(top_10_keys,text="",font="Courier 10")
    keys_top[i].grid(row=i,column=1,sticky=tk.NW)

top_10_keys.grid(row=0,column=0,sticky=tk.NW,padx=5)
top_10_keys.grid_propagate(False)

# Decryption options frame
decryptionconfig = ttk.LabelFrame(final_layer,text="Decryption",width=300,height=50)
decryptionconfig.grid(row=0,column=2,sticky=tk.NSEW,padx=5)
decryptionconfig.grid_propagate(False)
selected_cipher = tk.StringVar(decryptionconfig)
ttk.Label(decryptionconfig,text="Cipher Type",font="Helvetica 9 bold").grid(row=1,column=0,sticky=tk.W,padx=5,pady=(5,0))
cipher_list = ttk.OptionMenu(decryptionconfig, selected_cipher, "Vigenere", "Vigenere", "Beaufort", "Caesar","Polybius")
cipher_list.grid(row=1,column=1,padx=5,sticky="ew")
cipher_list.grid_propagate(False)

# # Slider for Hill ciphers
# scaleholder = tk.Frame(decryptionconfig)
# scaleholder.grid(row=2,columnspan=10)
# scale_var = tk.DoubleVar(scaleholder)
# scale = ttk.Scale(scaleholder, orient=tk.HORIZONTAL, length=200, from_=2, to=15, variable=scale_var)
# scale.grid(row=0, column=0, pady=5)
# scale_label = ttk.Label(scaleholder, text=str(round(scale_var.get())))
# scale_label.grid(row=0, column=1, padx=10)



v = tk.IntVar(decryptionconfig)

ttk.Label(decryptionconfig,text="Cipher Layers",font="Helvetica 9 bold").grid(row=0,column=0,sticky=tk.W,padx=5)
layer_selection_single = ttk.Radiobutton(decryptionconfig,text="Single",command=lambda: set_cipherselection(v,cipher_list),variable=v,value=1,state="normal")
layer_selection_single.grid(row=0,column=1,padx=(5,0),sticky=tk.W)
layer_selection_single.invoke()
ttk.Radiobutton(decryptionconfig, text="Double",command=lambda: set_cipherselection(v,cipher_list), variable=v, value=2).grid(row=0, column=1,sticky=tk.W,pady=5,padx=(70,0))

selected_period = tk.StringVar(decryptionconfig)

key = ttk.Entry(decryptionconfig,text="key")
key.grid(row=3,column=1,padx=5,sticky="ew")
ttk.Label(decryptionconfig,text="Key (Optional)",font="Helvetica 9 bold").grid(row=3,column=0,sticky=tk.W,padx=5,pady=10)

ttk.Label(decryptionconfig,text="Period (Optional)",font="Helvetica 9 bold").grid(row=4,column=0,sticky=tk.W,padx=5)
period_selection = ttk.OptionMenu(decryptionconfig,selected_period,"-","-","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15")
period_selection.grid(row=4,column=1,sticky="ew",padx=5)

#Solve Button
stop = False
ttk.Button(decryptionconfig,text="SOLVE",command=lambda: solve_cipher(selected_cipher.get(),pbprogress)).grid(row=5,column=0,columnspan=2,padx=5,pady=(10,0),sticky=tk.NSEW)
stopper = ttk.Button(decryptionconfig, text="STOP",command=lambda: stop_cipher(pbprogress),state=tk.DISABLED)
stopper.grid(row=6, column=0, columnspan=2,padx=5, pady=5,sticky=tk.NSEW)

final_layer.grid(row=7,column=1,sticky=tk.NW,pady=5,padx=(20,0))

# def ctext_class.restore(text):
#     text = list(text)
#     for i in range(len(nonalphabetic)):
#         text.insert(nonalphabetic[i][1], nonalphabetic[i][0])
#     for i in range(len(case)):
#         text[case[i]] = text[case[i]].lower()
#     return "".join(text)





# Decryption button action


def crack_vigenere(ctext_class):
    ctext = ctext_class.clean()
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
                    cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.vigenere(ctext, best_key)))
                    cipher_output.update()
                count += 1
                keystested.config(text=str(count))
                pbprogress.set(int((count/3120)*100))
                pb.update()
            parentkey = best_starter

def crack_beaufort(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()
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
                    cipher_output.insert(tk.INSERT,ctext_class.restore(decrypt.vigenere(ctext, best_key)))
                    cipher_output.update()
                count += 1
                keystested.config(text=str(count))
                pbprogress.set(int((count/3120)*100))
                pb.update()
            parentkey = best_starter

def crack_caesar(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()
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
    cipher_output.insert(tk.INSERT,ctext_class.restore(decrypted))
    cipher_output.update()

def crack_coltrans(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()

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
                cipher_output.insert(tk.INSERT, ctext_class.restore(deciphered))
                cipher_output.update()
            count += 1
            pbprogress.set(round((count/5912)*100))
            pb.update()
            keystested.config(text=str(count))

def crack_polybius(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()
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
            cipher_output.insert(tk.INSERT, ctext_class.restore(best_decryption))
            cipher_output.update()
        count += 1
        keystested.config(text=str(count))
        pbprogress.set(round((count/maxkeys)*100))
        pb.update()

def crack_2x2hill(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()
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
        cipher_output.insert(tk.INSERT, ctext_class.restore("".join(current_decryption)))
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
            complete = ctext_class.restore(decry1[:-1])
        else:
            complete = ctext_class.restore(decry1)
        cipher_output.insert(tk.INSERT, complete)
        cipher_output.update()
        keys_top[0].config(text=key1)
        keys_top[1].config(text=key2)
    else:
        cipher_output.delete('1.0', tk.END)
        if padded == 1:
            complete = ctext_class.restore(decry2[:-1])
        else:
            complete = ctext_class.restore(decry2)
        cipher_output.insert(tk.INSERT, complete)
        cipher_output.update()
        keys_top[0].config(text=key2)
        keys_top[1].config(text=key1)

def crack_3x3hill(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()
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
        cipher_output.insert(tk.INSERT, ctext_class.restore("".join(current_decryption)))
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
                complete = ctext_class.restore(decry[x][:-1])
            elif padded == 2:
                complete = ctext_class.restore(decry[x][:-2])
            else:
                complete = ctext_class.restore(decry[x])
            cipher_output.delete('1.0', tk.END)
            cipher_output.insert(tk.INSERT, complete)
            cipher_output.update()
        keys_top[i].config(text=keylist[x],font="Courier 7")
        if i != 5:
            s.remove(max(s))

def crack_substitution(ctext,pbprogress):

    ctext_class = ctext
    ctext = ctext_class.clean()
    stopper.config(state=tk.NORMAL)
    global stop
    stop = False
    pb.config(mode='indeterminate')
    pb.start()

    alleles = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    chromosome = ["" for x in range(10)]

    for i in range(10):
        chromosome[i] = alleles[:]
        random.shuffle(chromosome[i])


    while True:
        #Generate Chromosomes

        scores = []
        for i in range(10):
            print("")
            print(decrypt.substitution(ctext,chromosome[i]))
            scores.append(fitness.score(decrypt.substitution(ctext,chromosome[i])))

        parents = []
        for i in range(6):
            best = scores.index(max(scores))
            scores.remove(max(scores))
            parents.append(chromosome[best])

        #Position-Based-Crossover (PBX)
        for i in range(0,5,2):
            y = []
            child = ["" for j in range(26)]

            for k in range(12):
                k = random.randint(0,25)
                child[k] = parents[i][k][:]

            for l in range(26):
                if parents[i+1][l] not in child:
                    y.append(parents[i+1][l])

            for m in range(26):
                if len(child[m]) == 26:
                    break
                if child[m] == "":
                    child[m] = y[0][:]
                    y.remove(child[m])

            chromosome.append(child)

        mutation_top_six = random.randint(0,5)
        a = random.randint(0,25)
        b = random.randint(0,25)
        pos = chromosome.index(parents[mutation_top_six])
        chromosome.append(chromosome[pos][:])
        chromosome[-1][a],chromosome[-1][b] = chromosome[-1][b],chromosome[-1][a]

        pos = scores.index(min(scores))
        a = random.randint(0,25)
        b = random.randint(0,25)
        chromosome.append(chromosome[pos][:])
        chromosome[-1][a], chromosome[-1][b] = chromosome[-1][b], chromosome[-1][a]

        scores = []
        for i in range(15):
            scores.append(fitness.score(decrypt.substitution(ctext,chromosome[i])))

        best_chromosome = []
        for i in range(10):
            best = scores.index(max(scores))
            scores.remove(max(scores))
            best_chromosome.append(chromosome[best])

        chromosome = best_chromosome[:]

        if stop == True:
            break


    # ctext_class = ctext
    # ctext = ctext_class.clean()
    # stopper.config(state=tk.NORMAL)
    # global stop
    # stop = False
    # pb.config(mode='indeterminate')
    # pb.start()
    # tested = 0
    # maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    # maxscore = -99e9
    # parentscore, parentkey = maxscore, maxkey[:]
    # # keep going until we are killed by the user
    # i = 0
    # while True:
    #     i += 1
    #     random.shuffle(parentkey)
    #     deciphered = decrypt.substitution(ctext,parentkey)
    #     parentscore = fitness.score(deciphered)
    #     count = 0
    #     while count < 1000:
    #         pb.update()
    #         a = random.randint(0, 25)
    #         b = random.randint(0, 25)
    #         child = parentkey[:]
    #         # swap two characters in the child
    #         child[a], child[b] = child[b], child[a]
    #         deciphered = decrypt.substitution(ctext,child)
    #         score = fitness.score(deciphered)
    #         # if the child was better, replace the parent with it
    #         if score > parentscore:
    #             parentscore = score
    #             parentkey = child[:]
    #             count = 0
    #         count = count + 1
    #         tested += 1
    #         keystested.config(text=str(tested))
    #         if stop == True: break
    #     # keep track of best score seen so far
    #     if parentscore > maxscore:
    #         maxscore, maxkey = parentscore, parentkey[:]
    #         bestfitness.config(text=str(round(maxscore)))
    #         current_keys = []
    #         for i in range(10):
    #             current_keys.append(keys_top[i].cget('text'))
    #         current_keys = current_keys[:-1]
    #         for i in range(1,10):
    #             keys_top[i].config(text=current_keys[i-1])
    #         keys_top[0].config(text="".join(maxkey)[:15])
    #         ss = decrypt.substitution(ctext,maxkey)
    #         cipher_output.delete('1.0', tk.END)
    #         cipher_output.insert(tk.INSERT, ctext_class.restore(ss))
    #         cipher_output.update()
    #     if stop == True: break
    # stopper.config(state=tk.DISABLED)
    # pb.stop()
    # pb.config(mode='determinate')
    # pb.update()

def crack_vigenere_affine(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()
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
                        cipher_output.insert(tk.INSERT, ctext_class.restore(decrypt.vigenereaffine(ctext, best_key, best_a)))
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
                cipher_output.insert(tk.INSERT, ctext_class.restore(decrypt.vigenereaffine(ctext, actualkey, best_a)))
                cipher_output.update()
            count += 1
            keystested.config(text=str(count))
            pbprogress.set(round((count/len(coprime_26))*100))
            pb.update()

def crack_vigenere_scytale(ctext,pbprogress):
    ctext_class = ctext
    ctext = ctext_class.clean()
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
        for keylength in range(1, 16): # Set to 16 down from 21 for efficiency
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
            cipher_output.insert(tk.INSERT, ctext_class.restore(decrypt.vigenere(cipher,best_key)))
            cipher_output.update()
    stopper.config(state=tk.DISABLED)
    pb.stop()
    pb.config(mode='determinate')
    pb.update()


master.mainloop()