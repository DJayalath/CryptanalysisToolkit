import random
import decrypt
from analyse import quadgram_score

fitness = quadgram_score()

NUM_CHROMOSOMES = 12
NUM_TOP_CHROMOSOMES = 7
NUM_TOP_MUTATIONS = 2
NUM_BOTTOM_MUTATIONS = 2

ctext = """UGXXVBGXVGBTHQQRTKRFNQRKNYKCHZUGTPRYRRFGZCHXNRXGYFTURKUCHQUKVCHBNQUKARNYKRXRTKRFNYSCNYNYQHTURXTCHXZRTUGORZCYENXBRFKUGKKURACCLNTARNYQUHYKRFAVGYNIIRQGIEHYFXGNTNYQQXCHMYGBRFBNFGTPUNZUUGTARRYGTTCZNGKRFPNKUTRORXGIKRXXCXYRKPCXLTNYKURIGTKERPVRGXTBGXVGBUGTKXGORIIRFKCNTKGYAHIECIICPNYQGIRGFCYKURAHVRXNYKURUCMRPRZGYTZGXRKURBCEEAHKNEKUGKFCRTYKPCXLKURYPRPNIIYRRFKCENYFKURXRTKCEKURACCLZUGMKRXTARECXRBNFGTFCPRGXRACKUUCMNYQVCHXFNGXVNTZIRGXARZGHTRNENGBXNQUKPRPNIIUGORGYCKURXKUXRRMIGZRTKCONTNKGEKRXKUNTCYRGYFNGBYCKTHXRUCPICYQNKPNIIKGLRNENYNTURFBVPCXLCYKURKUNXFZUGMKRXCEKGZNKHTTBCYCQXGMUPUNZUNECHYFCYXUCFRTNKPGTZCYZRGIRFNYGIGXQRTKCYRINYKRIARGXNYQGYNBGQRCEGXCTRKURTVBACICEKURZCYTCXKCEKURTHYQCFURINCTNYKXNQHNYQIVXUCFRTNTGITCLYCPYGTKURNTIGYFCEKURLYNQUKTYGBRFGEKRXKURLYNQUKTCETGNYKSCUYCESRXHTGIRBGYFKURZIHRGKKURRYFCEZUGMKRXKUXRRMCNYKRFKCGYCKURXUCBRCEKURLYNQUKTGKACFXHBTCNKXGORIIRFKURXRGYFPGTYCKKCCTHXMXNTRFKCENYFZUGMKRXECHXZCYZRGIRFNYKURXRBGNYTCEKURNXECXKNPGTUCPRORXGTKCYNTURFAVKURKRJKNKKCCLBRGPUNIRKCZXGZLNKGTNFNFYKXRZCQYNTRKURRYZXVMKNCYGTGYVKUNYQZIGTTNZGIPURYNENYGIIVAXCLRNKNFNTZCORXRFKUGKKGZNKHTUGFHTRFGZNMURXKUGKPRKUCHQUKUGFARRYNYORYKRFNYTNJKRRYKUZRYKHXVEXGYZRNKTRRBTKUGKKURNBMRXNGIZNMURXTZUCCIPRXRBHZUBCXRGFOGYZRFKUGYPRUGFGYVXRGTCYKCRJMRZKNEZCHXNRXFHKVNTYKRJZNKNYQRYCHQUECXVCHMRXUGMTKURZUGYZRKCFNTZCORXBCXRNBMRXNGIZNMURXTPNIIARKURZIHRGKKURRYFCEKUNTZUGMKRXNTORXVTHQQRTKNORGYFNUGORACHQUKGKNZLRKKCTRIZHLKCNYORTKNQGKRNGBMXRKKVTHXRNPGTECIICPRFKCKURKNZLRKCEENZRNEVCHZGYZCBRKURYPRYRRFVCHKCFXCMAVKURAXNKNTUBHTRHBARECXRVCHZCBRCHKNKUNYLKURXRNTTCBRKUNYQKURXRKUGKPRYRRFGYFPNIITRYFGBRTTGQRKCBVZCYKGZKNYXCCBKPRYKVKPCKRIINYQKURBKCRJMRZKVCHGYFAXNRENYQKURBCYPUGKKCICCLCHKECXNKPCHIFARQCCFNEVCHZCHIFARORXVFNTZXRRKGACHKKUGKAHKBGLRGTBHZUEHTTGTVCHINLRGACHKBRRKNYQBRNYTRIZHLNPNIIRJMIGNYIGKRXGIIKURARTKSCFNR"""
ctext = ctext[:len(ctext)//2]
alleles = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Random initial generation
chromosome = []
for i in range(NUM_CHROMOSOMES):
    chromosome.append(alleles[:])
    random.shuffle(chromosome[i])

generation = 1
previous = 0
while True:

    # Score the new generation
    scores = []
    for i in range(NUM_CHROMOSOMES):
        scores.append(fitness.score(decrypt.substitution(ctext, chromosome[i])))

    scores_original = scores[:]

    # Select NUM_TOP_CHROMOSOMES for breeding
    parents = []
    for i in range(NUM_TOP_CHROMOSOMES):
        best = scores.index(max(scores))
        scores.remove(max(scores))
        parents.append(chromosome[best])

    # Position-Based-Crossover (PBX) of top chromosomes
    for i in range(0, NUM_TOP_CHROMOSOMES-1, 2):
        y = []
        child = ["" for j in range(26)]

        for k in range(13):
            k = random.randint(0, 25)
            child[k] = parents[i][k][:]

        for l in range(26):
            if parents[i + 1][l] not in child:
                new_pos = child.index("")
                child[new_pos] = parents[i + 1][l]

        chromosome.append(child)

    for i in range(NUM_TOP_MUTATIONS):
        mutation = random.randint(0, NUM_TOP_CHROMOSOMES-1)
        a = random.randint(0, 25)
        b = random.randint(0, 25)
        pos = chromosome.index(parents[mutation])
        chromosome.append(chromosome[pos][:])
        chromosome[-1][a], chromosome[-1][b] = chromosome[-1][b], chromosome[-1][a]

    non_parents = []
    for i in range(NUM_CHROMOSOMES-NUM_TOP_CHROMOSOMES):
        worst = scores_original.index(min(scores_original))
        scores_original.remove(min(scores_original))
        non_parents.append(chromosome[worst])

    for i in range(NUM_BOTTOM_MUTATIONS):
        mutation = random.randint(0,NUM_CHROMOSOMES-NUM_TOP_CHROMOSOMES-1)
        a = random.randint(0, 25)
        b = random.randint(0, 25)
        pos = chromosome.index(non_parents[mutation])
        chromosome.append(chromosome[pos][:])
        chromosome[-1][a], chromosome[-1][b] = chromosome[-1][b], chromosome[-1][a]

    scores = []
    decryptions = []
    for i in range(NUM_CHROMOSOMES+NUM_BOTTOM_MUTATIONS+NUM_TOP_MUTATIONS+(NUM_TOP_CHROMOSOMES//2)):
        decryptions.append(decrypt.substitution(ctext,chromosome[i]))
        scores.append(fitness.score(decryptions[-1]))

    best_chromosome = []
    for i in range(NUM_CHROMOSOMES):
        maximum = max(scores)
        best = scores.index(maximum)
        if i == 0:
            if maximum != previous:
                previous = maximum
                print("Generation",generation)
                print("Score",maximum)
                print(decryptions[best])
        scores.remove(maximum)
        best_chromosome.append(chromosome[best])

    chromosome = best_chromosome[:]
    generation += 1
