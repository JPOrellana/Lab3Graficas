import numpyPablo as np
from math import acos, asin


def reflectVector(normal,direction):
    reflect = 2* np.custom_dot_product(normal, direction)
    reflect = np.custom_multiply_vector_by_scalar(normal,reflect)
    reflect = np.custom_subtract_vectors(reflect, direction)
    reflect = np.custom_multiply_vector_by_scalar(reflect, 1 / np.custom_linalg_norm(reflect))
    return reflect

def refractVector(normal, incident, n1,n2): 
    c1 = np.custom_dot_product(normal,incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = np.custom_normalize(normal)
        normal = [i * -1 for i in normal]
    
        n1, n2 = n2, n1

    n = n1 / n2

    T = np.custom_subtract_vectors( np.custom_multiply_vector_by_scalar((np.custom_add_vectors(incident ,  np.custom_multiply_vector_by_scalar(normal,c1))),n  ) , np.custom_multiply_vector_by_scalar(normal ,(1 - n**2 * (1 - c1**2))** 0.5))
    T = np.custom_multiply_vector_by_scalar(T, 1 / np.custom_linalg_norm(T))

    return T

def totalInternalReflection(normal,incident,n1,n2):
    c1 = np.custom_dot_product(normal,incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False
    

    return acos(c1) >= asin(n2/n1)

def fresnel(normal,incident,n1, n2):
    c1 = np.custom_dot_product(normal,incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1
        
    s2 = (n1 * (1 - c1**2)**0.5) / n2
    c2 = (1 - s2 **2) **0.5
    F1 = (( (n2 * c1) - (n1 * c2) ) / ((n2 * c1) + (n1 *c2))) **2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 *c1))) **2


    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt


class Light(object):
    def __init__(self, intensity = 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType

    def getLightColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intecept, viewPos):
        return None


class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,1,1)):
        super().__init__(intensity, color, "Ambient")

class DirectionalLight(Light):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = np.custom_multiply_vector_by_scalar(direction, 1 / np.custom_linalg_norm(direction))
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):
        dir = [(i * -1) for i in self.direction] 
        intensity = np.custom_dot_product(intercept.normal, dir) * self.intensity
        intensity = max(0,min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return  [(i * intensity) for i in self.color]
    
    def getSpecularColor(self, intercept, viewPos):
        dir = [(i * -1) for i in self.direction]

        reflect = reflectVector(intercept.normal, dir)

        
        viewDir = np.custom_subtract_vector_from_vector(viewPos,intercept.point)
        viewDir = np.custom_multiply_vector_by_scalar(viewDir, 1 / np.custom_linalg_norm(viewDir))


        specIntensity = max(0, np.custom_dot_product(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        return [(i * specIntensity) for i in self.color] 
    
class PointLight(Light):
    def __init__(self, point = (0,0,0),intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity,color, "Point")

    def getDiffuseColor(self, intercept):
        dir = np.custom_subtract_vector_from_vector(self.point,intercept.point)
        self.dir = np.custom_multiply_vector_by_scalar(dir, 1 / np.custom_linalg_norm(dir))

        intensity = np.custom_dot_product(intercept.normal, dir) * self.intensity
        intensity = max(0,min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return  [(i * intensity) for i in self.color]

    def getSpecularColor(self, intercept, viewPos):
        dir = np.custom_subtract_vector_from_vector(self.point,intercept.point)

        reflect = reflectVector(intercept.normal, dir)

        viewDir = np.custom_subtract_vector_from_vector(viewPos, intercept.point)
        viewDir = np.custom_normalize(viewDir)
        
        specIntensity = max(0, np.custom_dot_product(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        return [(i * specIntensity) for i in self.color] 