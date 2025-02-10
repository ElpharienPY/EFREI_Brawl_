import pygame

pygame.init()

#Config fenêtre
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arène")

#données
background = pygame.image.load("assets/images/Arène EFREI Brawl.png")

#fonction pour afficher arène
def draw_background():
    scaled_background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

#Boucle
run=True
while run:

    #afficher arène
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()


#exit pygame
pygame.quit()
