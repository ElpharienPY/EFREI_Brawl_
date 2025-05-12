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

# Window config
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arène")

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# FPS CONTROL
clock = pygame.time.Clock()
FPS = 60

# Musics and sound fx
music_folder = "assets/sounds/music_folder"
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

shake = 0
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

#define animation
WARRIOR_ANIMATION_STEPS= [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS= [8,8,2,8,8,3,7]
KING_ANIMATION_STEPS= [6,8,2,6,6,4,11]
FIGHTER_ANIMATION_STEPS= [8,8,2,6,6,4,6]

# Count
count_font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 400)
score_font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 50)
round_over = False

# Lobby music
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/lobby_sound.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Window configuration
WIDTH, HEIGHT = 1280, 720
pygame.display.set_caption("Menu du Jeu")

# Loading interface images
background_menu = pygame.image.load("assets/images/menu_background.png")
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))
button_image = pygame.image.load("assets/images/button_1v1.png")
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
control_select_background = pygame.image.load("assets/images/control_select_background.png").convert()
control_select_background = pygame.transform.scale(control_select_background, (WIDTH, HEIGHT))

background_select = pygame.image.load("assets/images/characters_select.png")
background_select = pygame.transform.scale(background_select, (WIDTH, HEIGHT))

# Addition of dedicated funds for player selection
player1_screen = pygame.image.load("assets/images/player1_select.png")
player1_screen = pygame.transform.scale(player1_screen, (WIDTH, HEIGHT))

player2_screen = pygame.image.load("assets/images/player2_select.png")
player2_screen = pygame.transform.scale(player2_screen, (WIDTH, HEIGHT))

# Liste of characters and images
character_names = ["M.Rado", "M.Chahine", "Gabi", "M.Kais"]
character_images = [
    pygame.image.load("assets/images/assets_1_(Rado).png"),
    pygame.image.load("assets/images/assets_2_(Chahine).png"),
    pygame.image.load("assets/images/assets_3_(Morgadp).png"),
    pygame.image.load("assets/images/secret_character.png"),
]

# Scale characters images
character_width, character_height = 150, 250
character_images = [pygame.transform.scale(img, (character_width, character_height)) for img in character_images]

