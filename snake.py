import pygame as pg
import sys
import math
import numpy as np
import random

clock = pg.time.Clock()

#### pálya atatai
n_blocks_x = 17
n_blocks_y = 15
block_w = 32
block_h = 32
edge = 28
win_x = n_blocks_x * block_w + 2 * edge
win_y = n_blocks_y * block_h + 2 * edge
score = 0

#### snake variables
blue = (77, 145, 213)
snake_w = 30
snake_x = int(edge + 9 * (block_w / 2))
snake_y = int(edge + 15 * (block_h / 2))
length = 3
snake_o = 1  ## True = x     False = y
snake_parts = np.array([(snake_x, snake_y, snake_o),
                        ((snake_x - block_w), snake_y, snake_o), ((snake_x - 2 * block_w),snake_y, snake_o)])

#### Fruit
is_fruit = False
red = (255, 0, 0)
fruit_x = int(edge + (13 * 2 - 1) * (block_w / 2))
fruit_y = int(edge + (8 * 2 - 1) * (block_w / 2))

#### ablak beálltása
pg.init()
screen_dim = (win_x, win_y)
screen = pg.display.set_mode(screen_dim)
pg.display.set_caption("Snake by Tuba Balázs")


def create_snake():
    global snake_o, length, snake_parts, snake_x, snake_y, block_w, block_h

    snake_parts[0][0] = snake_x
    snake_parts[0][1] = snake_y
    snake_parts[0][2] = snake_o

    for i in range(length - 1, 0, -1):
        if snake_parts[i][2] == 1:
            snake_parts[i][0] = snake_parts[i][0] + block_w
        elif snake_parts[i][2] == 2:
            snake_parts[i][0] = snake_parts[i][0] - block_w
        elif snake_parts[i][2] == 3:
            snake_parts[i][1] = snake_parts[i][1] - block_h
        elif snake_parts[i][2] == 4:
            snake_parts[i][1] = snake_parts[i][1] + block_h


def draw_snake():
    for i in range(length):
        pg.draw.circle(screen, (0, 0, 255), (snake_parts[i][0], snake_parts[i][1]), 15)


def redraw_game_window():
    # edge
    pg.draw.rect(screen, (121, 179, 46), (0, 0, win_x, win_y))

    #### playing area
    ## light rectangles
    for i in range(math.ceil(n_blocks_x / 2)):
        for y in range(math.ceil(n_blocks_y / 2)):
            pg.draw.rect(screen, (204, 255, 102), (edge + i * 2 * block_w, edge + y * 2 * block_h, block_w, block_h))
    for i in range(math.floor(n_blocks_x / 2)):
        for y in range(math.floor(n_blocks_y / 2)):
            pg.draw.rect(screen, (204, 255, 102),
                         (edge + block_w + i * 2 * block_w, edge + block_h + y * 2 * block_h, block_w, block_h))

    ## dark rectangles
    for i in range(math.floor(n_blocks_x / 2)):
        for y in range(math.ceil(n_blocks_y / 2)):
            pg.draw.rect(screen, (165, 208, 81),
                         (edge + block_w + i * 2 * block_w, edge + block_h * y * 2, block_w, block_h))
    for i in range(math.ceil(n_blocks_x / 2)):
        for y in range(math.floor(n_blocks_y / 2)):
            pg.draw.rect(screen, (165, 208, 81),
                         (edge + i * 2 * block_w, edge + block_h + y * 2 * block_h, block_w, block_h))
    ## score
    font = pg.font.SysFont('calibri', 25)
    text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(text, (win_x / 2 - 35, 5))

    check_fruit()
    create_snake()
    change_snake_orientation()
    draw_fruit()
    # snake
    draw_snake()

    pg.display.update()


