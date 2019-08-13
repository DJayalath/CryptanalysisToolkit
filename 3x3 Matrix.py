from sympy import *
import numpy as np

M = []
matrix_labels = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]

rows = 3
cols = 3
result = [[(input("row: %d col: %d  => " % (row, col)))
           for col in range(cols)] for row in range(rows)]
for i in range(3):
    for j in range(3):
        if result[i][j].isdigit():
            result[i][j] = int(result[i][j])

result = Matrix(result)
print("")
print("Input Matrix")
print("")
pprint(result)
print("")

cofactor_matrix = []
count = 0
for i in range(3):
    for j in range(3):
        cofactor_matrix.append(result.minorMatrix(i, j))
        # print("\n%s\n" %(matrix_labels[count]))
        # pprint(result.minorMatrix(i,j))
        # count += 1
cofactor_matrix = Matrix(3, 3, cofactor_matrix)

print("Cofactor Matrices")
print("")
pprint(cofactor_matrix)
print("")

cofactors = []
for i in range(3):
    for j in range(3):
        cofactors.append(result.cofactor(i, j))
cofactors = Matrix(3, 3, cofactors)
print("Cofactor Matrix")
print("")
pprint(cofactors)
result = np.array(result)
cofactors = np.array(cofactors)
print("")
print("Determinant")
print("")
print("%s*%s + %s*%s + %s*%s = %s" % (
result[0][0], cofactors[0][0], result[0][1], cofactors[0][1], result[0][2], cofactors[0][2], Matrix(result).det()))
print("")
print("Inverse")
print("")
pprint((1 / Matrix(result).det()) * Matrix(cofactors).T)

# for i in range(9):
#   M.append((input("%s: " %(matrix_labels[i]))))

# cofactor_matrix = [[0 for i in range(3)] for j in range(3)]
# cofactors = []
# cofactors.append([[M[4],M[5]],[M[7],M[8]]])
# cofactors.append(([[M[3],M[5]],[M[6],M[8]]]))
# cofactors.append(([[M[3],M[4]],[M[6],M[7]]]))
# cofactors.append(([[M[1],M[2]],[M[7],M[8]]]))
# cofactors.append(([[M[0],M[2]],[M[6],M[8]]]))
# cofactors.append(([[M[0],M[1]],[M[6],M[7]]]))
# cofactors.append(([[M[1],M[2]],[M[4],M[5]]]))
# cofactors.append(([[M[0],M[2]],[M[3],M[5]]]))
# cofactors.append(([[M[0],M[1]],[M[3],M[4]]]))