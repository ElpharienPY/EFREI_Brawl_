import pygame
from player import Player

pygame.init()

#Config fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arène")

#color
RED=(255,0,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

#FPS CONTRÔLE
clock = pygame.time.Clock()
FPS = 60

#données
background = pygame.image.load("assets/images/Arène EFREI Brawl.png")
warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/wizard.png").convert_alpha()
WARRIOR_SIZE = 162
WARRIOR_SCALE = 6
WARRIOR_OFFSET = [72,68]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 5
WIZARD_OFFSET = [112,127]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

#Compteur
count_font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 400)
score_font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 200)
intro_count = 3
last_count_update = pygame.time.get_ticks()

#definir animation
WARRIOR_ANIMATION_STEPS= [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS= [8,8,1,8,8,3,7]

#
def draw_text (text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

#fonction pour afficher arène
def draw_background():
    scaled_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))

#barre de vie
def draw_health_bar(health,x,y):
    ratio = health/100
    pygame.draw.rect(screen, RED, (x-5,y-5,410, 40))
    pygame.draw.rect(screen, WHITE, (x,y,400, 30))
    pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, 400*ratio, 30))




#deux joueurs
fighter_1= Player(1,200, 480, False, WARRIOR_DATA,warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Player(2 ,1000, 480,True, WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS )

#Boucle
run=True
while run:

    clock.tick(FPS)

    #afficher arène
    draw_background()

    #afficher barre de vie
    draw_health_bar(fighter_1.health,20,50)
    draw_health_bar(fighter_2.health,850,50)

    #mouvement pour P1
    if intro_count <= 0:

        fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen, fighter_2)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    else :
        draw_text(str(intro_count), count_font, BLUE, 540, 200)
        if (pygame.time.get_ticks() - last_count_update) > 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    #charger animation
    fighter_1.update()
    fighter_2.update()

    #afficher fighter_1 and 2
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()


#exit pygame
pygame.quit()
