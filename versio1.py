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
GREEN = (0, 255, 0)
ORANGE = (252, 157, 3)
CYAN = (248, 3, 252)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Pelaaja
player_size = 50
player_x = SCREEN_WIDTH // 2
player_y = 10  # Pelaaja lähellä yläreunaa
player_speed = 5
max_vertical_speed = 10
player_starting_lives = 1
player_lives = player_starting_lives
# Aseta fontti
font = pygame.font.Font(None, 32)
# Tekstin asetukset
game_over_text = font.render('PELI OHI!', True, BLACK, WHITE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
continue_text = font.render('Paina mitä tahansa näppäintä pelataksesi uudelleen', True, BLACK, WHITE)
continue_rect = continue_text.get_rect()
continue_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 32)

# Esteet
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Pisteet
score = 0

# Fontti
font = pygame.font.Font(None, 36)
# Kerättävien esineiden tyypit
POINTS100 = 1
SHIELD = 2

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

kilpi_paalla = False 

# Funktio esteiden luomiseen
def create_obstacle():
    x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    y = SCREEN_HEIGHT  # Aloita alhaalta
    # esteen tyyppi (kerättävä = 1, este = 2)
    if random.randint(1, 10) > 7:
        kerattava_tyyppi = 1
        if random.randint(1, 10) > 7:
            esine_tyyppi = SHIELD
        else:
            esine_tyyppi = POINTS100         
    else:
        kerattava_tyyppi = 2
        esine_tyyppi = 0
    return [x, y, kerattava_tyyppi, esine_tyyppi]

# Funktio pelin resetoimiseen game-overin jälkeen
def reset_game():
    global player_x, player_y, player_lives, obstacles, score, kilpi_paalla
    player_x = SCREEN_WIDTH // 2
    player_y = 10
    player_lives = player_starting_lives
    obstacles = []  # Tyhjennä esteet
    score = 0
    kilpi_paalla = False
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
            # jos osuu esteeseen peli loppuu, jos osuu kerättävään esineeseen peli jatkuu
            if obstacle[2] == 2:
                if kilpi_paalla:
                    kilpi_paalla = False 
                    obstacles.remove(obstacle)
                else:
                    running = False
                    player_lives -= 1
                    obstacles.remove(obstacle)                    
                    
            else:
                if obstacle[3] == POINTS100:
                    # pisteet
                    obstacles.remove(obstacle)
                    score += 100
                elif obstacle[3] == SHIELD:
                    obstacles.remove(obstacle)
                    kilpi_paalla = True

    # Pisteiden laskenta
    # score += 1
    if score > highscore:
        highscore = score

    # Piirrä pelaaja ja esteet
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

    # Piirrä kipli
    if kilpi_paalla:
        pygame.draw.rect(screen, CYAN, (player_x, player_y, player_size, player_size), 4)

    for obstacle in obstacles:
        if obstacle[2] == 2:
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))
        elif obstacle[2] == 1:
            if obstacle[3] == POINTS100:
                pygame.draw.rect(screen, GREEN, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))
            elif obstacle[3] == SHIELD:
                pygame.draw.rect(screen, ORANGE, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

    # Piirrä pisteet
    score_text = font.render(f"Pisteet: {score}", True, BLACK)
    highscore_text = font.render(f"Ennätys: {highscore}", True, BLACK)
    speed_text = font.render(f"Speed: {obstacle_speed}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(highscore_text, (10, 40))
    screen.blit(speed_text, (10, 70))

    pygame.display.flip()
    clock.tick(FPS)

        # Tarkista onko Game-Over
    if player_lives <= 0:
        screen.blit(game_over_text, game_over_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.update()
        # Pause kunnes pelaaja painaa nappia
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    reset_game()  # Nollaa peli ja aloita alusta
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
# Tallenna korkein pistemäärä
save_score(highscore)

pygame.quit()
