import pygame
import cv2
import os
import numpy as np
import random
from pygame import mixer
from player import Player
from projectile import Projectile


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

# Musique et effets sonores
music_folder = "assets/sounds/musics"
music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
if music_files:
    chosen_music = random.choice(music_files)
    music_path = os.path.join(music_folder, chosen_music)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1, 0.0, 5000)

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

# Warrior (Morgado)
warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
WARRIOR_SIZE = 162
WARRIOR_SCALE = 5
WARRIOR_OFFSET = [72,68]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]

# Wizard (Kais)
wizard_sheet = pygame.image.load("assets/images/wizard/wizard.png").convert_alpha()
WIZARD_SIZE = 250
WIZARD_SCALE = 4
WIZARD_OFFSET = [112,127]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

# Knight (Chahine)
king_sheet = pygame.image.load("assets/images/king/king.png").convert_alpha()
KING_SIZE = 155
KING_SCALE = 3
KING_OFFSET = [70,63]
KING_DATA = [KING_SIZE,KING_SCALE,KING_OFFSET]

# Fighter (Rado)
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
round_over = False

# Musique Lobby
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/lobby_sound.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Configuration de la fenêtre
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu du Jeu")

# Chargement des images de l'interface
background_menu = pygame.image.load("assets/images/menu_background.png")
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))
button_image = pygame.image.load("assets/images/button_1v1.png")
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

background_select = pygame.image.load("assets/images/characters_select.png")
background_select = pygame.transform.scale(background_select, (WIDTH, HEIGHT))

# Ajout des fonds dédiés pour la sélection des joueurs
player1_screen = pygame.image.load("assets/images/player1_select.png")
player1_screen = pygame.transform.scale(player1_screen, (WIDTH, HEIGHT))

player2_screen = pygame.image.load("assets/images/player2_select.png")
player2_screen = pygame.transform.scale(player2_screen, (WIDTH, HEIGHT))

# Liste des personnages et images
character_names = ["M.Rado", "M.Chahine", "Gabi", "M.Kais"]
character_images = [
    pygame.image.load("assets/images/assets_1_(Rado).png"),
    pygame.image.load("assets/images/assets_2_(Chahine).png"),
    pygame.image.load("assets/images/assets_3_(Morgadp).png"),
    pygame.image.load("assets/images/test_joueur4.png"),
]

# Redimensionnement des images des personnages
character_width, character_height = 150, 250
character_images = [pygame.transform.scale(img, (character_width, character_height)) for img in character_images]

