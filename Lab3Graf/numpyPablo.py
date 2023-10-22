import math
from math import sqrt
#---------------------------------------------------------
def custom_subtract_vectors(vector1, vector2):
    result = []
    for x, y in zip(vector1, vector2):
        result.append(x - y)
    return result
#---------------------------------------------------------


#---------------------------------------------------------
def custom_ref(normal, direction):

    reflect = 2 * custom_dot_product(normal, direction)
    reflect = [reflect * normal[i] for i in range(3)]
    reflect = custom_subtract_vectors(reflect, direction)
    reflect = custom_vector_normalize(reflect)

    return reflect
#---------------------------------------------------------


#---------------------------------------------------------
def custom_linalg_norm(vector):
    norm = 0
    for x in vector:
        norm += x * x
    return math.sqrt(norm)
#---------------------------------------------------------


#---------------------------------------------------------
def custom_multiply_vector_by_scalar(vector, scalar):
    result = []
    for x in vector:
        result.append(x * scalar)
    return result
#---------------------------------------------------------


#---------------------------------------------------------
def custom_multiply_vectors(vector1, vector2):
    result = []
    for x, y in zip(vector1, vector2):
        result.append(x * y)
    return result
#---------------------------------------------------------


#---------------------------------------------------------
def custom_add_vectors(vector1, vector2):
    result = []
    for x, y in zip(vector1, vector2):
        result.append(x + y)
    return result
#---------------------------------------------------------


#---------------------------------------------------------
def custom_subtract_vector_from_vector(vector1, vector2):
    result = []
    for x, y in zip(vector1, vector2):
        result.append(x - y)
    return result
#---------------------------------------------------------


#---------------------------------------------------------
def custom_cross_product(vector1, vector2):
    x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
    y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
    z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    return [x, y, z]
#---------------------------------------------------------


#---------------------------------------------------------
def custom_dot_product(vector1, vector2):
    result = 0
    for x, y in zip(vector1, vector2):
        result += x * y
    return result
#---------------------------------------------------------


#---------------------------------------------------------
def custom_vector_mag(vector):
    magnitude = sqrt(sum(component ** 
                         2 for component in vector))

    return magnitude
#---------------------------------------------------------


#---------------------------------------------------------
def custom_vector_s_m(scalar, vector):
    return [vector[i] * scalar for i in range(3)]
#---------------------------------------------------------


#-----------------------------------------------------------------------
def custom_vector_normalize(vector):

    magnitude = sqrt(sum(component ** 2 for component in vector))
    normalized_vector = [component / magnitude for component in vector]
    return normalized_vector
#-----------------------------------------------------------------------