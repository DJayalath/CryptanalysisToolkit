from math import log10
from quadgrams import quadgram_list

def chisqr(text):
    
    text = text.upper()
    
    expected = [
        0.08167,
        0.01492,
        0.02782,
        0.04253,
        0.12702,
        0.02228,
        0.02015,
        0.06094,
        0.06966,
        0.00153,
        0.00772,
        0.04025,
        0.02406,
        0.06749,
        0.07507,
        0.01929,
        0.00095,
        0.05987,
        0.06327,
        0.09056,
        0.02758,
        0.00978,
        0.02360,
        0.00150,
        0.01974,
        0.00074
        ]
    
    chi = 0
    for i in range(26):
        chi += (((text.count(chr(i+65)))-(expected[i]*len(text)))**2/(expected[i]*len(text)))
    return chi

def indice_coincidence(text):
    
    text = text.upper()
    
    coincidence = 0
    for i in range(26):
        coincidence = coincidence + text.count(chr(i+65))*(text.count(chr(i+65)) - 1)
    
    indexofcoincidence = coincidence/(len(text)*(len(text) - 1))
    
    return indexofcoincidence

class quadgram_score:
    def __init__(self):
        self.quadgrams = {}
        self.count = []
        self.key = []
        self.N = 4224127912
        for line in quadgram_list():
            key,count = line.split(" ")
            self.quadgrams[key] = log10(float(int(count))/self.N)

    def score(self,ctext):
        score = 0
        quadgrams = self.quadgrams.__getitem__
        self.floor = -11.625737060717677
        for i in range(len(ctext)-3):
            self.current_quadgram = ctext[0+i:4+i]
            if self.current_quadgram in self.quadgrams:
                score += quadgrams(self.current_quadgram)
            else:
                score += self.floor
        return score