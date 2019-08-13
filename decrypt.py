import numpy as np

def caesar(ctext,shift):

    # t = (c - k) % m // t = plaintext , c = ciphertext , k = shift(n) , m = alphabet length
    int_deciphered = []
    for letter in ctext:
        int_deciphered.append(((ord(letter)-65) - shift) % 26)
    
    # Convert integers into letters
    str_deciphered = []
    for t in int_deciphered:
        str_deciphered.append(chr(t+65))
    
    return "".join(str_deciphered)

def atbash(ctext):
  
    # t = (c - 25) * -1 // t = plaintext , c = ciphertext
    str_deciphered = []
    for c in ctext:
        str_deciphered.append(chr(((ord(c)-65)-25)*(-1)+65))
    
    return "".join(str_deciphered)

def affine(ctext,a,b):

    # Find multiplicative inverse of a
    for z in range(1,26):
        if (a*z) % 26 == 1:
            a_inverse = z
    
    # t = ((c-b)*a^-1) % m // t = plaintext , c = ciphertext , a^-1 = multiplicative inverse of a , m = alphabet length
    int_deciphered = []
    for letter in ctext:
        int_deciphered.append((((ord(letter) - 65) - b)*a_inverse) % 26)

    # Convert integers into characters
    str_deciphered = []
    for t in int_deciphered:
        str_deciphered.append(chr(t+65))
    
    return "".join(str_deciphered)

def substitution(ctext,key):
    
    # Convert key into integers
    int_key = []
    for letter in key:
        int_key.append(ord(letter)-65)
    
    # Find letter in key and replace with position in standard alphabet
    str_deciphered = []
    for letter in ctext:
        str_deciphered.append(chr(int_key.index(ord(letter)-65)+65))
    
    return "".join(str_deciphered)

def vigenere(ctext,key):
    
    # Get integer position of ciphertext characters in alphabet
    int_key = []
    for k in key:
        int_key.append(ord(k)-65)

    # Decode each letter as a caesar cipher using ctext and integer of key as the shift
    str_deciphered = []
    for c in range(len(ctext)):
        str_deciphered.append(caesar(ctext[c],int_key[c % len(int_key)]))
    
    return "".join(str_deciphered)

def vigenereaffine(ctext,key,a):
    
    # Decode each letter as an affine cipher using a, b as the value of the key character, and each letter
    str_deciphered = []
    for t in range(len(ctext)):
        str_deciphered.append(affine(ctext[t],a,ord(key[t % len(key)])-65))
    
    return "".join(str_deciphered)

def bifid(ctext,key,period):
    
    rows,columns = [],[]
    for i in range(0,len(ctext),period):
        num_seq = []
        for j in range(period):
            if i+j < len(ctext):
                num_seq.append(int(key.index(ctext[i+j]) / 5))
                num_seq.append(int(key.index(ctext[i+j]) % 5))
            
        rows.extend(num_seq[0:int(len(num_seq)/2)])
        columns.extend(num_seq[int(len(num_seq)/2):])
    
    deciphered = ""
    for i in range(len(rows)):
        deciphered += key[rows[i]*5 + columns[i]]
    
    return deciphered

def hill2x2(ctext,mat_key):
    
    # Build 2x2 matrix from decryption key
    matrix_key = np.reshape(np.array([int(i) for i in mat_key.split(" ")]),[2,2])
    
    # Get letter pairs
    individual_vectors = [ctext[i:i+2] for i in range(0, len(ctext), 2)]
    
    result = ""
    for i in range(len(individual_vectors)):
    
        # Convert letter pairs into vectors
        vector = [[ord(individual_vectors[i][0])-65],[ord(individual_vectors[i][1])-65]]

        # Multiply matrix key by letter pair vector
        multiplied_matrix = np.mod(np.dot(matrix_key,np.array(vector)),26)
        
        result += chr(multiplied_matrix[0][0]+65) + chr(multiplied_matrix[1][0]+65)
    
    return result

def hill3x3(ctext,mat_key):

    # Build 3x3 matrix from decryption key
    matrix_key = np.reshape(np.array([int(i) for i in mat_key.split(" ")]),[3,3])
    
    # Get letter triplets
    individual_vectors = [ctext[i:i+3] for i in range(0, len(ctext), 3)]
    
    result = ""
    for i in range(len(individual_vectors)):
    
        # Convert letter triplets into vectors
        vector = [[ord(individual_vectors[i][0])-65],[ord(individual_vectors[i][1])-65],[ord(individual_vectors[i][2])-65]]
        
        # Multiply matrix key by letter triplet vector
        multiplied_matrix = np.mod(np.dot(matrix_key,np.array(vector)),26)
        
        result += chr(multiplied_matrix[0][0]+65) + chr(multiplied_matrix[1][0]+65) + chr(multiplied_matrix[2][0]+65)
    
    return result