# Coordonnées des personnages
character_positions = [
    (WIDTH // 2 - 378, HEIGHT // 2 - 265),
    (WIDTH // 2 - 172, HEIGHT // 2 - 265),
    (WIDTH // 2 + 28, HEIGHT // 2 - 265),
    (WIDTH // 2 + 228, HEIGHT // 2 - 265)
]

# Stockage des choix des joueurs sous forme d'index
selected_players = {"J1": None, "J2": None}

# Dictionnaire des vidéos d'introduction des personnages
character_videos = {
    "M.Rado": "assets/vidéos/Rado_intro.mp4",
    "M.Chahine": "assets/vidéos/Chahine_intro.mp4",
    "Gabi": "assets/vidéos/Gabi_intro.mp4",
    "M.Kais": "assets/vidéos/Kais_intro.mp4"
}

# Dictionnaire des personnages et leurs données associées
character_data = {
    "M.Rado": {"data": FIGHTER_DATA, "sheet": fighter_sheet, "animation_steps": FIGHTER_ANIMATION_STEPS, "effect": punch_fx},
    "M.Chahine": {"data": KING_DATA, "sheet": king_sheet, "animation_steps": KING_ANIMATION_STEPS, "effect": sword_fx},
    "Gabi": {"data": WARRIOR_DATA, "sheet": warrior_sheet, "animation_steps": WARRIOR_ANIMATION_STEPS, "effect": electricity_fx},
    "M.Kais": {"data": WIZARD_DATA, "sheet": wizard_sheet, "animation_steps": WIZARD_ANIMATION_STEPS, "effect": magic_fx},
}

# Chargement des spritesheets de projectiles
def load_frames_from_sheet(sheet, frame_width, frame_height, count, scale=1):
    frames = []
    for i in range(count):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        if scale != 1:
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)
    return frames

# Données attaques ultimes
fireball_sheet = pygame.image.load("assets/images/blue_fireball/blue_fireball.png").convert_alpha()
fireball_frames = load_frames_from_sheet(fireball_sheet, 52, 52, 6, scale=6)

lightning_sheet = pygame.image.load("assets/images/lightning/lightning.png").convert_alpha()
lightning_frames = load_frames_from_sheet(lightning_sheet, 42, 42, 6, scale=8)


# Association des attaques ultimes/personnages
ultimate_projectiles = {
    "M.Rado": {
        "frames": fireball_frames,
        "speed": 15,
        "damage": 25
    },
    "M.Chahine": {
        "frames": lightning_frames,
        "speed": 12,
        "damage": 25
    },
    "Gabi": {
        "frames": lightning_frames,
        "speed": 20,
        "damage": 25
    },
    "M.Kais": {
        "frames": fireball_frames,
        "speed": 15,
        "damage": 25
    }
}

def play_video(video_path):
    """Jouer une vidéo directement dans la fenêtre Pygame."""
    if not os.path.exists(video_path):
        print(f"⚠️ Erreur : Le fichier vidéo {video_path} est introuvable.") #Vérification présence de la vidéo
        return

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"⚠️ Erreur : Impossible d'ouvrir la vidéo {video_path}.")
        return

    clock = pygame.time.Clock()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))

        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        clock.tick(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()

    cap.release()
    cv2.destroyAllWindows()


def select_player():
    """Écran pour choisir les joueurs."""
    global selected_players

    # Attente pour J1
    screen.blit(player1_screen, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                waiting = False  # J1 a appuyé sur "1"

    select_character("J1")  # Sélection du personnage du Joueur 1

    # Attente pour J2
    screen.blit(player2_screen, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                waiting = False  # J2 a appuyé sur "2"

    select_character("J2")  # Sélection du personnage du Joueur 2

    pygame.mixer.music.stop()

def select_character(player_key):
    """Écran pour choisir un personnage avec stockage dans le dictionnaire."""
    selected_index = 0
    running = True

    while running:
        screen.blit(background_select, (0, 0))

        for i, (img, pos) in enumerate(zip(character_images, character_positions)):
            screen.blit(img, pos)
            if i == selected_index:
                pygame.draw.rect(screen, (255, 215, 0),
                                 (pos[0] - 5, pos[1] - 5, character_width + 10, character_height + 10), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(character_names)
                elif event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(character_names)
                elif event.key == pygame.K_RETURN:
                    selected_players[player_key] = character_names[selected_index]  # Stocke le nom du personnage
                    running = False

        pygame.display.flip()

    # Récupérer les données associées au personnage choisi
    chosen_character = selected_players[player_key]
    character_info = character_data[chosen_character]  # Obtenir les données associées au personnage choisi

    # Initialiser le personnage dans le gameplay
    if player_key == "J1":
        global fighter_1
        fighter_1 = Player(1, 200, 480, False, character_info["data"], character_info["sheet"], character_info["animation_steps"], character_info["effect"])
    else:
        global fighter_2
        fighter_2 = Player(2, 1000, 500, True, character_info["data"], character_info["sheet"], character_info["animation_steps"], character_info["effect"])

    # Jouer la vidéo du personnage sélectionné
    if chosen_character in character_videos:
        play_video(character_videos[chosen_character])

    print(f"{player_key} a choisi : {chosen_character} (Index {selected_players[player_key]})")

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

def check_game_over():
    if score[0] == 3:
        return "Joueur 1 Gagne !"
    elif score[1] == 3:
        return "Joueur 2 Gagne !"
    return None

# Dictionnaire d'association entre les personnages et leurs données
character_mapping = {
    "M.Rado": (FIGHTER_DATA, fighter_sheet, FIGHTER_ANIMATION_STEPS, punch_fx),
    "M.Chahine": (KING_DATA, king_sheet, KING_ANIMATION_STEPS, sword_fx),
    "Gabi": (WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, electricity_fx),
    "M.Kais": (WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx),
}

def reset_round():
    """Réinitialise le round en prenant en compte les personnages sélectionnés."""
    global fighter_1, fighter_2, intro_count, round_over, rounds_joues

    rounds_joues += 1
    intro_count = 3
    round_over = False

    # Récupérer les choix des joueurs
    player1_choice = selected_players["J1"]
    player2_choice = selected_players["J2"]

    # Obtenir les données des personnages sélectionnés
    p1_data, p1_sheet, p1_steps, p1_fx = character_mapping[player1_choice]
    p2_data, p2_sheet, p2_steps, p2_fx = character_mapping[player2_choice]

    # Créer les objets Player avec les données correspondantes
    fighter_1 = Player(1, 200, 480, False, p1_data, p1_sheet, p1_steps, p1_fx)
    fighter_2 = Player(2, 1000, 500, True, p2_data, p2_sheet, p2_steps, p2_fx)

# Jauge d'énergie segmentée (couleur or)
def draw_energy_bar_segments(energy, x, y):
    segment_count = 5
    segment_width = 35
    segment_height = 15
    spacing = 8
    energy_per_segment = 100 / segment_count
    active_segments = int(energy / energy_per_segment)
    for i in range(segment_count):
        seg_x = x + i * (segment_width + spacing)
        color = (255, 215, 0) if i < active_segments else (60, 60, 60)
        glow_color = (255, 255, 150, 50) if i < active_segments else None
        if glow_color:
            glow_surf = pygame.Surface((segment_width + 10, segment_height + 10), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, glow_color, (0, 0, segment_width + 10, segment_height + 10))
            screen.blit(glow_surf, (seg_x - 5, y - 5))
        pygame.draw.rect(screen, color, (seg_x, y, segment_width, segment_height), border_radius=4)
        pygame.draw.rect(screen, WHITE, (seg_x, y, segment_width, segment_height), 2, border_radius=4)

# Variables globales
fighter_1 = None
fighter_2 = None
projectiles = []
score = [0, 0]
projectiles = []
round_over = False

intro_count = 3
last_count_update = pygame.time.get_ticks()
rounds_joues = 0
MAX_ROUNDS = 5
ROUND_OVER_COOLDOWN = 2000

emoji_font=pygame.font.SysFont("segoeuiemoji", 40)

def main_gameplay():
    global round_over, score, intro_count, last_count_update, rounds_joues

    run = True
    round_over_time = 0

    music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    if music_files:
        chosen_music = random.choice(music_files)
        music_path = os.path.join(music_folder, chosen_music)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1, 0.0, 5000)

    while run:
        clock.tick(FPS)
        draw_background()

        # Affichage barres et noms
        draw_health_bar(fighter_1.health, 20, 70)
        draw_health_bar(fighter_2.health, 850, 70)
        draw_energy_bar_segments(fighter_1.energy, 20, 110)
        draw_energy_bar_segments(fighter_2.energy, 850, 110)
        # Icônes étoiles pour le score
        stars_p1 = "💥" * score[0]
        stars_p2 = "💥" * score[1]

        # Afficher noms + étoiles
        draw_text(f"{selected_players['J1']}  {stars_p1}", emoji_font, WHITE, 20, 20)
        draw_text(f"{stars_p2}  {selected_players['J2']}", emoji_font, WHITE, 850, 20)

        if intro_count <= 0:
            # Mouvements et update
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)

            # Attaques ultimes
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and fighter_1.energy == 100:
                direction = 1 if not fighter_1.flip else -1
                name = selected_players["J1"]
                ult = ultimate_projectiles[name]

                # Point de départ ajusté vers le haut du corps
                proj_x = fighter_1.rect.centerx
                proj_y = fighter_1.rect.centery - 70  # Ajuste ici si besoin

                projectiles.append(
                    Projectile(proj_x, proj_y, direction, ult["frames"], ult["speed"], ult["damage"], fighter_1))
                fighter_1.energy = 0

            if keys[pygame.K_KP3] and fighter_2.energy == 100:
                direction = 1 if not fighter_2.flip else -1
                name = selected_players["J2"]
                ult = ultimate_projectiles[name]

                proj_x = fighter_2.rect.centerx
                proj_y = fighter_2.rect.centery - 70  # Même principe

                projectiles.append(
                    Projectile(proj_x, proj_y, direction, ult["frames"], ult["speed"], ult["damage"], fighter_2))
                fighter_2.energy = 0

            # Projectiles
            for projectile in projectiles:
                projectile.update()
                projectile.draw(screen)
                if projectile.owner == fighter_1:
                    projectile.check_collision(fighter_2)
                else:
                    projectile.check_collision(fighter_1)
            projectiles[:] = [p for p in projectiles if p.active]

            # Update perso
            fighter_1.update()
            fighter_2.update()
            fighter_1.draw(screen)
            fighter_2.draw(screen)

            # Round terminé ?
            if not round_over:
                if not fighter_1.alive:
                    score[1] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not fighter_2.alive:
                    score[0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                # Fin de partie, au meilleur des 3 manches
                if score[0] == 3 or score[1] == 3:
                    screen.blit(victory, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    run = False
                elif pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    reset_round()
        else:
            draw_text(str(intro_count), count_font, BLUE, 540, 200)
            draw_text(str(intro_count), count_font, WHITE, 535, 195)
            # Affichage du compte à rebours
            count_sound="assets/sounds/count_sound 2.mp3"
            count_fx = pygame.mixer.Sound(count_sound)
            count_fx.play()
            if pygame.time.get_ticks() - last_count_update >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()
    pygame.quit()

def main_menu():
    """Menu principal du jeu avec bouton interactif."""
    running = True
    while running:
        screen.blit(background_menu, (0, 0))
        screen.blit(button_image, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                select_player()
                main_gameplay()
                return

        pygame.display.flip()
    pygame.quit()


# Lancer le menu principal
main_menu()
