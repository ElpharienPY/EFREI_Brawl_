import numpy as np
import pygame
import os
from ffpyplayer.player import MediaPlayer
import cv2

screen = pygame.display.set_mode((1280, 720))

def play_video(video_path):
    """Jouer une vidéo OpenCV dans Pygame avec le son."""
    if not os.path.exists(video_path):
        print(f"⚠️ Erreur : Le fichier vidéo {video_path} est introuvable.")
        return

    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)  # Lecture de l'audio

    if not cap.isOpened():
        print(f"⚠️ Erreur : Impossible d'ouvrir la vidéo {video_path}.")
        return

    clock = pygame.time.Clock()

    while cap.isOpened():
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()  # Gestion de l'audio

        if not ret:
            print("✅ Fin de la vidéo.")
            break

        # Convertir BGR (OpenCV) en RGB (Pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Redimensionner l'image pour la fenêtre Pygame
        frame = cv2.resize(frame, (1280, 720))

        # Corriger l'orientation de l'image
        frame = np.transpose(frame, (1, 0, 2))  # Rotation correcte

        # Convertir l'image en surface Pygame
        frame_surface = pygame.surfarray.make_surface(frame)

        # Afficher la vidéo dans Pygame
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        # Lire l'audio synchronisé avec la vidéo
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame  # t = timestamp audio
        elif val == 'eof':
            break

        clock.tick(25)

        # Gestion des événements pour quitter proprement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()

    cap.release()
    cv2.destroyAllWindows()
play_video("assets/vidéos/Gabi_intro.mp4")