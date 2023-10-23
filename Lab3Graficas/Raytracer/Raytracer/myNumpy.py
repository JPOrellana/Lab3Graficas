from math import acos, asin, isclose, sqrt

#------------------------------------------------------------------------------------------------------
def barycentricCoords(A, B, C, P):

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    if areaABC == 0:
        return None

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC


    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return (-1,-1,-1)
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def matrix_multiplier(matrixA, matrixB):

    result = [[sum(a * b for a, b in zip(rowA, colB)) for colB in zip(*matrixB)] for rowA in matrixA]
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def matrix_vector_multiplier(matrix, vector):

    result = [sum(a * b for a, b in zip(row, vector)) for row in matrix]
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def identity_matrix(n):

    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
#------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------
def inverse_matrix(matrix):

    n = len(matrix)
    augmented_matrix = [[matrix[i][j] for j in range(n)] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = augmented_matrix[i][i]
        for j in range(2 * n):
            augmented_matrix[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(2 * n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    inverse = [augmented_matrix[i][n:] for i in range(n)]
    return inverse
#----------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------
def cross_product(vecA, vecB):

    result = [vecA[1] * vecB[2] - vecA[2] * vecB[1], vecA[2] * vecB[0] - vecA[0] * vecB[2], vecA[0] * vecB[1] - vecA[1] * vecB[0]]
    return result
#-----------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------

def vector_normalize(vector):

    magnitude = sqrt(sum(component ** 2 for component in vector))
    normalized_vector = [component / magnitude for component in vector]
    return normalized_vector
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def vector_magnitude(vector):
    magnitude = sqrt(sum(component ** 2 for component in vector))
    return magnitude
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def subtract_vector(vectorA, vectorB):

    result = [a - b for a, b in zip(vectorA, vectorB)]
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def add_vector(vectorA, vectorB):

    result = [a + b for a, b in zip(vectorA, vectorB)]
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def dot_product(A, B):

    result = sum(a * b for a, b in zip(A, B))
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def vector_scalar_mult(scalar, vector):

    result = [component * scalar for component in vector]
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def vector_scalar_div(scalar, vector):

    result = [component / scalar for component in vector]
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def reflectVector(normal, direction):
    reflect = [2 * (a * b) for a, b in zip(direction, normal)]
    result = subtract_vector(reflect, direction)
    result = vector_normalize(result)
    return result
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def refractVector(normal, incident, n1, n2):

    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        normal = vector_scalar_mult(-1, normal)
        n1, n2 = n2, n1
    term1 = add_vector(incident, vector_scalar_mult(c1, normal))
    term2 = vector_scalar_mult((1 - ((n1 / n2) ** 2 * (1 - c1 ** 2)) ** 0.5), normal)
    T = subtract_vector(vector_scalar_mult(n1 / n2, term1), term2)
    T = vector_normalize(T)
    return T
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def totalInternalReflection(normal, incident, n1, n2):

    c1 = dot_product(normal, incident)

    if c1 < -1:
        c1 = -1
    elif c1 > 1:
        c1 = 1

    if c1 < 0:
        c1 = -c1
        n1, n2 = n2, n1

    return acos(c1) >= asin(n2 / n1)
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
def fresnel(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1
    s2 = (n1 * (1 - c1 ** 2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5
    F1 = (((n2 * c1) - (n1 * c2)) / (n2 * c1 + n1 * c2)) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / (n1 * c2 + n2 * c1)) ** 2
    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt
#------------------------------------------------------------------------------------------------------
