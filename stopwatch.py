# Фазульзянов Амир

import pygame

FPS = 60

time_seconds = 0  # перед игровым циклом

# после игрового цикла
clock = pygame.time.Clock()
time_millis = clock.tick(30)
time_seconds += time_millis / 1000