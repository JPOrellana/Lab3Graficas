import pygame
from pygame.locals import *
from rt import Raytracer
from figures     import *
from lights import *
from materials import *

width = 670
height = 500

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)

raytracer.environmentMap = pygame.image.load("Fondo/fondito.jpg")

raytracer.rtClearColor(0.25, 0.25, 0.25)

# Crear Texturas

TexturaMorada   = pygame.image.load("Texturas/morado.jpg")
TexturaVerde  = pygame.image.load("Texturas/verde.jpg")
TexturaRoja  = pygame.image.load("Texturas/rojo.jpg")

# Crear Materiales
verde = Material(spec = 64, Ks = 0.2, texture = TexturaVerde)

roja = Material(spec = 64, Ks = 0.2, matType = REFLECTIVE, texture = TexturaRoja)

morada = Material(diffuse=(0.9, 0.9, 0.9), spec = 128, Ks = 0.2, ior= 1.5, matType = TRANSPARENT, texture = TexturaMorada)

# Crear Figuras

raytracer.scene.append(Triangle(v0=[-1.3, -1, -2], v1=[ -0.8, -1, -2],  v2=[ -1.05,  -0.5 , -2], material = verde))

raytracer.scene.append(Triangle(v0=[-0.7, -1, -2], v1=[0.1,  -1, -2], v2=[-0.35,  0.1, -2], material = roja))

raytracer.scene.append(Triangle(v0=[0.2, -1, -2], v1=[1.3,  -1, -2], v2=[0.7,  0.4, -2], material = morada))


# Luces
raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction = (-1,-1,-1), intensity = 0.9))
raytracer.lights.append(PointLight(point = (2.5,0,-4.5), intensity = 100, color = (1,0.2,1)))


raytracer.rtClear()
raytracer.rtRender()

print("\n Render Time: ", pygame.time.get_ticks() / 1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                isRunning = False


rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "output.jpg")

pygame.quit()