import pygame
import constante
import math
import random

class Weapon():
    def __init__(self,image,imagen_bala):
        self.imagen_bala=imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original,self.angulo)
        self.forma = self.imagen.get_rect()
        self.dispara =  False
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self,personaje, disparar): 
        bala = None
        disparo_cooldown = 250
        self.forma.center = (personaje.forma.centerx, personaje.forma.centery + 60)#esto para bajar el alma

        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.forma.width/4
        else:
            self.forma.x = self.forma.x - personaje.forma.width/4 

        mouse_pos = pygame.mouse.get_pos()
        dist_x = mouse_pos[0] - self.forma.centerx
        dist_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(dist_y, dist_x))

        if disparar and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.ultimo_disparo = pygame.time.get_ticks()

        return bala
    
    def dibujar(self, interfaz, personaje): 
        imagen_flip = self.imagen_original
        if personaje.flip:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, True)
            
        self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        nueva_forma = self.imagen.get_rect(center=self.forma.center)
        interfaz.blit(self.imagen, nueva_forma)


class Bullet(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        
        self.image = pygame.transform.scale(image, (int(image.get_width() * constante.escala_bala), int(image.get_height() * constante.escala_bala)))
        
        self.image = pygame.transform.rotate(self.image, self.angulo)
        self.rect = self.image.get_rect()
        
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.rect.center = (int(self.pos_x), int(self.pos_y))

        self.delta_x = math.cos(math.radians(self.angulo)) * constante.velocidad_bala
        self.delta_y = -(math.sin(math.radians(self.angulo)) * constante.velocidad_bala)

    def update(self, lista_enemigos):
        daño = 0
        pos_daño = None
        
        self.pos_x += self.delta_x
        self.pos_y += self.delta_y
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
       
        info = pygame.display.Info()
        if self.rect.right < -100 or self.rect.left > info.current_w + 100 or \
           self.rect.bottom < -100 or self.rect.top > info.current_h + 100:
            self.kill()

        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect) and enemigo.vivo:
                daño = 15 + random.randint(-7, 7)
                pos_daño = enemigo.forma
                enemigo.energia -= daño
                self.kill() 
                break
        return daño, pos_daño
          
    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.rect)