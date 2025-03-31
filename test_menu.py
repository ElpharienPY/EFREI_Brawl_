import pygame
import cv2
import os
import numpy as np

# Initialisation de Pygame
pygame.init()

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


def play_video(video_path):
    """Jouer une vidéo OpenCV directement dans la fenêtre Pygame."""
    if not os.path.exists(video_path):
        print(f"⚠️ Erreur : Le fichier vidéo {video_path} est introuvable.")
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
                    selected_players[player_key] = selected_index
                    running = False

        pygame.display.flip()

    # Jouer la vidéo du personnage sélectionné
    char_name = character_names[selected_players[player_key]]
    if char_name in character_videos:
        play_video(character_videos[char_name])

    print(f"{player_key} a choisi : {char_name} (Index {selected_players[player_key]})")


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
                return

        pygame.display.flip()

    pygame.quit()


# Lancer le menu principal
main_menu()


