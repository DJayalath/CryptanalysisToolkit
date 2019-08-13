import decrypt, process_encryption, random, pycipher, numpy as np
from analyse import quadgram_score, chisqr, indice_coincidence
from itertools import permutations
from quadgrams import quadgram_list
fitness = quadgram_score()

def crack_caesar(ctext):

  shifted = []
  stringsqr = []
  for i in range(26):
    shifted.append(decrypt.caesar(ctext,26-i))
    stringsqr.append(chisqr(shifted[i])) # Calculate Chi^2 Statistics
  
  key = stringsqr.index(min(stringsqr)) # Key will be shift with lowest Chi^2 Statistic
  
  print("\nTYPE: CAESAR")
  print("KEY: " + str(key))
  decrypted = decrypt.caesar(ctext,26-key)
  print(decrypted)
  return process_encryption.restore_punctuation(decrypted)

def crack_polybius(ctext):
    chars = "".join(list(set(ctext)))
    perms = [''.join(p) for p in permutations(chars)]
    best_score = -99e9
    for key in perms:
        deciphered = pycipher.PolybiusSquare("ABCDEFGHIKLMNOPQRSTUVWXYZ",len(chars),key).decipher(ctext)
        score = fitness.score(deciphered)
        if score > best_score:
            best_score = score
            best_decryption = deciphered
    return best_decryption

def crack_beaufort(ctext):
  
  ctext = decrypt.atbash(ctext)
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  best_overall = -99e9
  for keylength in range(1,21):
      parentkey = "A"*keylength
      parentscore = fitness.score(decrypt.vigenere(ctext,parentkey))
      parentkey = list(parentkey)
      best_starter_score = parentscore
      best_starter = "".join(parentkey)
      for i in range(keylength):
          for letter in alphabet:
              parentkey = list(parentkey)
              child = parentkey
              child[i] = letter
              child = "".join(child)
              childscore = fitness.score(decrypt.vigenere(ctext,child))
              if childscore > best_starter_score:
                  best_starter_score = childscore
                  best_starter = child
              if childscore > best_overall:
                  best_overall = childscore
                  best_key = child
                  print("\nTYPE: BEAUFORT")
                  print("KEY: %s" %(decrypt.atbash(best_key)))
                  print(decrypt.vigenere(ctext,best_key))
          parentkey = best_starter
  return process_encryption.restore_punctuation(decrypt.vigenere(ctext,best_key))

def crack_vigenere(ctext):
    
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  best_overall = -99e9
  print(ctext)

  for keylength in range(1,21):
      parentkey = "A"*keylength
      parentscore = fitness.score(decrypt.vigenere(ctext,parentkey))
      parentkey = list(parentkey)
      best_starter_score = parentscore
      best_starter = "".join(parentkey)
      for i in range(keylength):
          for letter in alphabet:
              parentkey = list(parentkey)
              child = parentkey
              child[i] = letter
              child = "".join(child)
              childscore = fitness.score(decrypt.vigenere(ctext,child))
              if childscore > best_starter_score:
                  best_starter_score = childscore
                  best_starter = child
              if childscore > best_overall:
                  best_overall = childscore
                  best_key = child
                  print("\nTYPE: VIGENERE (CAESAR)")
                  print("KEY: %s" %(best_key))
                  print(decrypt.vigenere(ctext,best_key))
          parentkey = best_starter
  return process_encryption.restore_punctuation(decrypt.vigenere(ctext,best_key))

def crack_coltrans(ctext):
  
  alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  max_score = -99*(10**9)
  for i in range(2,8):
      current_alphabet = alphabet[:i]
      current_alphabet = "".join(current_alphabet)
      perms = [''.join(p) for p in permutations(current_alphabet)]
      for j in range(len(perms)):
          deciphered = pycipher.ColTrans(perms[j]).decipher(ctext)
          score = fitness.score(deciphered)
          if score > max_score:
              max_score = score
              bestkey = perms[j]
              print("\nTYPE: COLUMNAR TRANSPOSITION")
              print("KEY: " + str(bestkey))
              print(deciphered)
  return pycipher.ColTrans(bestkey).decipher(ctext)

def crack_porta(ctext):
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  best_overall = -99e9
  
  for keylength in range(1,21):
      parentkey = "A"*keylength
      parentscore = fitness.score(pycipher.Porta(parentkey).decipher(ctext))
      parentkey = list(parentkey)
      best_starter_score = parentscore
      best_starter = "".join(parentkey)
      for i in range(keylength):
          for letter in alphabet:
              parentkey = list(parentkey)
              child = parentkey
              child[i] = letter
              child = "".join(child)
              childscore = fitness.score(pycipher.Porta(child).decipher(ctext))
              if childscore > best_starter_score:
                  best_starter_score = childscore
                  best_starter = child
              if childscore > best_overall:
                  best_overall = childscore
                  best_key = child
                  print("\nKEY: %s" %(best_key))
                  print(pycipher.Porta(best_key).decipher(ctext))
          parentkey = best_starter
  return process_encryption.restore_punctuation(pycipher.Porta(best_key).decipher(ctext))

def crack_substitution(ctext):
  
  key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  
  def score(key,ctext):
      points = fitness.score(decrypt.substitution(ctext,key))
      return points
  
  def shuffle(key):
      a = random.randint(0, len(key)-1)
      b = random.randint(0, len(key)-1)
      a_v = key[a]
      b_v = key[b]
      am = list(key)
      am[b] = a_v
      am[a] = b_v
      return "".join(am)
  
  points = -99e9
  
  max_points = points
  
  t = 1.0
  
  freezing = 0.9997
  
  while t > 0.0001:
      new_key = shuffle(key)
  
      p = score(new_key,ctext)
      if p > points:
          if p > max_points:
              max_points = p
              print("\nTYPE: SUBSTITUTION")
              print("TEMPERATURE:", t,"SCORE:",p)
              print("KEY", new_key)
              print(decrypt.substitution(ctext, new_key,))
          key = new_key
          points = p
  
      else:
          if random.random() < t:
              points = p
              key = new_key
      t *= freezing
  return process_encryption.restore_punctuation(decrypt.substitution(ctext,key))

