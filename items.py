import pygame.sprite

class Item(pygame.sprite.Sprite):
    
    def __init__(self, x, y, item_type, animacion_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0 = monedas, 1 = pociones
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
    
        # Actualizar la imagen según el frame actual
        self.image = self.animacion_list[self.frame_index]

        # Controlar la velocidad de la animación
        if pygame.time.get_ticks() - self.update_time > cooldow_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # Reiniciar la animación si llega al final de la lista
        if self.frame_index >= len(self.animacion_list):
            self.frame_index = 0