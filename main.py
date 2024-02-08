import pygame
from pygame.locals import *
from sys import exit

pygame.init()

# Screen
sc_width = 680
sc_height = 720
screen = pygame.display.set_mode((sc_width, sc_height))
frames = pygame.time.Clock()

# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (180, 180, 180)
red = (210, 0, 0)
yellow = (230, 230, 0)
orange = (240, 110, 0)
green = (0, 100, 0)
blue = (0, 0, 255)

# Elements of the game
start_line_p1, start_line_p2 = (80, 560), (200, 560)
finish_line_p1, finish_line_p2 = (440, 560), (560, 560)
blockSize = 40 # Set the size of the grid block

# Posição inicial dos jogadores
player1_pos = [120, 560]
player2_pos= [160, 560]

# Adicionado velocidade base do jogador
player1_xspeed = 0.5
player1_yspeed = 0.5
player2_xspeed = 0.5
player2_yspeed = 0.5

player1_moving = [0, 0, 0, 0]

# Adicionado velocidade do turno anterior
player1_xacceleration = 0.5
player1_yacceleration = 0.5
player2_xacceleration = 0.5
player2_yacceleration = 0.5

player2_moving = [0, 0, 0, 0]


def draw_grid():

    for x in range(0, sc_width, blockSize):
        for y in range(0, sc_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, green, rect, 1)


def draw_circuit():

    line_left = start_line_p1[1] - blockSize * 3 # 440

    line_right1 = finish_line_p1[1] - blockSize * 6 # 320
    line_right2 = finish_line_p1[1] - blockSize * 7  # 280

    # Linha de partida
    pygame.draw.line(screen, white, start_line_p1, start_line_p2)

    # Linha de chegada
    pygame.draw.line(screen, white, finish_line_p1, finish_line_p2)

    # Linhas retas
    pygame.draw.line(screen, white, start_line_p1, (start_line_p1[0], line_left))
    pygame.draw.line(screen, white, start_line_p2, (start_line_p2[0], line_left))

    pygame.draw.line(screen, white, finish_line_p1, (finish_line_p1[0], line_right1))
    pygame.draw.line(screen, white, finish_line_p2, (finish_line_p2[0], line_right2))

    # Linhas "curvas"

    # Curvas superiores da pista
    pygame.draw.line(screen, white, (80, 440), (80, 440-blockSize))
    pygame.draw.line(screen, white, (80, 400), (80+blockSize, 400 - blockSize))
    pygame.draw.line(screen, white, (120, 360), (120, 360 - blockSize), 2)
    pygame.draw.line(screen, white, (120, 320), (120+blockSize, 320 - blockSize))

    pygame.draw.line(screen, white, (160, 280), (160, 280-blockSize*2))
    pygame.draw.line(screen, white, (160, 200), (160+blockSize, 200-blockSize))

    pygame.draw.line(screen, white, (200, 160), (200 + blockSize, 160))
    pygame.draw.line(screen, white, (240, 160), (240+blockSize, 160 - blockSize))
    pygame.draw.line(screen, white, (280, 120), (280 + blockSize, 120))
    pygame.draw.line(screen, white, (320, 120), (320+blockSize, 120 - blockSize))

    pygame.draw.line(screen, white, (360, 80), (360 + blockSize * 2, 80))

    pygame.draw.line(screen, white, (440, 80), (440 + blockSize*2, 80 + blockSize*2))
    pygame.draw.line(screen, white, (520, 160), (520, 160 + blockSize))
    pygame.draw.line(screen, white, (520, 200), (520 + blockSize, 200 + blockSize))
    pygame.draw.line(screen, white, (560, 240), (560, 240 + blockSize))

    # Curvas inferiores da pista
    pygame.draw.line(screen, white, (200, 440), (200 + blockSize, 440 - blockSize))
    pygame.draw.line(screen, white, (240, 400), (240, 400 - blockSize))
    pygame.draw.line(screen, white, (240, 360), (240 + blockSize * 2, 360 - blockSize * 2))
    pygame.draw.line(screen, white, (320, 280), (320 + blockSize * 2, 280))
    pygame.draw.line(screen, white, (400, 280), (400 + blockSize, 280 + blockSize))


