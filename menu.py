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

# Chargement des personnages
character_images = [
    pygame.image.load("assets/images/assets_1_(Rado).png"),
    pygame.image.load("assets/images/test_joueur2.png"),
    pygame.image.load("assets/images/assets_3_(Morgadp).png"),
    pygame.image.load("assets/images/test_joueur4.png"),
]
character_names = ["M.Rado", "M.Chahine", "Gabi", "M.Kais"]

# Dictionnaire associant chaque personnage à une vidéo spécifique
character_videos = {
    "M.Rado": "assets/vidéos/Rado_intro.mp4",
    "M.Chahine": "assets/vidéos/Chahine_intro.mp4",
    "Gabi": "assets/vidéos/Gabi_intro.mp4",
    "M.Kais": "assets/vidéos/Kais.mp4"
}

# Redimensionner les images des personnages
character_width, character_height = 150, 250
character_images = [pygame.transform.scale(img, (character_width, character_height)) for img in character_images]

# Coordonnées des personnages
character_positions = [
    (WIDTH // 2 - 378, HEIGHT // 2 - 265),
    (WIDTH // 2 - 172, HEIGHT // 2 - 265),
    (WIDTH // 2 + 28, HEIGHT // 2 - 265),
    (WIDTH // 2 + 228, HEIGHT // 2 - 265)
]

# Sélections des joueurs
player1 = None
player2 = None


def play_video(video_path):
    """Jouer une vidéo OpenCV directement dans la fenêtre Pygame."""

    # Vérification si le fichier existe
    if not os.path.exists(video_path):
        print(f"⚠️ Erreur : Le fichier vidéo {video_path} est introuvable.")
        return

    cap = cv2.VideoCapture(video_path)

    # Vérifier si la vidéo est bien ouverte
    if not cap.isOpened():
        print(f"⚠️ Erreur : Impossible d'ouvrir la vidéo {video_path}.")
        return

    clock = pygame.time.Clock()  # Pour contrôler le framerate

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("✅ Fin de la vidéo.")
            break

        # Convertir BGR (OpenCV) en RGB (Pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Redimensionner l'image à la taille de la fenêtre
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        # Convertir l'image en surface Pygame
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))

        # Affichage dans la fenêtre Pygame
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        # Contrôle du framerate (~60 fps)
        clock.tick(60)

        # Gérer les événements Pygame (pour quitter proprement)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()

    cap.release()
    cv2.destroyAllWindows()


def select_player():
    """Écran pour choisir les joueurs."""
    global player1, player2

    screen.blit(player1_screen, (0, 0))
    pygame.display.flip()

    while player1 is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                player1 = "Joueur 1"

    screen.blit(player2_screen, (0, 0))
    pygame.display.flip()

    while player2 is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                player2 = "Joueur 2"

    select_character(1)  # Sélection du personnage du Joueur 1


def select_character(player_num):
    """Écran pour choisir un personnage."""
    selected_index = 0
    running = True

    while running:
        screen.blit(background_select, (0, 0))

        for i, (img, pos) in enumerate(zip(character_images, character_positions)):
            screen.blit(img, pos)
            if i == selected_index:
                pygame.draw.rect(screen, (255, 215, 0), (pos[0] - 5, pos[1] - 5, character_width + 10, character_height + 10), 5)

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
                    global player1, player2
                    if player_num == 1:
                        player1 = character_names[selected_index]
                        print(f"Joueur 1 a choisi : {player1}")
                        select_character(2)  # Sélection du Joueur 2
                    else:
                        player2 = character_names[selected_index]
                        print(f"Joueur 2 a choisi : {player2}")
                        running = False

        pygame.display.flip()

    # Lancement des vidéos après sélection des deux joueurs
    if player1 in character_videos and character_videos[player1]:
        play_video(character_videos[player1])

    if player2 in character_videos and character_videos[player2]:
        play_video(character_videos[player2])

    exit()


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