# def crack_2x2hill(ctext):
#
#   encryptedText = ctext[:]
#   best_score = -99e9
#
#   keyslist = []
#   for line in quadgram_list():
#       key,count = line.split(" ")
#       keyslist.append(key)
#
#   # Calculate decryption keys for each crib
#   for x in range(len(keyslist)):
#
#       crib = keyslist[x]
#       for i in range(len(encryptedText)-3):
#           if i != 0:
#               encryptedText = encryptedText[1:]
#
#           vector_ctext1 = [ord(encryptedText[0]) - 65,ord(encryptedText[1]) - 65]
#           vector_crib1 = [ord(crib[0]) - 65,ord(crib[1]) - 65]
#           vector_ctext2 = [ord(encryptedText[2]) - 65,ord(encryptedText[3]) - 65]
#           vector_crib2 = [ord(crib[2]) - 65,ord(crib[3]) - 65]
#
#           vector_ctext = [[vector_ctext1[0],vector_ctext2[0]],[vector_ctext1[1],vector_ctext2[1]]]
#           vector_crib = [[vector_crib1[0],vector_crib2[0]],[vector_crib1[1],vector_crib2[1]]]
#
#           ctext_d = int(np.linalg.det(vector_ctext) % 26)
#
#           # Get multiplicative inverse of determinant
#           valid = False
#           for i in range(1,26):
#               if (ctext_d*i) % 26 == 1:
#                   d_inverse = i
#                   valid = True
#
#           if valid is True:
#
#               # Calculate adjoint matrix (replace with numpy later)
#               vector_adjugate = [["" for x in range(2)] for y in range(2)]
#               vector_adjugate[0][0] = vector_ctext[1][1]
#               vector_adjugate[0][1] = -(vector_ctext[0][1])
#               vector_adjugate[1][0] = -(vector_ctext[1][0])
#               vector_adjugate[1][1] = vector_ctext[0][0]
#
#               # Adjoint matrix * multiplicative inverse of matrix determinant
#               vector_adjugate = np.dot(vector_adjugate,d_inverse)
#
#               # (Vector of the crib * Adjoint Matrix) modulo 26
#               D_matrix = np.mod(np.dot(vector_crib,vector_adjugate),26)
#
#               D_matrix = list(D_matrix.flat)
#               key = " ".join([str(x) for x in D_matrix])
#               score = fitness.score(decrypt.hill2x2(ctext,key))
#               if score > best_score:
#                   best_key = key
#                   best_score = score
#                   print("\nTYPE: 2*2 HILL MATRIX")
#                   print("CRIB: " + str(crib))
#                   print("MATRIX KEY: " + key)
#                   print(decrypt.hill2x2(ctext,best_key))
#
#   return decrypt.hill2x2(ctext,best_key)
#crack_2x2hill("""SVGFLBCSLUJGEXALYOHAEXMOGRMXSOMACSMMHPCIOQEAOWJOUYEODDPLULLZHASAXPZJSFLDOQKQJDBZYHGGGCHVFXTFXPNMKCVHEAQJULHAWBTFXPVXRDSRAZANVHYMXPPSMUJOEXALEKPLXPHAWBXZVUQZJJJBLZDFKSHAHAYGGVIXFPCFVDGFPLNNLULVMULBUIIXSBGNEXWBIXBPRCSBIOALMIZXXZVUJGCSLBCIPCYCHAOGHLZTJOOBKPCSRIDRWBDBSVAZDFSIMUJOHAWBKPSOGVIXAZPIMAGCLGEXWQLULVMULBOQXZNMBMQHOCZCMJNHHAWAFXFJSRADIFDRGULUUGWBSBXDHLRCIFFXGATAHAMWEAVXNDEXGKFJXPJNDRJODRAHCGAZLVMULBOQBZWBTADRVXYIWQYNCSLGDECSZCXZLZDJGRIXBZWBRHOQVXWUNMAZOQACUGCRYTDRCAYKXYHRMZIOKQNCIXEXHAOCXDYVYIMELUEXHAOCXDYVPLMUSNAPQVMKFJRIKUCWHBPFJTCHWBHAMWJDOBAZLZVXKRSAOCSRXZLZDJQIDRYIEOXGUGEKJIKLCSVUCWTFGGUDDSMJCWEQJBYKREADDRPFLUALGCBZALKRQZCSIAIXRBTEIXLZHRWQRSCSJNDRBDDRYIJOAZLZXZDHJBNDCFSINSCWCIPIMAHAYGGVIXFPCFZCDRGULUUGWBWAIXIXMJYOJBULEOQRUOIAJODREXJTPSWBMINNLBJOMJLBWGDJSOMAKOZXNFLZOWVKUCGNACBCOCJIANUORBLGDRONGNVLULWAYKXYNDYITXJJJBRBPFUNIODBLULZMAANKYQESRMIBDGGUDZGMXKDIKNNYWAZSNHAMWVXMGQIJTVHCIGFSVULUOAPWAOQIBVNAGKRJVBZYHALJJPTHAWBFLNNSMLYCSLBCIBZGFJVULCHWBHAYTUULAWBCSRSXDQWNVYKXYDFRBZWGFWGMMKRCFYTGGRLANKRAUSAANRIDRSJCSLBCIRIXZXWSCMJEKXZRIDRDBFJJOANNJGFPLJODRSCTVPLULLZGCYYALGGRLOQOQGCJIWUWLANIFDRQDYHVLHAEXMPEPIOKDYOZKQIPLJBEXALLXXJDRDJALYHMJFJDRGFBMCOYKDVHAWBHAMWEAVXGGRLEXYMBDMAYTJJJBTVMPDRSJCSLBCIRIXZZCJJMMYKXYNDHAKDVXCGHAXDGATADRMRIKBZRIDRKPGCKGQHOCZKQIVDCFPLDJULXPJOMINNHCWBNSQVKCXYEAQJULZJHAVXWBCFAZLZNDWUMUCJEOFJJTULHASOUPIXHLZCFJVNMJVHLUHAMWEAVXCIGFSVEXERADEOMUHAEXQBWALZVXDHDBLBCIHASOMABJXRWBVNDVPLHAEXOHDRISCFWWTFJVSMACLUIXSRCWPPXZBIMRSCGDEAVXGGRLEXYMJODRWUBQYCMIVYYTEACFWTMXALGMMXQIANRVPFDHDBPLULKRYIXPGHAZOPIXUCTFLZOQACMUHAWBFLNNSMZBIXGRKHEXMPOGCSJHZXZHCISASMOWKXQHALCNIXXZPZDHAAVXEONNDJIKXGSOLMGNHASAYIWDOPIXILYKDBEAQJULIBGCKGBZSRTRKXMINNQLSCMJEKCIVCIOUUCGQIYNCSBPSCVLRRQRCSXJXZTKGIJOHASBIOBIAYALKRACBCOCJIANUOGULUUGWBYGQZEXZVLOAZHAMWEAVXEXALEKJIAUYTAVLZHOSBGFQVADWBWMWADRLUAYALKRACBCOCJIANUOSAVLHPJBIXQVPVKXQHCSMGANHNCDSOXMEPQMKCCIZKKPULMUJOEXCHUGTADRWUJOCFLZZZMAKOZXOWPLULIACIDJZJXKAZEOCISIVXJVHAWBVLKRYMBPHAWYANUBQWEQXJALFXGNNDJGKEEXCYRRHOQICFUOHAMWEAVXYYSBEXQOYNIOIKSWULKRVSDREOFEYIVXBZXPHPTLCFZCCSUSWBGFUSGCRZJDKXQRIXWQLUXZXNSBXWSCMJEKANNJGFPLRZLUIXCJCIBCWBMIHVDRHVADEQJBRBNMMRSCGDHAMWEAVXUOLGMKXEKYWWQCLZVXKRSAYTDRJHJTJOEKHPFEDRIAQBKRVLSACSNNJVIASRSOXMCEQESRDRBJKPXZTOOPMJKHAZRBLTPFDHDBPLULKRYIXPBZJTKXMINNRRMASBGIJOHAYKUNEOMUULIXCSLBCIRIDRNPLUSCCFDBNUZRKSRZIAJBWBUULAWBKDOQAZQJHOUYSVCHUGJJNNNDZCIXGGZWPPYKXYXZXPFJRIQZDRCFDFFEDRHOOTSOHNBQADHNNNJTJVEOMUOPOBWGZXYCWBHAQIMRHROWJTWQYIEODDPLULANRVQHCFHAKQTIMIYCLBSMRRULYMXPPSMUJOQWPLULEXHASAMZDRVXHAMWBZAGBZRIEPOPIXWOSBBPRXJTCIKXADEXZVLOUUCFZPQHCFHAOCTEKZWGDIADVXFJRXDJSOALYHMJFJEAVXANCJDHYKSRGFWGDBLUEAVXNQYKUNPLJOQZDRNTKXQRGEBQADHNNNJTJVRBLGDRGULUUGWBQIMAKQTFWBAGDBBZJIKDZRPWAZLZOQCFMIFBQHOBCIBCANDBLUHAWAFXFJKHIXWBMIHVOQJTHHEXWBAZHAWNKZMIXDHBPFPLXPQYIXAZSAHBDVAZSCULYMHAIXBZBJLGMUJOEBGNHAUUUVADLAKEIXQYIXIXYTKPAZEAVLAOVLUJXZZCDRVXGCEXEOFEDRGULUUGWBSOULPLRZAZLZKHIXWBWAALNVALYHMJFJANTOMRSCGDNPLUEXQOYMXPPSMUJOBZBJLGMUJOVLHPJBIXYSOQHAXDYVRPGCLGEXMMKRVSQZDRFIULMJEXYYRIKUALYHMJFJZTBPJBHAOCJOIXDHWAZRSREAEYANJKADSCMACFZCFXGATAHAWBDRYIQYADEQJBKSHAHAUULXLZZZYKDVGRWAOQVLTKFXZXJBAGDBBZJIOCDLYTPFQCHASBFXTFEAKSJIVNLULVMULBUIALXMADCSFWQIYKFBQIIBHAOCXDYVAPCSLUGCLGEXCIUUSRYXMXSBZRSWRIDRRCQWWFWBWQZCDRKPOGJBSCYTCGEXKWXZZCDRMRIKVHSRDRCNVXBJVXRISFYKRCSOXDKGHAUUUCCOAYTAOQMOHDAPOCWDQZGCEQJBOAVXIBANQVRBLGLZJJBZPIMAHAQIMRHROWJTANHRRRKRLBQILXZCXZPLSRDRNDEMNFIBHAWAKEHAMWXZXPHASACIHNTLGFPLBDPLMUKSHAHASOEPFJKXQHGROQNDCFMZCFRRIKHRJBWUNTQIIBHAQVOBKQJOAQXPZJCIBCIXDRWUUDJKEXHRJDXRHAEXUNQJHBTFRIQZDRGPOGALGGUDDSOCWLIOIARCQVADHAQIMRHROWJTFLNNSMNRFBALYHMJFJLZACRSVXKGHAOCBQADGCPLULALGGUDJKHPSFHAWAKDHAOCPFRSGFCFTXGFMJQIWDQIQYCSYYDJZJXKMINNLUJHADJVJJTOCFDFSIMUJOOSGFPLBDQJHBGFANUOULHLPTACBCOCJIANUOOWMUPFWQLUJJINSAMVOBALUCJODREABTIXCSJIBJLGIBOQSVUUYTAQBDQRYTDREMHAADALKCSEQZACMZUGMIYCOQADLZVNBDQRANUOJHLBYAALRBFBAZHAQIMRHROWJTLZHOQZSOZCDRKBCFUOHAGRAYVTKMLBNFJGMXMJDFSIMUJOSRQMYTVXKRHOQZSOPLULLVMULBEZYHLZGCYYACVXHAOCDVLZZJWUUDVULMQIMGOQDRJXQZDRQDYHLZLXIFWMQIDRANNJGFPLNNWTIKRIOGADMOALTADRGULUUGWBCSLULZWUBDNTVXEXLVMULBOQJDYYTOCSHAANHRHAEXOHDRCAULDHDJAZHAQIMRHROWJTLZFJVDGFPLHIGIJODRXZQCIXWUJISOPLXPRPHOQICFPLJBALOQWOCWLDGVIXRBNMWBQWEPFJKXMINNLTWWJBHAWBHAMWTFAZAZLZCIZCDRHLCILBTFRBLGDRNDXZDHYKPFVSUULAWBQILXDOOGHAKDAYMGQIPLULDFEAYMFVRCUGSNEADFALKSJIZRDJYTDRPJOBANPPGRMXCSVXKRSVANUOIBNQEXCYJBDFYVHAQIMRHROWJTANHRRRWUJIILADWBADIABDOPIXKRGCTTPFHHOSANYPQWHNVXDVEASMUNDBNHCJCSRCYTQZPFUOHAYTUULAWBYTGFWGRRULHAKQHAIXXZLUSNEADFHAWBEAKREOBPYWEQJIEXKJSCMJEKANNJGFPLVLDJYTDRSRADYOMZSXLBKXDRVXSAVLVXOQULRBLGDRZQKGMRHROWJTLZYYSBHAUUKRQHCSLUOPIXSJCSEOJOIOOBCFUOKSDOQICIIADFJOSTOGCHWBUCGNJJPTLXPLHAEXMOCFIKRISFCSTZALTAJJEOXGLBTFHAKQXYJDAPMITFPPKE""")

