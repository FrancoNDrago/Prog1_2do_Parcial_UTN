import pygame
import os
from Constantes import *

left_enemy = [pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_0.png")),
              pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_1.png")),
              pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_3.png")),
              pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_4.png")),
              pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_5.png")),
              pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_6.png")),
              pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_7.png"))
              ]
right_enemy = [pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_8.png")),
               pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_9.png")),
               pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_10.png")),
               pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_11.png")),
               pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_12.png")),
               pygame.image.load(os.path.join("Enemy_Multimedia", "enemy_13.png"))
               ]

class Enemy:
    """
    Inicializa un objeto Enemy.

    Args:
        x (int): Posición x del enemigo.
        y (int): Posición y del enemigo.
        velocidad (int): Velocidad del enemigo.
        player (Personaje): Objeto del jugador.
        win_width (int): Ancho de la ventana del juego.
    """
    def __init__(self, x, y, velocidad, player, win_width):
        self.x = x
        self.y = y
        self.vel = velocidad
        self.player = player
        self.win_width = win_width
        self.stepIndex = 0
        self.health = 30
        self.hitbox = (self.x, self.y, 64, 64)

    def step(self):
        """
        Actualiza el índice del sprite del enemigo.
        """
        if self.stepIndex >= len(left_enemy):
            self.stepIndex = 0

    def dibujar(self, win):
        """
        Dibuja al enemigo en la ventana.

        Args:
            win (pygame.Surface): Superficie de la ventana del juego.
        """
        self.hitbox = (self.x + 6, self.y - 5, 60, 90)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y - 10, 30, 8))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y - 10, self.health, 8))
        self.step()
        win.blit(left_enemy[self.stepIndex], (self.x, self.y))
        self.stepIndex += 1

    def hit(self, damage=10):
        """
        Reduce la salud del enemigo cuando es golpeado.

        Args:
            damage (int): Cantidad de daño infligido. Por defecto es 10.
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def mover(self):
        """
        Mueve al enemigo.
        """
        self.x -= self.vel

    def off_screen(self):
        """
        Verifica si el enemigo está fuera de la pantalla.

        Returns:
            bool: True si el enemigo está fuera de la pantalla, False en caso contrario.
        """
        return not (0 <= self.x <= self.win_width)

    def colision(self, rect):
        """
        Verifica si el enemigo colisiona con otro objeto.

        Args:
            rect (pygame.Rect): Rectángulo con el que se verifica la colisión.

        Returns:
            bool: True si hay colisión, False en caso contrario.
        """
        enemy_rect = pygame.Rect(self.hitbox)
        return enemy_rect.colliderect(rect)