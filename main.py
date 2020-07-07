#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

class Cube:
    rows = 20
    def __init__(self, position):
        self.pos = position

    def move(self, dirx, diry):
        pass

class Snake:
    # Class attributes
    body = []    # This is where we stage all snake cubes.
    turns = {}   # Holds in memory all the points where the user changed the direction. These points stands still. Dict structure
                 # will look like this - (point where snake turns) : (direction of the turn)



    def __init__(self, pos, color = (255, 0, 0)):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)  # This instruction is responsible to make the first block of the snake -> head
        self.dirx = 0
        self.diry = -1

    def move(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]


                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]


                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

            for i, cube in enumerate(self.body): #Iteration on snake's cubes
                position_of_cube = cube.pos[:]

                if position_of_cube in self.turns: # If the cube reach the point of the turn
                    turn = self.turns[position_of_cube] # We are taking direction of the turn at that point
                    cube.move(turn[0], turn[1]) # And we are changing direction of the cube

                    if i == len(self.body) - 1:
                        self.turns.pop(position_of_cube) # If this is the last block we remove the point from the list of turns

                else:
                    # If we reach the edge of the screen we come back on the opposite side
                    if self.dirx == 1 and cube.pos[0] >= (cube.rows - 1): cube.pos[0] = 0
                    elif self.dirx == -1 and cube.pos[0] <= 0: cube.pos[0] = (cube.rows - 1)
                    elif self.diry == 1 and cube.pos[0] >= (cube.rows - 1): cube.pos[1] = 0
                    elif self.diry == -1 and cube.pos[0] <= 0: cube.pos[1] = (cube.rows - 1)

                    else: cube.move(self.dirx, self.diry) # If nothing happen we move in the current direction



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
    start = (10, 10)
    screen = pygame.display.set_mode((window_size, window_size))

    snake = Snake(start)

    # Game loop
    while True:

        ref_scrn(screen, window_size, rows)
        snake.move()




main()