def crack_2x2hill_alt(ctext):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    combinations = []
    for i in range(26):
        for j in range(26):
                combinations.append([i,j])
    cvectors = []
    for i in range(0,len(ctext),2):
        cvectors.append([alphabet.index(ctext[i]),alphabet.index(ctext[i+1])])
    decryption_score = []
    for combo in combinations:
        current_decryption = []
        for block in cvectors:
            current_decryption.append(chr(((block[0]*combo[0] + block[1]*combo[1]) % 26) + 65))
        decryption_score.append(chisqr("".join(current_decryption)))
    best_1 = combinations[decryption_score.index(min(decryption_score))]
    decryption_score.remove(min(decryption_score))
    best_2 = combinations[decryption_score.index(min(decryption_score))]
    for i in range(2):
        best_1[i] = str(best_1[i])
        best_2[i] = str(best_2[i])
    key1 = " ".join(best_1) + " " + " ".join(best_2)
    key2 = " ".join(best_2) + " " + " ".join(best_1)
    decry1 = decrypt.hill2x2(ctext,key1)
    decry2 = decrypt.hill2x2(ctext,key2)
    s1 = fitness.score(decry1)
    s2 = fitness.score(decry2)
    if s1 > s2:
        print(decry1)
    else:
        print(decry2)

