from numpyPablo import custom_vector_normalize, custom_dot_product, custom_subtract_vectors, custom_vector_mag, custom_ref


class Light(object):

    def __init__(self, intensity = 1, color = (1,1,1), light_type = "None"):
        self.intensity = intensity
        self.color = color
        self.type = light_type


    def getLightColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]


    def getDiffuseColor(self, intercept):
        return self.getLightColor()

    def getSpecularColor(self, intercept, viewPos):
        return None



class AmbientLight(Light):

    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Ambient")



class DirectionalLight(Light):

    def __init__(self, direction = (0,-1,0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Directional")
        self.direction = custom_vector_normalize(direction)


    def getDiffuseColor(self, intercept):
        direction = [i * -1 for i in self.direction]

        intensity = custom_dot_product(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.Ks

        diffuseColor = [i * intensity for i in self.color]

        return diffuseColor


    def getSpecularColor(self, intercept, viewPos):
        direction = [i * -1 for i in self.direction]
        
        reflect = custom_ref(intercept.normal, direction)

        viewDir = custom_subtract_vectors(viewPos, intercept.point)
        viewDir = custom_vector_normalize(viewDir)

        specularIntensity = max(0, custom_dot_product(viewDir, reflect)) ** intercept.obj.material.specular
        specularIntensity *= intercept.obj.material.Ks
        specularIntensity *= self.intensity

        specularColor = [i * specularIntensity for i in self.color]

        return specularColor



class PointLight(Light):
    def __init__(self, point = (0,0,0), intensity = 1, color = (1, 1, 1)):
        super().__init__(intensity, color, "Point")
        self.point = point


    def getDiffuseColor(self, intercept):
        direction = custom_subtract_vectors(self.point, intercept.point)
        R = custom_vector_mag(direction)
        direction = [direction[i] / R for i in range(3)]

        intensity = custom_dot_product(intercept.normal, direction) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks

        if R != 0:
            intensity = intensity / R**2
        
        intensity = max(0, min(1, intensity))
        
        diffuseColor = [i * intensity for i in self.color]

        return diffuseColor

    def getSpecularColor(self, intercept, viewPos):
        direction = custom_subtract_vectors(self.point, intercept.point)
        R = custom_vector_mag(direction)
        direction = [direction[i] / R for i in range(3)]
        
        reflect = custom_ref(intercept.normal, direction)

        viewDir = custom_subtract_vectors(viewPos, intercept.point)
        viewDir = custom_vector_normalize(viewDir)

        specularIntensity = max(0, custom_dot_product(viewDir, reflect)) ** intercept.obj.material.specular
        specularIntensity *= intercept.obj.material.Ks
        specularIntensity *= self.intensity

        if R != 0:
            specularIntensity /= R**2
        
        specularIntensity = max(0, min(1, specularIntensity))

        specularColor = [i * specularIntensity for i in self.color]

        return specularColor