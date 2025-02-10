import pygame
class Player():
    def __init__(self, x, y):
        self.rect=pygame.Rect(x,y,80,180)
        self.vel_y=0
        self.jump = False

    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        #Touche clavier
        key = pygame.key.get_pressed()

        #Contrôle
        if key[pygame.K_q]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED

        #saut
        if key[pygame.K_z] and self.jump == False:
            self.vel_y = -30
            self.jump = True

        #Gravité
        self.vel_y += GRAVITY
        dy += self.vel_y

        #Ne pas sortir de l'écran
        if self.rect.left + dx < 0:
            dx = -self.rect.x
        if self.rect.right + dy > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 55:
            self.vel_y = 0
            self.jump = False
            dy= screen_height - 55 - self.rect.bottom




        #position joueur
        self.rect.x += dx
        self.rect.y += dy




    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)