def movement_formula(direction, current_accel):
    # verifica primeiro se é o primeiro turno, se for a aceleração muda dependendo da direção pra n acumular mt
    # velocidade em pouco tempo se for pra cima primeiro, yaccel = 1 e speed sempre vai ser zero; 1+0, se continuar,
    # yaccel = 2 e speed = 0, 2+0 então andar 2 blocos pra frente. se for pra baixo no proximo turno, xaccel = 2 - 1,
    # então andaria 1 bloco pra frente. talvez adicionar uma condição pra accel n ficar 0

    if direction == "left":
        current_accel -= 0.5

    elif direction == "right":
        current_accel += 0.5

    elif direction == "up":
        current_accel += 0.5

    elif direction == "down":
        current_accel -= 0.5

    return current_accel


while True:

    for event in pygame.event.get():
        # Quits if you close the window
        if event.type == QUIT:
            pygame.display.quit()
            exit()

        if event.type == pygame.KEYUP:
            player1_moving[2] += 1

    screen.fill(black)
    draw_grid()
    draw_circuit()

    # Drawing players
    pygame.draw.circle(screen, yellow, player1_pos, 5)
    pygame.draw.circle(screen, blue, player2_pos, 5)

    keys = pygame.key.get_pressed()

    # Controles do jogador 1
    if keys[K_LEFT]:
        player1_moving[0] = 1
    if keys[K_RIGHT]:
        player1_moving[1] = 1
    #if keys[K_UP]:
    #    player1_moving[2] = 1
    if keys[K_DOWN]:
        player1_moving[3] = 1

    # Identifica em qual direção o jogador apertou para andar a cada um bloco
    if player1_moving[0]:
        if player1_xacceleration < 40:
            player1_xacceleration += player1_xspeed
            player1_pos[0] -= player1_xspeed
        else:
            player1_xacceleration = 0
            player1_moving[0] = 0
            player1_xspeed = movement_formula("left", player1_xspeed)

    elif player1_moving[1]:
        if player1_xacceleration < 40:
            player1_xacceleration += player1_xspeed
            player1_pos[0] += player1_xspeed
        else:
            player1_xacceleration = 0
            player1_moving[1] = 0
            player1_xspeed = movement_formula("right", player1_xspeed)

    elif player1_moving[2]:
        if player1_yacceleration < 40:
            player1_yacceleration += player1_yspeed
            player1_pos[1] -= player1_yspeed
        else:
            player1_yacceleration = 0
            player1_moving[2] = 0
            player1_yspeed = movement_formula("up", player1_yspeed)

    elif player1_moving[3]:
        if player1_yacceleration < 40:
            player1_yacceleration += player1_yspeed
            player1_pos[1] += player1_yspeed
        else:
            player1_yacceleration = 0
            player1_moving[3] = 0
            player1_yspeed = movement_formula("down", player1_yspeed)

    # Teclas do jogador 2
    if keys[K_a]:
        player2_moving[0] = 1
    elif keys[K_d]:
        player2_moving[1] = 1
    elif keys[K_w]:
        player2_moving[2] = 1
    elif keys[K_s]:
        player2_moving[3] = 1

    if player2_moving[0]:
        if player2_xacceleration < 40:
            player2_xacceleration += player2_xspeed
            player2_pos[0] -= player2_xspeed
        else:
            player2_xacceleration = 0
            player2_moving[0] = 0
            player2_xspeed = movement_formula("left", player2_xspeed)

    elif player2_moving[1]:
        if player2_xacceleration < 40:
            player2_xacceleration += player2_xspeed
            player2_pos[0] += player2_xspeed
        else:
            player2_xacceleration = 0
            player2_moving[1] = 0
            player2_xspeed = movement_formula("right", player2_xspeed)

    elif player2_moving[2]:
        if player2_yacceleration < 40:
            player2_yacceleration += player2_yspeed
            player2_pos[1] -= player2_yspeed
        else:
            player2_yacceleration = 0
            player2_moving[2] = 0
            player2_yspeed = movement_formula("up", player2_yspeed)

    elif player2_moving[3]:
        if player2_yacceleration < 40:
            player2_yacceleration += player2_yspeed
            player2_pos[1] += player2_yspeed
        else:
            player2_yacceleration = 0
            player2_moving[3] = 0
            player2_yspeed = movement_formula("down", player2_yspeed)

    frames.tick(200)
    pygame.display.update()
    screen.fill(white)