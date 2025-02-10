import pygame
from player import Player

pygame.init()

#Config fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arène")

#FPS CONTRÔLE
clock = pygame.time.Clock()
FPS = 60

#données
background = pygame.image.load("assets/images/Arène EFREI Brawl.png")

#fonction pour afficher arène
def draw_background():
    scaled_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))

#deux joueurs
fighter_1= Player(200, 480)
fighter_2 = Player(1000, 480 )

#Boucle
run=True
while run:

    clock.tick(FPS)

    #afficher arène
    draw_background()

    #mouvement pour P1
    fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT)
    #fighter_2.move()

    #afficher fighter_1 and 2
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()


#exit pygame
pygame.quit()