def check_key():
    global game_run, is_fruit, snake_x, snake_y, length, snake_parts, score, fruit_y, fruit_x
    keys = pg.key.get_pressed()
    global snake_o
    if keys[pg.K_LEFT] and snake_o != 1:
        snake_o = 2
    if keys[pg.K_RIGHT] and snake_o != 2:
        snake_o = 1
    if keys[pg.K_UP] and snake_o != 4:
        snake_o = 3
    if keys[pg.K_DOWN] and snake_o != 3:
        snake_o = 4
    if keys[pg.K_SPACE]:
        is_fruit = False
        score = 0
        snake_x = int(edge + 9 * (block_w / 2))
        snake_y = int(edge + 15 * (block_h / 2))
        fruit_x = int(edge + (13 * 2 - 1) * (block_w / 2))
        fruit_y = int(edge + (8 * 2 - 1) * (block_w / 2))
        length = 3
        snake_o = 1
        snake_parts = np.array([(snake_x, snake_y, snake_o),
                                ((snake_x - block_w), snake_y, snake_o), ((snake_x - 2 * block_w), snake_y, snake_o)])
        game_run = True


def check_wall():
    global snake_x, snake_y, game_run

    # right
    if snake_o == 1 and snake_x < win_x - edge - block_w / 2:
        snake_x = snake_x + block_w
    elif snake_o == 1 and snake_x >= win_x - edge - block_w / 2:
        game_run = False
    # left
    if snake_o == 2 and snake_x > edge + block_w / 2:
        snake_x = snake_x - block_w
    elif snake_o == 2 and snake_x <= edge + block_w / 2:
        game_run = False
    # up
    if snake_o == 3 and snake_y > edge + block_h / 2:
        snake_y = snake_y - block_h
    elif snake_o == 3 and snake_y <= edge + block_h / 2:
        game_run = False
    # down
    if snake_o == 4 and snake_y < win_y - edge - block_h / 2:
        snake_y = snake_y + block_h
    elif snake_o == 4 and snake_y >= win_y - edge - block_h / 2:
        game_run = False


def check_itself():
    global game_run
    for i in range(4, length):
        if snake_parts[i][0] == snake_parts[0][0] and snake_parts[i][1] == snake_parts[0][1]:
            game_run = False


def draw_fruit():
    global fruit_x, fruit_y

    pg.draw.circle(screen, red, (fruit_x, fruit_y), 15)


def add_new_piece():
    global snake_parts, length

    new_o = snake_parts[length - 1][2]

    if new_o == 1:
        new_x = snake_parts[length - 1][0] - block_w
        new_y = snake_parts[length - 1][1]
    elif new_o == 2:
        new_x = snake_parts[length - 1][0] + block_w
        new_y = snake_parts[length - 1][1]
    elif new_o == 3:
        new_x = snake_parts[length - 1][0]
        new_y = snake_parts[length - 1][1] + block_h
    elif new_o == 4:
        new_x = snake_parts[length - 1][0]
        new_y = snake_parts[length - 1][1] - block_h

    ref = np.append(snake_parts, (new_x, new_y, new_o))
    length = length + 1
    snake_parts = ref.reshape((length, 3))


def check_fruit():
    global score, fruit_x, fruit_y, length
    if snake_x == fruit_x and snake_y == fruit_y:
        score = score + 1

        add_new_piece()

        fruit_x = int(edge + block_w / 2 + random.randint(0, n_blocks_x - 1) * block_w)
        fruit_y = int(edge + block_h / 2 + random.randint(0, n_blocks_y - 1) * block_h)

    draw_fruit()


def change_snake_orientation():
    global length
    for i in range(length - 1, 0, -1):
        snake_parts[i][2] = snake_parts[i - 1][2]


def end_screen():

    ## backgound
    pg.draw.rect(screen, (121, 179, 46), (0, 0, win_x, win_y))

    ## message
    font_1 = pg.font.SysFont('calibri', 60)
    font_2 = pg.font.SysFont('calibri', 40)
    font_3 = pg.font.SysFont('calibri', 20)

    text_p_1 = (178, 170)
    text_p_2 = (190, 250)
    text_p_3 = (230, 500)

    text_1 = "Game Over!"
    text_2 = "Your score was " + str(score)
    text_3 = "Press space to restart"

    screen.blit(font_1.render(text_1, True, (0, 0, 0)), text_p_1)
    screen.blit(font_2.render(text_2, True, (0, 0, 0)), text_p_2)
    screen.blit(font_3.render(text_3, True, (0, 0, 0)), text_p_3)

    pg.display.update()


game_run = True
## MAIN
while True:
    pg.time.delay(100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    while game_run:
        clock.tick(7)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        check_key()
        check_wall()

        if length >= 4:
            check_itself()

        redraw_game_window()
    end_screen()
    check_key()



