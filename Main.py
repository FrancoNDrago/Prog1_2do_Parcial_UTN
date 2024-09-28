import pygame
import os
import csv
from Jugador import Personaje
from Enemigo import Enemy
from Constantes import *

def cargar_vida_torre_desde_csv(archivo_csv):
    """
    Carga la vida de la torre desde un archivo CSV.

    Args:
        archivo_csv (str): Ruta del archivo CSV.

    Returns:
        int: Vida de la torre.
    """
    with open(archivo_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            return int(row['vida'])

pygame.init()
pygame.mixer.music.load("Music/musica_in_game.mp3")
pygame.mixer.music.play(-1)
volumen_musica = 0.5
pygame.mixer.music.set_volume(volumen_musica)
win = pygame.display.set_mode((win_width, win_height))

pop_sound = pygame.mixer.Sound("Music/fuego_sonido.mp3")

bullet_height = 20
bullet_width = 15

# Bullet
bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Pj", "fuego.png")), (bullet_height, bullet_width))
# Fondo
background = pygame.transform.scale(pygame.image.load("forest.png"), (win_width, win_height))
# Tesoro
teasure = pygame.transform.scale(pygame.image.load(os.path.join("Teasure", "Torre_monje.png")), (200, 200))

def dibujar_juego():
    """
    Dibuja todos los elementos del juego en la ventana.
    """
    global torre_vida, velocidad
    win.fill((0, 0, 0))
    win.blit(background, (0, 0))  # Agregar el fondo
    # Dibujo de jugador
    player.dibujar(win)
    # Dibujo de balas
    for bala in player.balas:
        bala.dibujar_bala(win)
    # Dibujo de enemigos
    for enemigo in enemigos:
        enemigo.dibujar(win)
    # Dibujo del tesoro
    win.blit(teasure, (-45, 350))
    # Vidas del jugador
    if not player.vivo:
        win.fill((0, 0, 0))
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render(f"Perdiste! Eliminaste a {kills} enemigos. Toca R para arrancar de nuevo.", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (win_width // 2, win_height // 2)
        win.blit(text, textRect)
        if userInput[pygame.K_r]:
            player.vivo = True
            player.vidas = 1
            player.health = 30
            torre_vida = 2
            velocidad = 2
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(f"Vidas: {player.vidas} | Torre: {torre_vida} | Kills: {kills}", True, (0, 0, 0))
    win.blit(text, (750, 20))
    # Delay y update
    pygame.time.delay(30)
    pygame.display.update()

# Personaje main
player = Personaje(100, 480, [], win_width)
kills = 0

# Enemigo
enemigos = []
velocidad = 10

# Torre
torre_vida = 2
torre_vida = cargar_vida_torre_desde_csv("torre.csv")


# Ciclo principal
run = True
while run:
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_1:  
                volumen_musica = min(1.0, volumen_musica + 0.1)
                pygame.mixer.music.set_volume(volumen_musica)
            elif event.key == pygame.K_2:  
                volumen_musica = max(0.0, volumen_musica - 0.1)
                pygame.mixer.music.set_volume(volumen_musica)

    # Input
    userInput = pygame.key.get_pressed()

    # Disparo
    player.disparar(userInput, pop_sound, bullet_img)

    # Movilidad
    player.movimiento_Personaje(userInput)
    player.movimiento_salto(userInput)

    # Vida de la torre
    if torre_vida == 0:
        player.vivo = False

    # Enemigo
    if len(enemigos) == 0:
        enemigo = Enemy(1000, 450, velocidad, player, win_width)
        enemigos.append(enemigo)
        if velocidad <= 50:
            velocidad += 5
    for enemigo in enemigos:
        enemigo.mover()
        if enemigo.off_screen() or enemigo.health == 0:
            enemigos.remove(enemigo)
        if enemigo.x < 50:
            enemigos.remove(enemigo)
            torre_vida -= 1
        if enemigo.health == 0:
            kills += 1
        # Verificar colisiones entre enemigo y jugador
        if enemigo.colision(player.hitbox):
            player.health -= 5  # Ajusta el valor de daño según sea necesario
            if player.health <= 0:
                player.vidas -= 1
                player.health = 30
                if player.vidas == 0:
                    player.vivo = False

    # Actualiza la lista de enemigos del jugador
    player.enemigos = enemigos

    dibujar_juego()

    pygame.time.delay(10)
    pygame.display.update()

pygame.quit()