import pygame
import random

# Pygame setup
pygame.init()

# Näytön koko
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Esteiden väistely")

# Värit
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Pelaaja
player_size = 50
player_x = SCREEN_WIDTH // 2
player_y = 10  # Pelaaja lähellä yläreunaa
player_speed = 5
max_vertical_speed = 10

# Esteet
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Pisteet
score = 0

# Fontti
font = pygame.font.Font(None, 36)

# Pelin tallennus
def save_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def load_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

highscore = load_score()

# Funktio esteiden luomiseen
def create_obstacle():
    x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    y = SCREEN_HEIGHT  # Aloita alhaalta
    return [x, y]

# Pelilooppi
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                obstacle_speed = min(max_vertical_speed, obstacle_speed + 1)
            if event.key == pygame.K_DOWN:
                obstacle_speed = max(1, obstacle_speed - 1)

    # Pelaajan liike
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
        player_x += player_speed        

    # Esteiden hallinta
    if random.randint(1, 20) == 1:
        obstacles.append(create_obstacle())

    for obstacle in obstacles:
     obstacle[1] -= obstacle_speed  # Liiku ylöspäin

    obstacles = [obs for obs in obstacles if obs[1] + obstacle_height > 0]


    # Törmäyksen tarkistus
    for obstacle in obstacles:
        if (player_x < obstacle[0] + obstacle_width and
            player_x + player_size > obstacle[0] and
            player_y < obstacle[1] + obstacle_height and
            player_y + player_size > obstacle[1]):
            running = False

    # Pisteiden laskenta
    score += 1
    if score > highscore:
        highscore = score

    # Piirrä pelaaja ja esteet
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

    # Piirrä pisteet
    score_text = font.render(f"Pisteet: {score}", True, BLACK)
    highscore_text = font.render(f"Ennätys: {highscore}", True, BLACK)
    speed_text = font.render(f"Speed: {obstacle_speed}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(highscore_text, (10, 40))
    screen.blit(speed_text, (10, 70))

    pygame.display.flip()
    clock.tick(FPS)

# Tallenna korkein pistemäärä
save_score(highscore)

pygame.quit()
