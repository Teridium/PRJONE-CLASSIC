import pygame
import random 

class music:
    def __init__(self):
        pygame.mixer.init()

        self.songs = ['mus\Meanwhile.mp3', 'mus\scott-buckley-moonlight.mp3']

    def update(self):
        self.next_music()

    def next_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(random.choice(self.songs))
            pygame.mixer.music.play()