#crack_2x2hill_alt("""SVGFLBCSLUJGEXALYOHAEXMOGRMXSOMACSMMHPCIOQEAOWJOUYEODDPLULLZHASAXPZJSFLDOQKQJDBZYHGGGCHVFXTFXPNMKCVHEAQJULHAWBTFXPVXRDSRAZANVHYMXPPSMUJOEXALEKPLXPHAWBXZVUQZJJJBLZDFKSHAHAYGGVIXFPCFVDGFPLNNLULVMULBUIIXSBGNEXWBIXBPRCSBIOALMIZXXZVUJGCSLBCIPCYCHAOGHLZTJOOBKPCSRIDRWBDBSVAZDFSIMUJOHAWBKPSOGVIXAZPIMAGCLGEXWQLULVMULBOQXZNMBMQHOCZCMJNHHAWAFXFJSRADIFDRGULUUGWBSBXDHLRCIFFXGATAHAMWEAVXNDEXGKFJXPJNDRJODRAHCGAZLVMULBOQBZWBTADRVXYIWQYNCSLGDECSZCXZLZDJGRIXBZWBRHOQVXWUNMAZOQACUGCRYTDRCAYKXYHRMZIOKQNCIXEXHAOCXDYVYIMELUEXHAOCXDYVPLMUSNAPQVMKFJRIKUCWHBPFJTCHWBHAMWJDOBAZLZVXKRSAOCSRXZLZDJQIDRYIEOXGUGEKJIKLCSVUCWTFGGUDDSMJCWEQJBYKREADDRPFLUALGCBZALKRQZCSIAIXRBTEIXLZHRWQRSCSJNDRBDDRYIJOAZLZXZDHJBNDCFSINSCWCIPIMAHAYGGVIXFPCFZCDRGULUUGWBWAIXIXMJYOJBULEOQRUOIAJODREXJTPSWBMINNLBJOMJLBWGDJSOMAKOZXNFLZOWVKUCGNACBCOCJIANUORBLGDRONGNVLULWAYKXYNDYITXJJJBRBPFUNIODBLULZMAANKYQESRMIBDGGUDZGMXKDIKNNYWAZSNHAMWVXMGQIJTVHCIGFSVULUOAPWAOQIBVNAGKRJVBZYHALJJPTHAWBFLNNSMLYCSLBCIBZGFJVULCHWBHAYTUULAWBCSRSXDQWNVYKXYDFRBZWGFWGMMKRCFYTGGRLANKRAUSAANRIDRSJCSLBCIRIXZXWSCMJEKXZRIDRDBFJJOANNJGFPLJODRSCTVPLULLZGCYYALGGRLOQOQGCJIWUWLANIFDRQDYHVLHAEXMPEPIOKDYOZKQIPLJBEXALLXXJDRDJALYHMJFJDRGFBMCOYKDVHAWBHAMWEAVXGGRLEXYMBDMAYTJJJBTVMPDRSJCSLBCIRIXZZCJJMMYKXYNDHAKDVXCGHAXDGATADRMRIKBZRIDRKPGCKGQHOCZKQIVDCFPLDJULXPJOMINNHCWBNSQVKCXYEAQJULZJHAVXWBCFAZLZNDWUMUCJEOFJJTULHASOUPIXHLZCFJVNMJVHLUHAMWEAVXCIGFSVEXERADEOMUHAEXQBWALZVXDHDBLBCIHASOMABJXRWBVNDVPLHAEXOHDRISCFWWTFJVSMACLUIXSRCWPPXZBIMRSCGDEAVXGGRLEXYMJODRWUBQYCMIVYYTEACFWTMXALGMMXQIANRVPFDHDBPLULKRYIXPGHAZOPIXUCTFLZOQACMUHAWBFLNNSMZBIXGRKHEXMPOGCSJHZXZHCISASMOWKXQHALCNIXXZPZDHAAVXEONNDJIKXGSOLMGNHASAYIWDOPIXILYKDBEAQJULIBGCKGBZSRTRKXMINNQLSCMJEKCIVCIOUUCGQIYNCSBPSCVLRRQRCSXJXZTKGIJOHASBIOBIAYALKRACBCOCJIANUOGULUUGWBYGQZEXZVLOAZHAMWEAVXEXALEKJIAUYTAVLZHOSBGFQVADWBWMWADRLUAYALKRACBCOCJIANUOSAVLHPJBIXQVPVKXQHCSMGANHNCDSOXMEPQMKCCIZKKPULMUJOEXCHUGTADRWUJOCFLZZZMAKOZXOWPLULIACIDJZJXKAZEOCISIVXJVHAWBVLKRYMBPHAWYANUBQWEQXJALFXGNNDJGKEEXCYRRHOQICFUOHAMWEAVXYYSBEXQOYNIOIKSWULKRVSDREOFEYIVXBZXPHPTLCFZCCSUSWBGFUSGCRZJDKXQRIXWQLUXZXNSBXWSCMJEKANNJGFPLRZLUIXCJCIBCWBMIHVDRHVADEQJBRBNMMRSCGDHAMWEAVXUOLGMKXEKYWWQCLZVXKRSAYTDRJHJTJOEKHPFEDRIAQBKRVLSACSNNJVIASRSOXMCEQESRDRBJKPXZTOOPMJKHAZRBLTPFDHDBPLULKRYIXPBZJTKXMINNRRMASBGIJOHAYKUNEOMUULIXCSLBCIRIDRNPLUSCCFDBNUZRKSRZIAJBWBUULAWBKDOQAZQJHOUYSVCHUGJJNNNDZCIXGGZWPPYKXYXZXPFJRIQZDRCFDFFEDRHOOTSOHNBQADHNNNJTJVEOMUOPOBWGZXYCWBHAQIMRHROWJTWQYIEODDPLULANRVQHCFHAKQTIMIYCLBSMRRULYMXPPSMUJOQWPLULEXHASAMZDRVXHAMWBZAGBZRIEPOPIXWOSBBPRXJTCIKXADEXZVLOUUCFZPQHCFHAOCTEKZWGDIADVXFJRXDJSOALYHMJFJEAVXANCJDHYKSRGFWGDBLUEAVXNQYKUNPLJOQZDRNTKXQRGEBQADHNNNJTJVRBLGDRGULUUGWBQIMAKQTFWBAGDBBZJIKDZRPWAZLZOQCFMIFBQHOBCIBCANDBLUHAWAFXFJKHIXWBMIHVOQJTHHEXWBAZHAWNKZMIXDHBPFPLXPQYIXAZSAHBDVAZSCULYMHAIXBZBJLGMUJOEBGNHAUUUVADLAKEIXQYIXIXYTKPAZEAVLAOVLUJXZZCDRVXGCEXEOFEDRGULUUGWBSOULPLRZAZLZKHIXWBWAALNVALYHMJFJANTOMRSCGDNPLUEXQOYMXPPSMUJOBZBJLGMUJOVLHPJBIXYSOQHAXDYVRPGCLGEXMMKRVSQZDRFIULMJEXYYRIKUALYHMJFJZTBPJBHAOCJOIXDHWAZRSREAEYANJKADSCMACFZCFXGATAHAWBDRYIQYADEQJBKSHAHAUULXLZZZYKDVGRWAOQVLTKFXZXJBAGDBBZJIOCDLYTPFQCHASBFXTFEAKSJIVNLULVMULBUIALXMADCSFWQIYKFBQIIBHAOCXDYVAPCSLUGCLGEXCIUUSRYXMXSBZRSWRIDRRCQWWFWBWQZCDRKPOGJBSCYTCGEXKWXZZCDRMRIKVHSRDRCNVXBJVXRISFYKRCSOXDKGHAUUUCCOAYTAOQMOHDAPOCWDQZGCEQJBOAVXIBANQVRBLGLZJJBZPIMAHAQIMRHROWJTANHRRRKRLBQILXZCXZPLSRDRNDEMNFIBHAWAKEHAMWXZXPHASACIHNTLGFPLBDPLMUKSHAHASOEPFJKXQHGROQNDCFMZCFRRIKHRJBWUNTQIIBHAQVOBKQJOAQXPZJCIBCIXDRWUUDJKEXHRJDXRHAEXUNQJHBTFRIQZDRGPOGALGGUDDSOCWLIOIARCQVADHAQIMRHROWJTFLNNSMNRFBALYHMJFJLZACRSVXKGHAOCBQADGCPLULALGGUDJKHPSFHAWAKDHAOCPFRSGFCFTXGFMJQIWDQIQYCSYYDJZJXKMINNLUJHADJVJJTOCFDFSIMUJOOSGFPLBDQJHBGFANUOULHLPTACBCOCJIANUOOWMUPFWQLUJJINSAMVOBALUCJODREABTIXCSJIBJLGIBOQSVUUYTAQBDQRYTDREMHAADALKCSEQZACMZUGMIYCOQADLZVNBDQRANUOJHLBYAALRBFBAZHAQIMRHROWJTLZHOQZSOZCDRKBCFUOHAGRAYVTKMLBNFJGMXMJDFSIMUJOSRQMYTVXKRHOQZSOPLULLVMULBEZYHLZGCYYACVXHAOCDVLZZJWUUDVULMQIMGOQDRJXQZDRQDYHLZLXIFWMQIDRANNJGFPLNNWTIKRIOGADMOALTADRGULUUGWBCSLULZWUBDNTVXEXLVMULBOQJDYYTOCSHAANHRHAEXOHDRCAULDHDJAZHAQIMRHROWJTLZFJVDGFPLHIGIJODRXZQCIXWUJISOPLXPRPHOQICFPLJBALOQWOCWLDGVIXRBNMWBQWEPFJKXMINNLTWWJBHAWBHAMWTFAZAZLZCIZCDRHLCILBTFRBLGDRNDXZDHYKPFVSUULAWBQILXDOOGHAKDAYMGQIPLULDFEAYMFVRCUGSNEADFALKSJIZRDJYTDRPJOBANPPGRMXCSVXKRSVANUOIBNQEXCYJBDFYVHAQIMRHROWJTANHRRRWUJIILADWBADIABDOPIXKRGCTTPFHHOSANYPQWHNVXDVEASMUNDBNHCJCSRCYTQZPFUOHAYTUULAWBYTGFWGRRULHAKQHAIXXZLUSNEADFHAWBEAKREOBPYWEQJIEXKJSCMJEKANNJGFPLVLDJYTDRSRADYOMZSXLBKXDRVXSAVLVXOQULRBLGDRZQKGMRHROWJTLZYYSBHAUUKRQHCSLUOPIXSJCSEOJOIOOBCFUOKSDOQICIIADFJOSTOGCHWBUCGNJJPTLXPLHAEXMOCFIKRISFCSTZALTAJJEOXGLBTFHAKQXYJDAPMITFPPKE""")

