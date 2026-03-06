from numpy import imag, size
import pygame 
import constante
from personaje import Personaje, Damagetex
from items import Item
from Weapon import Weapon
import os


pygame.init()

# para crear mi ventana
ventana = pygame.display.set_mode((constante.ancho_ventana, constante.alto_ventana))
pygame.display.set_caption("Mi primer juego en Pygame")

# Fuente
font = pygame.font.Font("assets/font/8-bit Arcade Out.ttf", 25)#esto es para la letras , o sea cuando disparo es lo que aparece

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_image

# Funcion para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

# Funcion listar nombres elementos 
def nombres_carpetas(directorio):
    return os.listdir(directorio)

# personaje
# Cargar imágenes y escalar
animaciones = []
for i in range(9): 
    img = pygame.image.load(f"assets/player/FREE_Samurai - copia/q1sguyq1sguyq1sg_{i}.png").convert_alpha()
    img = escalar_img(img, constante.escala_personaje)
    animaciones.append(img)

# importar imagenes enemigos
directorios_enemigos = "assets/image/characters/enemigos"
tipo_enemigos = nombres_carpetas(directorios_enemigos)
animaciones_enemigos = []

for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets/image/characters/enemigos/{eni}"
    if os.path.isdir(ruta_temp):
        archivos = os.listdir(ruta_temp)
        archivos.sort() 
        for nombre_archivo in archivos:
            if nombre_archivo.endswith(".png"):
                img_enemigo = pygame.image.load(f"{ruta_temp}/{nombre_archivo}").convert_alpha()
                img_enemigo = escalar_img(img_enemigo, constante.scala_enemigos)
                lista_temp.append(img_enemigo)
        animaciones_enemigos.append(lista_temp)

# arma importa la imagen
imagen_pistola = pygame.image.load(f"assets/image/weapons/gun.png").convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constante.escala_arma)

# Bala
imagen_balas = pygame.image.load(f"assets/image/weapons/bullet.png").convert_alpha()
imagen_balas = escalar_img(imagen_balas, constante.escala_arma)

#cargar imagenes de los items
posion_amarilla=pygame.image.load("assets/image/items/potion.png").convert_alpha()
posion_amarilla=escalar_img(posion_amarilla,0.5)

coin_imagenes=[]
ruta_img="assets/image/items/coin"
num_coin_image= contar_elementos(ruta_img)
for i in range(5):
    img=pygame.image.load(f"assets/image/items/coin/coin_{i+1}.png").convert_alpha()
    img=escalar_img(img,scale=1)
    coin_imagenes.append(img)

# Crear el jugador
jugador = Personaje(constante.ancho_ventana//6, constante.alto_ventana//6, animaciones, energia=100)
jugador.flip = False 

# crear un enemigo de la clase personaje
Dash = Personaje(400, 300, animaciones_enemigos[0], energia=100)
run_right = Personaje(200, 200, animaciones_enemigos[1], energia=100)
Dash_1 = Personaje(100, 250, animaciones_enemigos[0], energia=100)
run_right_1 = Personaje(100, 150, animaciones_enemigos[1], energia=100)

#Energia,se mostraran las imagenes de los corazones 
corazón_vacio = pygame.image.load("assets/image/items/heart_empty.png").convert_alpha()
corazón_vacio=escalar_img(corazón_vacio,constante.scala_corazón)
corazón_mitad=pygame.image.load("assets/image/items/heart_half.png").convert_alpha()
corazón_mitad=escalar_img(corazón_mitad,constante.scala_corazón)
corazón_lleno=pygame.image.load("assets/image/items/heart_full.png").convert_alpha()
corazón_lleno=escalar_img(corazón_lleno,constante.scala_corazón)

def vida_jugador():
    c_mitad_dibujado = False
    for i in range(4):
        if jugador.energia>=((i+1)*25):#si es menor que 35 se dibuja el primer corazon
            ventana.blit (corazón_lleno,(5+i*85,5))
        elif jugador.energia%25>0 and c_mitad_dibujado == False:
            ventana.blit(corazón_mitad,(5+i*85,5))
            c_mitad_dibujado=True
        else:
            ventana.blit(corazón_vacio,(5+i*85,5))

# crear lista de enemigos
lista_enemigos = []
lista_enemigos.append(Dash)
lista_enemigos.append(Dash_1)
lista_enemigos.append(run_right)
lista_enemigos.append(run_right_1)

# creación de un arma 
pistola = Weapon(imagen_pistola, imagen_balas)

# crear un grupo de sprites
grupo_balas = pygame.sprite.Group()
grupo_damage_text = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()#cada que se cree un items se agrega 

monedas=Item(350,25,0,coin_imagenes)
posion=Item(380,55,1,[posion_amarilla])

grupo_items.add(monedas)
grupo_items.add(posion)
# definir las variables de movimientos del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False
disparar = False 

# controlar el frame rate
reloj = pygame.time.Clock()

run = True
while run: 
    reloj.tick(constante.fps)
    ventana.fill(constante.color_BG)
    
    # Procesar eventos
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            run = False

        if evento.type == pygame.KEYDOWN:       
            if evento.key == pygame.K_LEFT:
                mover_izquierda = True
            if evento.key == pygame.K_RIGHT: 
                mover_derecha = True
            if evento.key == pygame.K_UP:
               mover_arriba = True
            if evento.key == pygame.K_DOWN:
                mover_abajo = True
            if evento.key == pygame.K_RETURN: 
                disparar = True

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                mover_izquierda = False
            if evento.key == pygame.K_RIGHT:
                mover_derecha = False
            if evento.key == pygame.K_UP:
                mover_arriba = False
            if evento.key == pygame.K_DOWN:
                mover_abajo = False
            if evento.key == pygame.K_RETURN: 
                disparar = False

    # movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_derecha:
        delta_x += constante.velocidad
    if mover_izquierda:
        delta_x -= constante.velocidad
    if mover_arriba:
        delta_y -= constante.velocidad
    if mover_abajo:
        delta_y += constante.velocidad
    
    jugador.movimiento(delta_x, delta_y)
    jugador.update()
    
    # actualiza el estado del arma
    bala = pistola.update(jugador, disparar)
    if bala:
        grupo_balas.add(bala)
        
    # actualizar el daño
    grupo_damage_text.update()
    #actualizar items
    grupo_items.update()

    # dibujar el jugador
    jugador.dibujar(ventana)

    # actualiza estado del enemigos
    for ene in lista_enemigos:
        if ene.vivo:
            ene.update() 
            ene.dibujar(ventana)

    # Dibuja el arma 
    pistola.dibujar(ventana, jugador)

    # dibujar balas PRIMERO para verlas antes de que desaparezcan al chocar
    for b in grupo_balas:
        b.dibujar(ventana)

    #dibujar los corazones
    vida_jugador()

    # mover las balas y detectar colisiones DESPUES de dibujar
    for b in grupo_balas:
        damage, pos_damage = b.update(lista_enemigos)
        if damage:
            damage_text = Damagetex(pos_damage.centerx, pos_damage.centery, str(damage), font, constante.rojo)
            grupo_damage_text.add(damage_text)

    # dibujar texto de daño
    grupo_damage_text.draw(ventana)
    #dibujar items
    grupo_items.draw(ventana)

    pygame.display.update()

pygame.quit()
