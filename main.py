#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

class Snake:
    def __init__(self):
        pass

    def move(self):
        pass

    def add_cube(self):
        pass



def draw_grid(surface, window_size: int, rows: int) -> None:
    # Draws grid on the screen.

    size_between = window_size // rows

    x = 0
    y = 0

    for i in range (rows):
        x += size_between
        y += size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, window_size))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (window_size, y))


def ref_scrn(surface, window_size, rows) -> None:
    # Funkcja jest odpowiedzialna za odświeżanie ekranu.
    # todo - Probably it will be responsible for rendering the snake and his food. But i need to figure it out
    surface.fill((0, 0, 0))
    draw_grid(surface, window_size, rows)
    pygame.display.update()


def main():
    window_size = 500   #It's going to be square all the time
    rows = 20
    screen = pygame.display.set_mode((window_size, window_size))

    while True:

        ref_scrn(screen, window_size, rows)





main()