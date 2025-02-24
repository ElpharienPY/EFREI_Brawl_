import pygame
from pygame import mixer
from player import Player

mixer.init()
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

#musique et effets sonores
pygame.mixer.music.load("assets/sounds/fight_music1.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1,0.0,5000)
sword_fx = pygame.mixer.Sound("assets/sounds/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/sounds/magic.wav")
magic_fx.set_volume(0.75)

#données
background = pygame.image.load("assets/images/Arène EFREI Brawl.png")
warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/wizard.png").convert_alpha()
versus = pygame.image.load("assets/images/versus1.png").convert_alpha()
victory = pygame.image.load("assets/images/victory2.png").convert_alpha()
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
score_font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 50)
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0]#score du joueur P1-P2
round_over = False
ROUND_OVER_COOLDOWN = 2000

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
    screen.blit(versus,(0,0))
    pygame.draw.rect(screen, RED, (x-5,y-5,410, 40))
    pygame.draw.rect(screen, WHITE, (x,y,400, 30))
    pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, 400*ratio, 30))




#deux joueurs
fighter_1= Player(1,200, 480, False, WARRIOR_DATA,warrior_sheet, WARRIOR_ANIMATION_STEPS,sword_fx)
fighter_2 = Player(2 ,1000, 480,True, WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)
#fighter_3
#fighter_4

#Boucle
run=True
while run:

    clock.tick(FPS)

    #afficher arène
    draw_background()

    #afficher barre de vie
    draw_health_bar(fighter_1.health,20,50)
    draw_health_bar(fighter_2.health,850,50)
    draw_text("P1: " + str(score[0]), score_font,RED,20 ,90)
    draw_text("P2: " + str(score[1]), score_font, BLUE,1145 ,90)

    #mouvement pour P1
    if intro_count <= 0:

        fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen, fighter_2,round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1,round_over)
    else :
        draw_text(str(intro_count), count_font, BLUE, 540, 200)
        draw_text(str(intro_count), count_font, WHITE, 535, 195)
        if (pygame.time.get_ticks() - last_count_update) > 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    #charger animation
    fighter_1.update()
    fighter_2.update()

    #afficher fighter_1 and 2
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #defaite
    if round_over == False:
        if fighter_1.alive == False:
            score[1]+=1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0]+=1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else :
        #VICTOIRE !
        screen.blit(victory, (0,0))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Player(1, 200, 480, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,sword_fx)
            fighter_2 = Player(2, 1000, 480, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,magic_fx)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()


#exit pygame
pygame.quit()
