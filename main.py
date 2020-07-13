#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
running = True


class Button:
    def __init__(self, x, y, width, height, color=(0, 0, 255), text="", text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self, screen, font_size=0, outline=None):  # Draws a rectanle button with opional outline and text
        # Makes Outline 2 pixels wide
        if outline:
            pygame.draw.rect(screen, outline,
                             (self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4))

        # Makes Rectangle
        pygame.draw.rect(screen, self.color, self.rect)

        # This statement puts text in the middle of rectangle
        if self.text != "":
            pygame.font.init()
            my_font = pygame.font.SysFont('Times New Roman', font_size, bold=True)
            scrn_text = my_font.render(self.text, False, self.text_color)
            screen.blit(scrn_text, (self.rect.x + (self.rect.width / 2 - scrn_text.get_width() / 2),
                                    self.rect.y + (self.rect.height / 2 - scrn_text.get_height() / 2)))

    def isOver(self) -> bool:  # Returns true when mouse is over the button
        mx, my = pygame.mouse.get_pos()
        return self.rect.collidepoint(mx, my)

    # When the cursor is above the rectangle it changes color
    def change_color_when_over(self, current_color, color, screen, font_size=0, outline=None):
        if self.isOver():
            self.color = color
            self.draw(screen, font_size, outline)
        else:
            self.color = current_color
            self.draw(screen, font_size, outline)


class Cube:
    rows = 20
    width = 500

    def __init__(self, position: tuple, dirx=0, diry=-1, color=(255, 0, 0)):
        self.pos = position
        self.dirx = dirx
        self.diry = diry
        self.color = color

    def move(self, dirx, diry):  # Moving cube in given durection
        self.dirx = dirx
        self.diry = diry

        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface):  # This function draws a given block
        size = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * size + 1, j * size + 1, size - 2, size - 2))


class Snake:
    # Class attributes
    body = []       # This is where we stage all snake cubes.
    turns = {}      # Holds in memory all the points where the user changed the direction.
    # Dict structure - (point where snake turns) : (direction of the turn)

    def __init__(self, pos, color=(255, 0, 0)):
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
                if self.head.dirx == -1 and len(self.body) > 1:
                    break           # This line makes impossible to press button in opposite direction
                self.dirx = 1
                self.diry = 0
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]

            elif keys[pygame.K_LEFT]:
                if self.head.dirx == 1 and len(self.body) > 1:
                    break
                self.dirx = -1
                self.diry = 0
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]

            elif keys[pygame.K_UP]:
                if self.head.diry == 1 and len(self.body) > 1:
                    break
                self.dirx = 0
                self.diry = -1
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]

            elif keys[pygame.K_DOWN]:
                if self.head.diry == -1 and len(self.body) > 1:
                    break
                self.dirx = 0
                self.diry = 1
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, cube in enumerate(self.body):  # Iteration on snake's cubes
            position_of_cube = cube.pos[:]

            if position_of_cube in self.turns:  # If the cube reach the point of the turn
                turn = self.turns[position_of_cube]  # We are taking direction of the turn at that point
                cube.move(turn[0], turn[1])  # And we are changing direction of the cube

                if i == len(self.body) - 1:
                    self.turns.pop(position_of_cube)  # If this is the last block we remove the point
                    # from the list of turns

            else:
                # If we reach the edge of the screen we come back on the opposite side
                if cube.dirx == 1 and cube.pos[0] >= (cube.rows - 1):
                    cube.pos = (0, cube.pos[1])

                elif cube.dirx == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows - 1, cube.pos[1])

                elif cube.diry == 1 and cube.pos[1] >= (cube.rows - 1):
                    cube.pos = (cube.pos[0], 0)

                elif cube.diry == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows - 1)

                else:
                    cube.move(cube.dirx, cube.diry)  # If nothing happen we move in the current direction

    def add_cube(self):
        tail = self.body[-1]
        dx = tail.dirx
        dy = tail.diry
        # Coordinates of next cube depends on durection whih we are moving. So we have to check four cases

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirx = dx  # we are giving the direction to new added cube
        self.body[-1].diry = dy

    def draw(self, surface):
        for i, cube in enumerate(self.body):
            cube.draw(surface)

    def reset(self):  # resets snake so we can start again
        self.head = Cube((10, 10))
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = -1


def random_food(rows: int, item) -> tuple:  # Returns random coordinates after checking if it's not a snake
    # todo - jak grałem to chyba pojawiały się na weżu więc trzeba sprawdzić czy to na pewno dobrze działa

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if (x, y) not in item.body:
            return x, y