# Coordinates of characters
character_positions = [
    (WIDTH // 2 - 378, HEIGHT // 2 - 265),
    (WIDTH // 2 - 172, HEIGHT // 2 - 265),
    (WIDTH // 2 + 28, HEIGHT // 2 - 265),
    (WIDTH // 2 + 228, HEIGHT // 2 - 265)
]

# Storage of player choices in index form
selected_players = {"J1": None, "J2": None}

# Dictionary of character introduction videos
character_videos = {
    "M.Rado": "assets/vidéos/Rado_intro.mp4",
    "M.Chahine": "assets/vidéos/Chahine_intro.mp4",
    "Gabi": "assets/vidéos/Gabi_intro.mp4",
    "M.Kais": "assets/vidéos/Kais_intro.mp4"
}

# Dictionary of characters and associated data
character_data = {
    "M.Rado": {"data": FIGHTER_DATA, "sheet": fighter_sheet, "animation_steps": FIGHTER_ANIMATION_STEPS, "effect": punch_fx},
    "M.Chahine": {"data": KING_DATA, "sheet": king_sheet, "animation_steps": KING_ANIMATION_STEPS, "effect": sword_fx},
    "Gabi": {"data": WARRIOR_DATA, "sheet": warrior_sheet, "animation_steps": WARRIOR_ANIMATION_STEPS, "effect": electricity_fx},
    "M.Kais": {"data": WIZARD_DATA, "sheet": wizard_sheet, "animation_steps": WIZARD_ANIMATION_STEPS, "effect": magic_fx},
}

# Loading spritesheets bullet
def load_frames_from_sheet(sheet, frame_width, frame_height, count, scale=1):
    frames = []
    for i in range(count):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        if scale != 1:
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)
    return frames

# Ultimate attack data
fireball_sheet = pygame.image.load("assets/images/blue_fireball/blue_fireball.png").convert_alpha()
fireball_frames = load_frames_from_sheet(fireball_sheet, 52, 52, 6, scale=9)

lightning_sheet = pygame.image.load("assets/images/lightning/lightning.png").convert_alpha()
lightning_frames = load_frames_from_sheet(lightning_sheet, 42, 42, 6, scale=9)

magic_sheet = pygame.image.load("assets/images/magic_spe/magic_spe.png").convert_alpha()
magic_frames = load_frames_from_sheet(magic_sheet, 50, 50, 6, scale=8)

# Ultimate attack/character association
ultimate_projectiles = {
    "M.Rado": {
        "frames": fireball_frames,
        "speed": 15,
        "damage": 25
    },
    "M.Chahine": {
        "frames": magic_frames,
        "speed": 25,
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

ultimate_sounds = {
    "M.Rado": {
        "cast": pygame.mixer.Sound("assets/sounds/rado_cast.mp3"),
        "hit": pygame.mixer.Sound("assets/sounds/rado_hit.mp3")
    },
    "M.Chahine": {
        "cast": pygame.mixer.Sound("assets/sounds/chahine_cast.mp3"),
        "hit": pygame.mixer.Sound("assets/sounds/chahine_hit.mp3")
    },
    "Gabi": {
        "cast": pygame.mixer.Sound("assets/sounds/gabi_cast.mp3"),
        "hit": pygame.mixer.Sound("assets/sounds/gabi_hit.mp3")
    },
    "M.Kais": {
        "cast": pygame.mixer.Sound("assets/sounds/kais_cast.mp3"),
        "hit": pygame.mixer.Sound("assets/sounds/kais_hit.mp3")
    }
}
for sounds in ultimate_sounds.values():
    sounds["cast"].set_volume(0.7)
    sounds["hit"].set_volume(0.9)

def play_video(video_path):
    """Play a video directly in the Pygame window."""
    if not os.path.exists(video_path):
        print(f"⚠️ Erreur : Le fichier vidéo {video_path} est introuvable.") #Vérification présence de la vidéo
        return

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"⚠️ Erreur : Impossible d'ouvrir la vidéo {video_path}.")
        return

    delay = pygame.time.Clock()

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

        delay.tick(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()

    cap.release()
    cv2.destroyAllWindows()

control_modes = {"J1": "clavier", "J2": "clavier"}

def choose_controls():
    """Choose between joystick and keyboard"""
    global control_modes

    font = pygame.font.Font("assets/fonts/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 55)

    for player in ["J1", "J2"]:
        choosing = True
        mode = "clavier"

        while choosing:
            screen.blit(control_select_background, (0, 0))
            draw_text(f"{player} : Choisis", font, WHITE, 430, 180)

            draw_text("Clavier", font, WHITE if mode == "clavier" else (13, 235, 254), 155, 360)
            draw_text("Manette", font, WHITE if mode == "manette" else (13, 235, 254), 855, 360)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        mode = "clavier"
                    elif event.key == pygame.K_RIGHT:
                        mode = "manette"
                    elif event.key == pygame.K_RETURN:
                        control_modes[player] = mode
                        choosing = False



def select_player():
    """Screen to choose players."""
    global selected_players

    # Wait for J1
    screen.blit(player1_screen, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                waiting = False  # J1 press "1"

    select_character("J1")  # Selection of characters for player 1

    # Wait for J2
    screen.blit(player2_screen, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                waiting = False  # J2 press "2"

    select_character("J2")  # Selection of characters for player 2

    pygame.mixer.music.stop()

def select_character(player_key):
    """Character selection screen with dictionary storage."""
    global selected_players, fighter_1, fighter_2
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
                    selected_players[player_key] = character_names[selected_index]
                    running = False

        pygame.display.flip()

    # Retrieve data for the selected character
    chosen_character = selected_players[player_key]
    character_info = character_data[chosen_character]

    # Intelligent joystick_id assignment
    joystick_id = None
    nb_manettes = pygame.joystick.get_count()

    if control_modes[player_key] == "manette":
        if player_key == "J1":
            if nb_manettes >= 1:
                joystick_id = 0
            else:
                print("⚠️ No controller detected for Player 1")
        elif player_key == "J2":
            if control_modes["J1"] == "manette":
                if nb_manettes >= 2:
                    joystick_id = 1
                else:
                    print("⚠️ Only one controller detected, already in use by Player 1")
            else:
                if nb_manettes >= 1:
                    joystick_id = 0
                else:
                    print("⚠️ No controller detected for Player 2")

    # Initialisation of the player
    if player_key == "J1":
        fighter_1 = Player(
            1, 200, 480, False,
            character_info["data"],
            character_info["sheet"],
            character_info["animation_steps"],
            character_info["effect"],
            control_mode=control_modes["J1"],
            joystick_id=joystick_id
        )
    else:
        fighter_2 = Player(
            2, 1000, 500, True,
            character_info["data"],
            character_info["sheet"],
            character_info["animation_steps"],
            character_info["effect"],
            control_mode=control_modes["J2"],
            joystick_id=joystick_id
        )

    # Intro video
    if chosen_character in character_videos:
        play_video(character_videos[chosen_character])

    if player_key == "J1":
        print(f"🧑‍🎮 Player 1 choose : {chosen_character} with {control_modes['J1']} (Joystick {joystick_id})")
    else:
        print(f"🧑‍🎮 Player 2 choose : {chosen_character} with {control_modes['J2']} (Joystick {joystick_id})")


# Functions
def draw_text(text, font, text_col, x, y):
    """Display text on whatever is necessary."""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_background():
    """Display background."""
    screen.blit(background, (0, 0))

def draw_health_bar(health, x, y):
    """Display health bar."""
    ratio = health / 100
    screen.blit(versus, (0, 0))
    pygame.draw.rect(screen, RED, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, WHITE, (x, y, 400, 30))
    pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, 400 * ratio, 30))

def check_game_over():
    """Best-of-5-rounds (BO5) combat system"""
    if score[0] == 3:
        return "Joueur 1 Gagne !"
    elif score[1] == 3:
        return "Joueur 2 Gagne !"
    return None

# Dictionary of associations between characters and their data
character_mapping = {
    "M.Rado": (FIGHTER_DATA, fighter_sheet, FIGHTER_ANIMATION_STEPS, punch_fx),
    "M.Chahine": (KING_DATA, king_sheet, KING_ANIMATION_STEPS, sword_fx),
    "Gabi": (WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, electricity_fx),
    "M.Kais": (WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx),
}

def reset_round():
    """Resets the round taking into account the selected characters."""
    global fighter_1, fighter_2, intro_count, round_over, rounds_joues

    rounds_joues += 1
    intro_count = 3
    round_over = False

    # Retrieving players choices
    player1_choice = selected_players["J1"]
    player2_choice = selected_players["J2"]

    p1_data, p1_sheet, p1_steps, p1_fx = character_mapping[player1_choice]
    p2_data, p2_sheet, p2_steps, p2_fx = character_mapping[player2_choice]

    nb_manettes = pygame.joystick.get_count()
    joystick_id_1 = None
    joystick_id_2 = None

    # Intelligent joystick assignment (as in select_character)
    if control_modes["J1"] == "manette":
        if nb_manettes >= 1:
            joystick_id_1 = 0
        else:
            print("⚠️ No controller available for Player 1")

    if control_modes["J2"] == "manette":
        if control_modes["J1"] == "manette":
            if nb_manettes >= 2:
                joystick_id_2 = 1
            else:
                print("⚠️ Only one controller available, already used by Player 1")
        else:
            if nb_manettes >= 1:
                joystick_id_2 = 0
            else:
                print("⚠️ No controller available for Player 2")

    # Player creation with dynamic joysticks
    fighter_1 = Player(
        1, 200, 480, False,
        p1_data, p1_sheet, p1_steps, p1_fx,
        control_mode=control_modes["J1"],
        joystick_id=joystick_id_1
    )

    fighter_2 = Player(
        2, 1000, 500, True,
        p2_data, p2_sheet, p2_steps, p2_fx,
        control_mode=control_modes["J2"],
        joystick_id=joystick_id_2
    )


# Segmented energy gauge gold color
def draw_energy_bar_segments(energy, x, y):
    """Generates dynamic attack bars"""
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

# Global variables
fighter_1 = None
fighter_2 = None
projectiles = []
score = [0, 0]
round_over = False

intro_count = 4
last_count_update = pygame.time.get_ticks()
rounds_joues = 0
MAX_ROUNDS = 5
ROUND_OVER_COOLDOWN = 2000

emoji_font=pygame.font.SysFont("segoeuiemoji", 40)

def trigger_shake(intensity):
    """Screen hake"""
    global shake
    shake = intensity

def pause_menu(background_snapshot):
    """In-game interactive pause menu"""
    pause_font = pygame.font.Font("assets/fonts/neo-latina-demo-FFP.ttf", 55)
    menu_options = ["Reprendre", "Menu", "Quitter"]
    selected = 0
    running = True

    # Creating button rectangles
    button_rects = []
    for i in range(len(menu_options)):
        rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 250 + i * 100, 300, 70)
        button_rects.append(rect)

    while running:
        # Display the frozen background of the game
        screen.blit(background_snapshot, (0, 0))

        # Semi-transparent gray overlay
        gray_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        gray_overlay.fill((50, 50, 50, 180))  # dark grey semi-transparent
        screen.blit(gray_overlay, (0, 0))

        # Button design
        for i, rect in enumerate(button_rects):
            if rect.collidepoint(pygame.mouse.get_pos()):
                selected = i

            color = (200, 200, 200) if i == selected else (100, 100, 100)
            pygame.draw.rect(screen, color, rect, border_radius=8)

            # Text centered in button
            text_surf = pause_font.render(menu_options[i], True, BLUE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()

        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        print("↩️ continue")
                        return "resume"
                    elif selected == 1:
                        print("↩️ Back to main menu")
                        return "menu"
                    elif selected == 2:
                        print("↩️ End of game")
                        pygame.quit()
                        exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left clic
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                return "resume"
                            elif i == 1:
                                return "menu"
                            elif i == 2:
                                pygame.quit()
                                exit()

def main_gameplay():
    """Main function of the game"""
    global round_over, score, intro_count, last_count_update, rounds_joues, countdown_started, count_start_time, count_complete, shake, fighter_1, fighter_2

    run = True
    round_over_time = 0
    count_complete = False

    reset_round()

    check_music = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    if check_music:
        random_music = random.choice(check_music)
        mp3_folder = os.path.join(music_folder, random_music)
        pygame.mixer.music.load(mp3_folder)
        pygame.mixer.music.play(-1, 0.0, 5000)

    countdown_started = False
    count_start_time = 0

    while run:
        clock.tick(FPS)
        if shake > 0:
            shake_x = random.randint(-10, 10)
            shake_y = random.randint(-10, 10)
            screen.blit(background, (shake_x, shake_y))
            shake -= 1
        else:
            draw_background()

        # Display bars and names
        draw_health_bar(fighter_1.health, 20, 70)
        draw_health_bar(fighter_2.health, 850, 70)
        draw_energy_bar_segments(fighter_1.energy, 20, 110)
        draw_energy_bar_segments(fighter_2.energy, 850, 110)
        # Stars for the score
        stars_p1 = "💥" * score[0]
        stars_p2 = "💥" * score[1]

        # Display names + stars
        draw_text(f"{selected_players['J1']}  {stars_p1}", emoji_font, WHITE, 20, 20)
        draw_text(f"{stars_p2}  {selected_players['J2']}", emoji_font, WHITE, 850, 20)

        if intro_count <= 0:
            # Movements and updates
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)

            # Ultimate attacks
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and fighter_1.energy == 100:
                direction = 1 if not fighter_1.flip else -1
                name = selected_players["J1"]
                ult = ultimate_projectiles[name]

                # Starting point adjusted towards the top of the body
                proj_x, proj_y = fighter_1.get_projectile_origin()  # Same principle
                ultimate_sounds[name]["cast"].play()
                projectiles.append(Projectile(proj_x, proj_y, direction, ult["frames"], ult["speed"], ult["damage"], fighter_1, name, hit_sound=ultimate_sounds[name]["hit"],trigger_shake=trigger_shake))
                fighter_1.energy = 0
                print(f"💥 {selected_players['J1']} has launched its ultimate attack !")

            if fighter_1.control_mode == "manette" and fighter_1.joystick:
                if fighter_1.joystick.get_button(3) and fighter_1.energy == 100:
                    name = selected_players["J1"]
                    ult = ultimate_projectiles[name]
                    hit_sound = ultimate_sounds[name]["hit"]
                    proj_x, proj_y = fighter_1.get_projectile_origin()
                    projectiles.append(
                        Projectile(proj_x, proj_y, 1 if not fighter_1.flip else -1, ult["frames"], ult["speed"],
                                   ult["damage"], fighter_1, name, hit_sound, trigger_shake))
                    ultimate_sounds[name]["cast"].play()
                    fighter_1.energy = 0
                    print(f"💥 {selected_players['J1']} has launched its ultimate attack !")

            if keys[pygame.K_KP3] and fighter_2.energy == 100:
                direction = 1 if not fighter_2.flip else -1
                name = selected_players["J2"]
                ult = ultimate_projectiles[name]

                proj_x, proj_y = fighter_2.get_projectile_origin() # Same principle
                ultimate_sounds[name]["cast"].play()
                projectiles.append(Projectile(proj_x, proj_y, direction, ult["frames"], ult["speed"], ult["damage"], fighter_2, name, hit_sound=ultimate_sounds[name]["hit"],trigger_shake=trigger_shake))
                fighter_2.energy = 0
                print(f"💥 {selected_players['J2']} has launched its ultimate attack !")

            # J2 ultimate attack via joystick
            if fighter_2.control_mode == "manette" and fighter_2.joystick:
                if fighter_2.joystick.get_button(3) and fighter_2.energy == 100:
                    name = selected_players["J2"]
                    ult = ultimate_projectiles[name]
                    hit_sound = ultimate_sounds[name]["hit"]
                    proj_x, proj_y = fighter_2.get_projectile_origin()
                    projectiles.append(
                        Projectile(proj_x, proj_y, 1 if not fighter_2.flip else -1, ult["frames"], ult["speed"],
                                   ult["damage"], fighter_2, name, hit_sound, trigger_shake))
                    ultimate_sounds[name]["cast"].play()
                    fighter_2.energy = 0
                    print(f"💥 {selected_players['J2']} has launched its ultimate attack !")

            # Bullet
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

            # Round finish ?
            if not round_over:
                if not fighter_1.alive:
                    score[1] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                    shake = 50
                    print(f"🏁 Round win by Joueur 2 ({selected_players['J2']})")
                elif not fighter_2.alive:
                    score[0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                    shake = 50
                    print(f"🏁 Round win by Joueur 1 ({selected_players['J1']})")

            else:
                # End of game, best of 3 rounds
                if score[0] == 3 or score[1] == 3:
                    screen.blit(victory, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    run = False
                elif pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    reset_round()
        else:
            # Countdown display
            count_sound="assets/sounds/count_sound0.mp3"
            count_fx = pygame.mixer.Sound(count_sound)
            if not countdown_started:
                count_fx.play()
                count_start_time = pygame.time.get_ticks()
                countdown_started = True

            elapsed_time = pygame.time.get_ticks() - count_start_time

            if elapsed_time < 900:
                draw_text("3", count_font, BLUE, 540, 200)
                draw_text("3", count_font, WHITE, 535, 195)
            elif elapsed_time < 1500:
                draw_text("2", count_font, BLUE, 540, 200)
                draw_text("2", count_font, WHITE, 535, 195)
            elif elapsed_time < 1900:
                draw_text("1", count_font, BLUE, 540, 200)
                draw_text("1", count_font, WHITE, 535, 195)
            elif elapsed_time < 2400:
                draw_text("GO!", count_font, BLUE, 340, 200)
                draw_text("GO!", count_font, WHITE, 335, 195)
            else:
                intro_count = 0  # End of countdown

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_screen = screen.copy()
                    action = pause_menu(paused_screen)
                    if action == "menu":
                        pygame.mixer.music.stop()  # Stop combat music
                        pygame.mixer.music.load("assets/sounds/lobby_sound.wav")
                        pygame.mixer.music.fadeout(1000)  # Fade to 1 second
                        pygame.time.delay(1000)  # Wait till the fade is over

                        pygame.mixer.music.load("assets/sounds/lobby_sound.wav")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)

                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)

                        select_player()
                        main_gameplay()
                        return
                    elif action == "resume":
                        continue  # Resume play
        pygame.display.flip()

def main_menu():
    """Main game menu with interactive button."""
    running = True
    while running:
        screen.blit(background_menu, (0, 0))
        screen.blit(button_image, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                choose_controls()
                select_player()
                main_gameplay()
                return

        pygame.display.flip()
    pygame.quit()

# Launch main
if __name__ == "__main__":
    main_menu()