def crack_3x3hill(ctext):
  
  encryptedText = ctext[:]
  alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  best_score = -99e9
  
  crib = (input("Enter 9-letter crib: ")).upper()
  
  for i in range(len(encryptedText)-8):
      if i != 0:
          encryptedText = encryptedText[1:]
  
      vector_ctext1 = [alphabet.index(encryptedText[0]),alphabet.index(encryptedText[1]),alphabet.index(encryptedText[2])]
      vector_crib1 = [alphabet.index(crib[0]),alphabet.index(crib[1]),alphabet.index(crib[2])]
      vector_ctext2 = [alphabet.index(encryptedText[3]),alphabet.index(encryptedText[4]),alphabet.index(encryptedText[5])]
      vector_crib2 = [alphabet.index(crib[3]),alphabet.index(crib[4]),alphabet.index(crib[5])]
      vector_ctext3 = [alphabet.index(encryptedText[6]),alphabet.index(encryptedText[7]),alphabet.index(encryptedText[8])]
      vector_crib3 = [alphabet.index(crib[6]),alphabet.index(crib[7]),alphabet.index(crib[8])]
      
      vector_ctext = [["" for x in range(3)] for y in range(3)]
      for i in range(3):
          vector_ctext[i][0] = vector_ctext1[i]
          vector_ctext[i][1] = vector_ctext2[i]
          vector_ctext[i][2] = vector_ctext3[i]
      
      vector_crib = [["" for x in range(3)] for y in range(3)]
      for i in range(3):
          vector_crib[i][0] = vector_crib1[i]
          vector_crib[i][1] = vector_crib2[i]
          vector_crib[i][2] = vector_crib3[i]
  
  
      DICT = {}
      counter = 0
      for i in range(3):
          for j in range(3):
              DICT[alphabet[counter]] = vector_ctext[i][j]
              counter += 1
      
      # Formula for determinant of 3x3 matrix: a(ei − fh) − b(di − fg) + c(dh − eg)
      ctext_d = (DICT["A"]*(DICT["E"]*DICT["I"] - DICT["F"]*DICT["H"]) - DICT["B"]*(DICT["D"]*DICT["I"] - DICT["F"]*DICT["G"]) + DICT["C"]*(DICT["D"]*DICT["H"] - DICT["E"]*DICT["G"])) % 26
      
      valid = False
      for i in range(1,26):
          if (ctext_d*i) % 26 == 1:
              d_inverse = i
              valid = True
      
      if valid is True:
          D_M = DICT
          vector_adjugate = [["" for x in range(3)] for y in range(3)]
          # Create Adjugate matrix of the key
          # Calculate Determinant of each 2x2 matrix = ad-bc
          vector_adjugate[0][0] = (D_M["E"]*D_M["I"] - D_M["F"]*D_M["H"])
          vector_adjugate[0][1] = (-(D_M["B"]*D_M["I"] - D_M["C"]*D_M["H"]))
          vector_adjugate[0][2] = (D_M["B"]*D_M["F"] - D_M["C"]*D_M["E"])
          vector_adjugate[1][0] = (-(D_M["D"]*D_M["I"] - D_M["F"]*D_M["G"]))
          vector_adjugate[1][1] = (D_M["A"]*D_M["I"] - D_M["C"]*D_M["G"])
          vector_adjugate[1][2] = (-(D_M["A"]*D_M["F"] - D_M["C"]*D_M["D"]))
          vector_adjugate[2][0] = (D_M["D"]*D_M["H"] - D_M["E"]*D_M["G"])
          vector_adjugate[2][1] = (-(D_M["A"]*D_M["H"] - D_M["B"]*D_M["G"]))
          vector_adjugate[2][2] = (D_M["A"]*D_M["E"] - D_M["B"]*D_M["D"])
          
          for i in range(3):
              for j in range(3):
                  vector_adjugate[i][j] *= d_inverse
                  
          vector_adjugate = np.array(vector_adjugate)
          vector_crib = np.array(vector_crib)
          
          D_matrix = np.dot(vector_crib,vector_adjugate)
          
          for i in range(3):
              for j in range(3):
                  D_matrix[i][j] = D_matrix[i][j] % 26
          
          decry_key = ""
          for i in range(3):
              for j in range(3):
                  if i == 2 and j == 2:
                      decry_key += str(D_matrix[i][j])
                  else:
                      decry_key += (str(D_matrix[i][j]) + " ")
          #D_matrix = decryption key
          score = fitness.score(decrypt.hill3x3(ctext,decry_key))
          #print(encipher_22hill((str(D_matrix[0][0])+ " " + str(D_matrix[0][1]) + " " + str(D_matrix[1][0]) + " " + str(D_matrix[1][1])),ciphertext))
          if score > best_score:
              best_key = decry_key
              best_score = score
              print("\nTYPE: 3*3 HILL MATRIX")
              print("CRIB: " + str(crib))
              print(best_key)
              print(decrypt.hill3x3(ctext,best_key))
  return decrypt.hill3x3(ctext,best_key)
