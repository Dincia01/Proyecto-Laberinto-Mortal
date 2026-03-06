import pygame
import constante

class Personaje:

    def __init__(self, x, y, animaciones,energia):
        self.energia =energia
        self.vivo= True #indica si el personaje esta vivo
        # Usar las animaciones que vienen desde juego.py
        self.animaciones = animaciones

        # Índice que indica qué imagen se está mostrando
        self.frame_index = 0

        # Control del tiempo de animación
        self.update_time = pygame.time.get_ticks()

        # Imagen actual
        self.image = self.animaciones[self.frame_index]
   
        # Rectángulo del personaje
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)

        self.flip = False  # False = mirando a la derecha, True = mirando a la izquierda

    def movimiento(self, dx, dy):
        self.forma.x += dx
        self.forma.y += dy

        # cambiar dirección
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

    def update(self):
        #comprobar si el personaje ha muerto
        if self.energia <= 0:
            self.energia=0
            self.vivo = False
        
        cooldown_animaciones=100
        if pygame.time.get_ticks() - self.update_time > constante.cooldown_animaciones:

            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0

        self.image = self.animaciones[self.frame_index]


    def dibujar(self, interfaz):
        image = self.image
        if self.flip:
            image = pygame.transform.flip(self.image, True, False)
        interfaz.blit(image, self.forma)

   # self.color_personaje,self.forma,width=1)
class Damagetex(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, font, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.contador = 0

    def update(self):
        self.rect.y -= 2
        self.contador += 1
        if self.contador > 50:
            self.kill()

