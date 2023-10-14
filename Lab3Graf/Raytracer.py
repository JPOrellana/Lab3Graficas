import pygame
from pygame.locals import *
from rt import Raytracer
from figuras import *
from lights import *
from materials import *

width = 500
height = 500
pygame.init() 

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE  )
screen.set_alpha(None)


raytracer = Raytracer(screen)

raytracer.envMap = pygame.image.load("Fondo/fondito.jpg")

raytracer.rtClearColor(0.25,0.25,0.25)

azul = pygame.image.load("Texturas/azul.jpg")
morado = pygame.image.load("Texturas/morado.jpg")


blueMirror = Material(diffuse = (0.4,0.4,0.9), spec = 32, ks = 0.15, matType = REFLECTIVE)

#TRANSPARENT MATS
diamond = Material(diffuse = (0.9,0.9,0.9), spec = 128, ks = 0.2, ior= 2.417, matType = TRANSPARENT)
brick = Material(diffuse = (1,0.4,0.4), spec = 8, ks = 0.01)
grass = Material(diffuse = (0.4,1,0.4), spec =32, ks = 0.1) 
water = Material(diffuse = (0.4,0.4,1), spec = 256, ks = 0.2)


mirror = Material(diffuse = (0.9,0.9,0.9), spec = 64, ks = 0.2, matType = REFLECTIVE)
glass = Material(diffuse= (0.9,0.9,0.9),spec = 64, ks = 0.15, ior = 1.5, matType=TRANSPARENT)
water = Material(diffuse = (0.4,0.4,1.0), spec = 128, ks = 0.2, ior= 1.33, matType = TRANSPARENT)
goldMinecraft = Material(texture = morado,spec = 24, ks = 0.1, matType=OPAQUE)
diamondMinecraft = Material(texture = morado,spec = 24, ks = 0.1, matType=OPAQUE)

cilindro_azul = Material(texture=azul, spec=32, ks=0.1, matType=OPAQUE)
cilindro_morado = Material(texture=morado, spec=32, ks=0.1, matType=TRANSPARENT)
pyramid_materialR = Material(texture=azul, spec=32, ks=0.1, matType=REFLECTIVE)

# Crear una piramide

cilindro = Cylinder(position=(0, -1, -1.5), radius=0.5, height=0.5, material=cilindro_azul)


raytracer.scene.append(cilindro)



# Luces
ambient_light = AmbientLight(intensity=0.3, color=(1, 0.8, 0.6))  # Luz ambiental suave
directional_light = DirectionalLight(direction=(1, -1, -1), intensity=1.0, color=(1, 0.9, 0.8))  # Luz direccional principal
point_light = PointLight(point=(2, 2, 2), intensity=1.0, color=(1, 1, 1))  # Luz puntual (ajusta la posición según sea necesario)

# Agregar las luces a la escena
raytracer.lights.append(ambient_light)
raytracer.lights.append(directional_light)
raytracer.lights.append(point_light)

raytracer.rtClear()
raytracer.rtRender()

print("\nrender time", pygame.time.get_ticks()/1000, "secs")
isRunning = True
while isRunning:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
rect = pygame.Rect(0,0,width,height)   
sub = screen.subsurface(rect)
pygame.image.save(sub, "output.jpg")   

pygame.quit()