#crack_3x3hill("""MVOPGXJYGOSLCBINFNFYDPPBKHEJBVCKKGKSHBXMGKIUQBHKCOMUPGVXJXQVFYDQBGDNHZSLCIEWFOFZVNXHBUSQXYSZTLPIHAOKCOCJYYKFZRCEVYKVLDCCCNUTCBTUORFQJOCKLDOFKWJYOXTUXBANJQZTWRLENEHBJDTENCFTUORFQJOCFFNFURANNPYBNQQAAOWBOAPLSJMUNRKLTGTTGKKVXJCHXTPOHARGVEXIQVTJTSNGHQYBJONRSZUHJYBXBTOLERMBGFOWIXFQVGHCHBYUESZHFVYNRJTQQKLDVEOPYBNQQIEQYZPIQXATEFHYJDCTBGNKMAFOSHWGVLRFFJLCWGEYPFWPVTHKNLCOWQGODFZPRSCQZAGDWMLWSZHKHQYKFVWSMUKPYBNQQIEQFZVWARGTZOEWECAXVHUILRFDSUBKDIJTDGTZFZVDKJPIEYUEHWFNNPGSIVKCHVYOMAREUNMVKNMOKEBWXMZNNCFYPCMTWWQIDUXYKFRIYRMYZZXPUEOJKFJXEFZFNRXWQEFQXVVUXBNCFMNQGVSHITRFDVXVCUEVGHWPFWOEJBDIYMPIDOAKPGTFZVVEREPGSAGGCRQNUQWQXDVVPKTTIEFQDUXFFNPRRYZXQTIUECHNUTTIFZACNSRCATTNAXZMTKJBDBHKDHEAPGIXTOLQSJSJJUEGILTKLIWPRLUDALMNXFQNCFRUWJRRENARSCWBOVJBXDVVLZKVAQCIYKFZMAUNROHXHOIGVERANVWBPEGCEMMCGQVAEHBQQAVURBWQBWKXVFLEFJTDCFVNCFCFEFWPEPGSAGGCROEWKNRGDWCFVLKSXMYHXSHBLBUSUWOHEWHOIYWKJDEQVNQZAWLGUYYQBJNCFCRSQKUMRONNPBUEKHUJTDOJKUKYZNSGYANFWAZWQHKFYDIFJUXBGVTIAADYXGVEXIQBUEJDLEZTNLMCRLDEWQVHFWSRSTDQIMKCCADURUFOBNLTMOGKVHQTKADAANABZJCISUWLFZPRFDVXVDHEUXBTDBCTKOJYICDIPIKVHUXJVNPFURYKFYMAQBZHOILDZMUKMRQADAKMGGMSHCRTMYEPONCFQXIVERFYDALZGVWBKEFCEDLNKLDXYQPZUALIOXBPUUYLMDADBXBUWFCKOEFSVGHSUBASQWBOLQOTWWJCSMKEHVYGDWDBZNCFCRSGVEXIQVGHSUBYGEREURGFNCFZWDVSWZWHRAWNCFUXIUJSICDRIYECWVKEZMADLNXBLJWLPJLVKFJWLMTIRGTKQZQPIZLGMWEARZGVLTGZENACRPUBLYUEUAIHRHYPRLQCNCFFOEPRWNLMADLRSKKFLICDASQWBOQYYMBBGDWCFVMKEHVYGDWDLZOLDWRWYZXUEQNCFCSGYZDDIUQBTENMFYDIFJFZPPEGJEYWDCUQQNNWUNUHBLORRTBUCBKXYURSCMQCNBBXDVYKFYUEJSJWEOHOHRZXKFQGDPIPCBUQGKMHWLGDPENOVXJEPBBUQXMAUJSSZHRGGGBOAUKWUGVGHROLPBHULAWBOETZGDWRTHFWSWLEZJTCUEAGYFECSPCMLDDLGUFWVXTADIXWKWLMHAUZJXVIVSUBKMUXMGEVYUXZBWQKCOCJYSNNECWGPAZROLUGHOIFQIQECFPRJOGDZDUGKOKQMLWXVE""")

