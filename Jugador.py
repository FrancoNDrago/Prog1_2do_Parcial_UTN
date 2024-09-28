import pygame
import os
from Constantes import *
from Disparo import Bala

left = [pygame.image.load(os.path.join("Pj", "sprite_8.png")),
        pygame.image.load(os.path.join("Pj", "sprite_9.png")),
        pygame.image.load(os.path.join("Pj", "sprite_10.png")),
        pygame.image.load(os.path.join("Pj", "sprite_11.png")),
        pygame.image.load(os.path.join("Pj", "sprite_12.png")),
        pygame.image.load(os.path.join("Pj", "sprite_13.png")),
        pygame.image.load(os.path.join("Pj", "sprite_14.png")),
        pygame.image.load(os.path.join("Pj", "sprite_15.png"))
       ]

right = [pygame.image.load(os.path.join("Pj", "run_0.png")),
         pygame.image.load(os.path.join("Pj", "run_1.png")),
         pygame.image.load(os.path.join("Pj", "run_2.png")),
         pygame.image.load(os.path.join("Pj", "run_3.png")),
         pygame.image.load(os.path.join("Pj", "run_4.png")),
         pygame.image.load(os.path.join("Pj", "run_5.png")),
         pygame.image.load(os.path.join("Pj", "run_6.png")),
         pygame.image.load(os.path.join("Pj", "run_7.png"))
       ]


class Personaje:
    """
    Inicializa un objeto Personaje.

    Args:
        x (int): Posición x del personaje.
        y (int): Posición y del personaje.
        enemigos (list): Lista de enemigos en el juego.
        win_width (int): Ancho de la ventana del juego.
    """
    def __init__(self, x, y, enemigos, win_width):
        self.x = x
        self.y = y
        self.enemigos = enemigos
        self.win_width = win_width
        self.vel_x = 10
        self.vel_y = 10
        self.frente_derecho = True
        self.frente_izquierdo = False
        self.stepIndex = 0
        self.salto = False
        self.balas = []
        self.cooldown_contador = 0
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 50
        self.vidas = 1
        self.vivo = True

    def movimiento_Personaje(self, userInput):
        """
        Mueve al personaje basado en la entrada del usuario.

        Args:
            userInput (dict): Diccionario con el estado de las teclas.
        """
        if userInput[pygame.K_d] and self.x <= self.win_width - 62:
            self.x += self.vel_x
            self.frente_derecho = True
            self.frente_izquierdo = False
        elif userInput[pygame.K_a] and self.x >= 0:
            self.x -= self.vel_x
            self.frente_derecho = False
            self.frente_izquierdo = True
        else:
            self.stepIndex = 0

    def dibujar(self, win):
        """
        Dibuja al personaje en la ventana.

        Args:
            win (pygame.Surface): Superficie de la ventana del juego.
        """
        self.hitbox = (self.x - 1, self.y + 7, 20, 40)
        pygame.draw.rect(win, (255, 0, 0), (self.x - 4, self.y - 20, 30, 8))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x - 4, self.y - 20, self.health, 8))
        if self.stepIndex >= len(right):
            self.stepIndex = 0
        if self.frente_derecho:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        elif self.frente_izquierdo:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1

    def movimiento_salto(self, userInput):
        """
        Controla el movimiento de salto del personaje.

        Args:
            userInput (dict): Diccionario con el estado de las teclas.
        """
        if userInput[pygame.K_SPACE] and not self.salto:
            self.salto = True
        if self.salto:
            self.y -= self.vel_y * 2
            self.vel_y -= 1
        if self.vel_y < -10:
            self.salto = False
            self.vel_y = 10

    def direccion(self):
        """
        Devuelve la dirección en la que está mirando el personaje.

        Returns:
            int: 1 si el personaje mira a la derecha, -1 si mira a la izquierda.
        """
        if self.frente_derecho:
            return 1
        if self.frente_izquierdo:
            return -1

    def cooldown(self):
        """
        Maneja el cooldown del disparo del personaje.
        """
        if self.cooldown_contador >= 20:
            self.cooldown_contador = 0
        elif self.cooldown_contador > 0:
            self.cooldown_contador += 2

    def disparar(self, userInput, pop_sound, bullet_img):
        """
        Maneja el disparo del personaje.

        Args:
            userInput (dict): Diccionario con el estado de las teclas.
            pop_sound (pygame.mixer.Sound): Sonido del disparo.
            bullet_img (pygame.Surface): Imagen de la bala.
        """
        self.cooldown()
        if userInput[pygame.K_f] and self.cooldown_contador == 0:
            pop_sound.play()
            bullet = Bala(self.x, self.y, self.direccion(), self.enemigos, bullet_img, self.win_width)
            self.balas.append(bullet)
            self.cooldown_contador = 1

        for bala in self.balas:
            bala.movimiento_bala()
            if bala.off_screen():
                self.balas.remove(bala)
            else:
                for enemigo in self.enemigos:
                    if bala.colision(enemigo.hitbox):
                        enemigo.hit()
                        if bala in self.balas:
                            self.balas.remove(bala)