def draw_grid(surface, window_size: int, rows: int):
    # Draws grid on the screen.

    size_between = window_size // rows

    x = 0
    y = 0

    for i in range(rows):
        x += size_between
        y += size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, window_size))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (window_size, y))


def ref_scrn(surface, window_size, rows, snake, food) -> None:
    # Rendering the screen - drawing food, snake and grid.
    surface.fill((0, 0, 0))
    snake.draw(surface)
    food.draw(surface)
    draw_grid(surface, window_size, rows)
    pygame.display.update()


def draw_text(screen, text, size, x, y):  # Draws the text on the screen
    pygame.font.init()
    my_font = pygame.font.SysFont('Times New Roman', size, bold=True)
    scrn_text = my_font.render(text, False, (255, 255, 255))
    screen.blit(scrn_text, (x, y))


def game(screen):
    window_size = 500   # It's going to be square so one parameter is given
    rows = 20
    start = (10, 10)

    snake = Snake(start)
    food = Cube(random_food(rows, snake), color=(0, 255, 0))

    clock = pygame.time.Clock()
    # Game loop

    while running:
        pygame.time.delay(50)
        clock.tick(10)

        snake.move()
        if snake.head.pos == food.pos:  # Checking if we ate the snack, extending the snake, and make another food
            snake.add_cube()
            food = Cube(random_food(rows, snake), color=(0, 255, 0))

        for i, cube in enumerate(snake.body):  # Here we are checking if the user ate the snake and ending the game
            if snake.head.pos == cube.pos and i > 0:
                pygame.time.delay(1000)
                snake.reset()

        ref_scrn(screen, window_size, rows, snake, food)


def main():

    # Making front page of the game - main menu
    window_size = 500
    screen = pygame.display.set_mode((window_size, window_size))
    screen.fill((0, 0, 0))
    draw_text(screen, "Welcome to", 80, 20, 20)
    draw_text(screen, "Snake Pro I", 80, 20, 100)

    # Making game button object
    game_button = Button(125, 250, 250, 70, color=(0, 0, 255), text="Game", text_color=(255, 255, 255))
    game_button.draw(screen, font_size=60, outline=(255, 255, 0))

    # Making LEVEL BUTTONS
    level_button_easy = Button(125, 72.5, 250, 70, text="Easy", text_color=(255, 255, 255))
    level_button_medium = Button(125, 215, 250, 70, text="Medium", text_color=(255, 255, 255))
    level_button_hard = Button(125, 357.5, 250, 70, text="Hard", text_color=(255, 255, 255))

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Changing color if the cursor is over the button
            if event.type == pygame.MOUSEMOTION:
                game_button.change_color_when_over((0, 0, 255), (140, 140, 140), screen,
                                                   font_size=60, outline=(255, 255, 0))

            # If user click the game button he can chose how hard the game should be.
            # So it shows next page with 3 buttons to chose (EASY, MEDIUM and HARD).
            # Code down below describes the next page.
            if event.type == pygame.MOUSEBUTTONDOWN and game_button.isOver():

                screen.fill((0, 0, 0))
                level_button_easy.draw(screen, font_size=60, outline=(255, 255, 0))
                level_button_medium.draw(screen, font_size=60, outline=(255, 255, 0))
                level_button_hard.draw(screen, font_size=60, outline=(255, 255, 0))

                while running:

                    for event_page_2 in pygame.event.get():
                        if event_page_2.type == pygame.QUIT:
                            pygame.quit()

                        # Starts the game on EASY mode
                        if event_page_2.type == pygame.MOUSEBUTTONDOWN and level_button_easy.isOver():
                            game(screen)

                        # Starts the game on MEDIUM mode
                        if event_page_2.type == pygame.MOUSEBUTTONDOWN and level_button_medium.isOver():
                            game(screen)

                        # # Starts the game on HARD mode
                        if event_page_2.type == pygame.MOUSEBUTTONDOWN and level_button_hard.isOver():
                            game(screen)

                        # Check if cursor is over the button. If it is it changes the color of the rectangle
                        if event_page_2.type == pygame.MOUSEMOTION:

                            level_button_easy.change_color_when_over((0, 0, 255), (140, 140, 140), screen,
                                                                     font_size=60, outline=(255, 255, 0))

                            level_button_medium.change_color_when_over((0, 0, 255), (140, 140, 140), screen,
                                                                       font_size=60, outline=(255, 255, 0))

                            level_button_hard.change_color_when_over((0, 0, 255), (140, 140, 140), screen,
                                                                     font_size=60, outline=(255, 255, 0))

                    pygame.display.update()

        pygame.display.update()


main()