def crack_vigenere_affine(ctext):
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  best_overall = -99e9
  coprime_26 = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23] # Removed 1 and 25 to save time
  
  average = []
  for j in range(2,16):
    sequence = []
    for k in range(j):
      text = list(ctext[k:])
      n = j
      period = int(int(len(text))//int(n))
      output = []
      i=0
      while i < len(text):
        output.append(text[i])
        i = i + int(n)
      phrase = "".join(output)
      sequence.append(indice_coincidence(phrase)) # Calculate each index of coincidence
    average.append(sum(sequence)/len(sequence)) # Calculate average IC for each period
  
  keylength = average.index(max(average)) + 2

  for a in coprime_26:
      parentkey = "A"*keylength
      parentscore = fitness.score(decrypt.vigenereaffine(ctext,parentkey,a))
      parentkey = list(parentkey)
      best_starter_score = parentscore
      best_starter = "".join(parentkey)
      for i in range(keylength):
          for letter in alphabet:
              parentkey = list(parentkey)
              child = parentkey
              child[i] = letter
              child = "".join(child)
              childscore = fitness.score(decrypt.vigenereaffine(ctext,child,a))
              if childscore > best_starter_score:
                  best_starter_score = childscore
                  best_starter = child
              if childscore > best_overall:
                  best_overall = childscore
                  best_key = child
                  best_a = a
                  print("\nTYPE: VIGENERE (AFFINE)")
                  print("KEY: %s" %(best_key))
                  print(decrypt.vigenereaffine(ctext,best_key,a))
          parentkey = best_starter
          
  return process_encryption.restore_punctuation(decrypt.vigenereaffine(ctext,best_key,best_a))

def crack_vigenere_scytale(ctext):
  
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  best_overall = -99e9
  best_scytale = -99e9
  
  for scytale in range(1,11):
      cipher = pycipher.ColTrans(alphabet[0:scytale+1]).decipher(ctext)
      for keylength in range(1,21):
          parentkey = "A"*keylength
          parentscore = fitness.score(decrypt.vigenere(cipher,parentkey))
          parentkey = list(parentkey)
          best_starter_score = parentscore
          best_starter = "".join(parentkey)
          for i in range(keylength):
              for letter in alphabet:
                  parentkey = list(parentkey)
                  child = parentkey
                  child[i] = letter
                  child = "".join(child)
                  childscore = fitness.score(decrypt.vigenere(cipher,child))
                  if childscore > best_starter_score:
                      best_starter_score = childscore
                      best_starter = child
                  if childscore > best_overall:
                      best_overall = childscore
                      best_key = child
              parentkey = best_starter
              
      current_scytale = fitness.score(decrypt.vigenere(cipher,best_key))
      if current_scytale > best_scytale:
          best_scytale = current_scytale
          scytalenum = scytale
          print("\nTYPE: VIGENERE + SCYTALE")
          print("SCYTALE WIDTH: ",str(scytale + 1))
          print("KEY:",str(best_key))
          print(decrypt.vigenere(cipher,best_key))
  return decrypt.vigenere(pycipher.ColTrans(alphabet[0:scytalenum+1]).decipher(ctext),best_key)

def crack_bifid(ctext,period):
  key = 'ABCDEFGHIKLMNOPQRSTUVWXYZ' # J removed!
  
  def shuffle(key):
      a = random.randint(0, len(key)-1)
      b = random.randint(0, len(key)-1)
      rand_1 = key[a]
      rand_2 = key[b]
      shuffled_key = list(key)
      shuffled_key[b] = rand_1
      shuffled_key[a] = rand_2
      return "".join(shuffled_key)
  
  points = -1000000
  
  max_points = points
  
  t = 1.0
  
  freezing = 0.9997
  
  while t > 0.0001:
      new_key = shuffle(key)
      deciphered = decrypt.bifid(ctext,new_key,period)
      p = fitness.score(deciphered)
      if p > points:
          if p > max_points:
              max_points = p
              print("\nTEMPERATURE", t)
              print("POINTS", p)
              print("KEY", new_key)
              print(deciphered)
          key = new_key
          points = p
  
      else:
          if random.random() < t:
              points = p
              key = new_key
      t *= freezing
      
  return decrypt.bifid(ctext,key,period)