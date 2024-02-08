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
blockSize = 40  # Set the size of the grid block

# Posição inicial dos jogadores
player1_pos = [120, 560]
player2_pos = [160, 560]

# Velocidade dos jogadoresw
player_speed = 2  # Alterado para 1 para atender às regras de aceleração/desaceleração

# Define o circuito
circuit = [
    # Linha de partida
    [(80, 560), (200, 560)],

    # Linha de chegada
    [(440, 560), (560, 560)],

    # Restante do circuito
    [(200, 560), (200, 200)],
    [(200, 200), (560, 200)],
    [(560, 200), (560, 520)],
    [(560, 520), (360, 520)],
    [(360, 520), (360, 440)],
    [(360, 440), (440, 440)],
    [(440, 440), (440, 360)],
    [(440, 360), (320, 360)],
    [(320, 360), (320, 480)],
    [(320, 480), (480, 480)],
    [(480, 480), (480, 320)],
    [(480, 320), (320, 320)],
    [(320, 320), (320, 400)],
    [(320, 400), (440, 400)],
    [(440, 400), (440, 320)],
    [(440, 320), (360, 320)],
    [(360, 320), (360, 280)],
    [(360, 280), (400, 280)],
    [(400, 280), (400, 240)],
    [(400, 240), (320, 240)],
    [(320, 240), (320, 280)],
    [(320, 280), (280, 280)],
    [(280, 280), (280, 240)],
    [(280, 240), (240, 240)],
    [(240, 240), (240, 280)],
    [(240, 280), (200, 280)],
    [(200, 280), (200, 440)],
    [(200, 440), (280, 440)],
    [(280, 440), (280, 360)],
    [(280, 360), (240, 360)],
    [(240, 360), (240, 400)],
    [(240, 400), (280, 400)],
    [(280, 400), (280, 480)],
    [(280, 480), (200, 480)],
    [(200, 480), (200, 560)]
]

def draw_grid():
    for x in range(0, sc_width, blockSize):
        for y in range(0, sc_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, green, rect, 1)

def draw_circuit():
    # Desenha o circuito com linhas mais grossas
    for segment in circuit:
        pygame.draw.line(screen, white, segment[0], segment[1], 5)  # Aumenta a espessura para 5 pixels

def is_inside_circuit(x, y):
    for segment in circuit:
        (x1, y1), (x2, y2) = segment
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            return True
    return False

def check_collision(player_pos):
    # Verifica colisões com os limites do circuito
    return not is_inside_circuit(player_pos[0], player_pos[1])

def check_winner(player_pos):
    # Verifica se algum jogador cruzou a linha de chegada
    return player_pos[0] >= finish_line_p1[0]

def update_position(player_pos, direction):
    # Atualiza a posição do jogador de acordo com a direção
    new_pos = player_pos.copy()
    if direction == "left":
        new_pos[0] -= player_speed
    elif direction == "right":
        new_pos[0] += player_speed
    elif direction == "up":
        new_pos[1] -= player_speed
    elif direction == "down":
        new_pos[1] += player_speed
    return new_pos
#calculo
def apply_acceleration(prev_dir, current_dir):
    # Aplica a regra de "aceleração/desaceleração"
    if current_dir == "up" or current_dir == "down":
        return "horizontal"
    elif current_dir == "left" or current_dir == "right":
        return "vertical"
    elif prev_dir == "up" or prev_dir == "down":
        return "horizontal"
    elif prev_dir == "left" or prev_dir == "right":
        return "vertical"
    else:
        return current_dir

prev_dir_p1 = None
prev_dir_p2 = None

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            exit()

    screen.fill(black)
    draw_grid()
    draw_circuit()

    # Desenha os jogadores
    pygame.draw.circle(screen, yellow, player1_pos, 5)
    pygame.draw.circle(screen, blue, player2_pos, 5)

    keys = pygame.key.get_pressed()

    # Movimento do jogador 1
    if keys[K_LEFT] and prev_dir_p1 != "right":
        player1_pos = update_position(player1_pos, "left")
        prev_dir_p1 = apply_acceleration(prev_dir_p1, "left")
    elif keys[K_RIGHT] and prev_dir_p1 != "left":
        player1_pos = update_position(player1_pos, "right")
        prev_dir_p1 = apply_acceleration(prev_dir_p1, "right")
    elif keys[K_UP] and prev_dir_p1 != "down":
        player1_pos = update_position(player1_pos, "up")
        prev_dir_p1 = apply_acceleration(prev_dir_p1, "up")
    elif keys[K_DOWN] and prev_dir_p1 != "up":
        player1_pos = update_position(player1_pos, "down")
        prev_dir_p1 = apply_acceleration(prev_dir_p1, "down")

    # Movimento do jogador 2
    if keys[K_a] and prev_dir_p2 != "right":
        new_pos = update_position(player2_pos, "left")
        if not check_collision(new_pos):
            player2_pos = new_pos
            prev_dir_p2 = apply_acceleration(prev_dir_p2, "left")
    elif keys[K_d] and prev_dir_p2 != "left":
        new_pos = update_position(player2_pos, "right")
        if not check_collision(new_pos):
            player2_pos = new_pos
            prev_dir_p2 = apply_acceleration(prev_dir_p2, "right")
    elif keys[K_w] and prev_dir_p2 != "down":
        new_pos = update_position(player2_pos, "up")
        if not check_collision(new_pos):
            player2_pos = new_pos
            prev_dir_p2 = apply_acceleration(prev_dir_p2, "up")
    elif keys[K_s] and prev_dir_p2 != "up":
        new_pos = update_position(player2_pos, "down")
        if not check_collision(new_pos):
            player2_pos = new_pos
            prev_dir_p2 = apply_acceleration(prev_dir_p2, "down")

    # Verifica colisões e o vencedor
    if check_collision(player1_pos) or check_collision(player2_pos):
        print("Collision detected! Game over.")
        pygame.display.quit()
        exit()
    elif check_winner(player1_pos):
        print("Player 1 wins!")
        pygame.display.quit()
        exit()
    elif check_winner(player2_pos):
        print("Player 2 wins!")
        pygame.display.quit()
        exit()

    pygame.display.update()
    frames.tick(60)

