import pygame

class Bala:
    """
    Inicializa un objeto Bala.

    Args:
        x (int): Posición x de la bala.
        y (int): Posición y de la bala.
        direccion (int): Dirección en la que se mueve la bala (1 para derecha, -1 para izquierda).
        enemigos (list): Lista de enemigos en el juego.
        bullet_img (pygame.Surface): Imagen de la bala.
        win_width (int): Ancho de la ventana del juego.
    """
    def __init__(self, x, y, direccion, enemigos, bullet_img, win_width):
        self.x = x
        self.y = y
        self.direccion = direccion
        self.vel = 20
        self.enemigos = enemigos
        self.bullet_img = bullet_img
        self.win_width = win_width
        self.width = self.bullet_img.get_width()
        self.height = self.bullet_img.get_height()
        self.bullet_img = pygame.transform.flip(self.bullet_img, self.direccion == -1, False)

    def dibujar_bala(self, win):
        """
        Dibuja la bala en la ventana.

        Args:
            win (pygame.Surface): Superficie de la ventana del juego.
        """
        win.blit(self.bullet_img, (self.x, self.y))

    def movimiento_bala(self):
        """
        Mueve la bala en la dirección especificada.
        """
        self.x += (self.vel * self.direccion)

    def off_screen(self):
        """
        Verifica si la bala está fuera de la pantalla.

        Returns:
            bool: True si la bala está fuera de la pantalla, False en caso contrario.
        """
        return not (0 <= self.x <= self.win_width)

    def colision(self, hitbox):
        """
        Verifica si la bala colisiona con otro objeto.

        Args:
            hitbox (pygame.Rect): Rectángulo con el que se verifica la colisión.

        Returns:
            bool: True si hay colisión, False en caso contrario.
        """
        bala_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return bala_rect.colliderect(hitbox)