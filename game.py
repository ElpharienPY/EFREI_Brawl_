import pygame
import random
import os
from pygame import mixer
from player import Player

mixer.init()
pygame.init()

# Config fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arène")

# Couleurs
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# FPS CONTRÔLE
clock = pygame.time.Clock()
FPS = 60
"""
# Musique et effets sonores
music_folder = "assets/sounds/musics"
music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
if music_files:
    chosen_music = random.choice(music_files)
    music_path = os.path.join(music_folder, chosen_music)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1, 0.0, 5000)"""

sword_fx = pygame.mixer.Sound("assets/sounds/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/sounds/magic.wav")
magic_fx.set_volume(0.75)
punch_fx = pygame.mixer.Sound("assets/sounds/Punch_Sound_Effect.wav")
punch_fx.set_volume(0.75)
electricity_fx = pygame.mixer.Sound("assets/sounds/electricity_sound.mp3")
electricity_fx.set_volume(0.75)

# Données des personnages
background = pygame.image.load("assets/images/Arene_HD.jpeg").convert_alpha()
versus = pygame.image.load("assets/images/versus1.png").convert_alpha()
victory = pygame.image.load("assets/images/victory2.png").convert_alpha()

#Warrior (Morgado)
warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
WARRIOR_SIZE = 162
WARRIOR_SCALE = 5
WARRIOR_OFFSET = [72,68]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]

#Wizard (Kais)
wizard_sheet = pygame.image.load("assets/images/wizard/wizard.png").convert_alpha()
WIZARD_SIZE = 250
WIZARD_SCALE = 4
WIZARD_OFFSET = [112,127]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

#Knight (Chahine)
king_sheet = pygame.image.load("assets/images/king/king.png").convert_alpha()
KING_SIZE = 155
KING_SCALE = 3
KING_OFFSET = [70,63]
KING_DATA = [KING_SIZE,KING_SCALE,KING_OFFSET]

#Fighter (Rado)
fighter_sheet = pygame.image.load("assets/images/fighter/fighter.png").convert_alpha()
FIGHTER_SIZE = 200
FIGHT_SCALE = 5
FIGHT_OFFSET = [95,88]
FIGHTER_DATA = [FIGHTER_SIZE,FIGHT_SCALE,FIGHT_OFFSET]

#definir animation
WARRIOR_ANIMATION_STEPS= [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS= [8,8,2,8,8,3,7]
KING_ANIMATION_STEPS= [6,8,2,6,6,4,11]
FIGHTER_ANIMATION_STEPS= [8,8,2,6,6,4,6]

# Compteur
count_font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 400)
score_font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 50)
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000
rounds_joues = 0
MAX_ROUNDS = 5

# Fonctions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_background():
    screen.blit(background, (0, 0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    screen.blit(versus, (0, 0))
    pygame.draw.rect(screen, RED, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, WHITE, (x, y, 400, 30))
    pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, 400 * ratio, 30))

def reset_round():
    global fighter_1, fighter_2, intro_count, round_over, rounds_joues
    rounds_joues += 1
    intro_count = 3
    round_over = False
    fighter_1 = Player(1, 200, 480, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, electricity_fx,joystick_id=0)  # warrior
    # fighter_1= Player(1,200,480,False,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)
    # fighter_1= Player(1,200, 500, False, KING_DATA,king_sheet, KING_ANIMATION_STEPS,sword_fx) #king
    # fighter_1= Player(1,200,480,False,FIGHTER_DATA,fighter_sheet,FIGHTER_ANIMATION_STEPS,punch_fx) #fighter

    fighter_2 = Player(2, 1000, 500, True, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, electricity_fx,joystick_id=1)  # warrior
    # fighter_2 = Player(2 ,1000, 500,True, WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx) #wizard
    # fighter_2 = Player(2 ,1000, 500,True, KING_DATA,king_sheet, KING_ANIMATION_STEPS,sword_fx) #king
    # fighter_2 = Player(2 ,1000, 500,True, FIGHTER_DATA,fighter_sheet,FIGHTER_ANIMATION_STEPS,punch_fx) #fighter


def check_game_over():
    if score[0] == 1:
        return "Joueur 1 Gagne !"
    elif score[1] == 1:
        return "Joueur 2 Gagne !"
    return None

# Initialisation des joueurs
reset_round()

# Boucle du jeu
run = True
while run:
    clock.tick(FPS)
    draw_background()
    draw_health_bar(fighter_1.health, 20, 50)
    draw_health_bar(fighter_2.health, 850, 50)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 90)
    draw_text("P2: " + str(score[1]), score_font, BLUE, 1145, 90)

    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT)
    else:
        draw_text(str(intro_count), count_font, BLUE, 540, 200)
        draw_text(str(intro_count), count_font, WHITE, 535, 195)
        if (pygame.time.get_ticks() - last_count_update) > 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    fighter_1.update()
    fighter_2.update()
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
        if round_over:
            round_over_time = pygame.time.get_ticks()
    else:
        winner = check_game_over()
        if winner:
            screen.blit(victory, (0, 0))
        else:
            screen.blit(victory, (0, 0))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                if rounds_joues < MAX_ROUNDS:
                    reset_round()
                else:
                    run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
