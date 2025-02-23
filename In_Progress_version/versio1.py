import pygame
import random
import sys
from pygame import mixer

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

# Game state
game_state = "menu"
game_started = False

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

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 32)

# Esteet
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5


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

m_vol = 0.7

# Menu
def main_menu(resume=False):
    #Displays the main menu. If resume==True the first button shows "Resume", 
    #otherwise it shows "Start". Returns a string indicating which option was chosen.
    menu_active = True
    while menu_active:
        screen.fill(WHITE)
        title_text = font.render("Pelin valikko", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_text, title_rect)

        # Define buttons
        button_width, button_height = 200, 50
        start_button = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, 200, button_width, button_height)
        rules_button = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, 300, button_width, button_height)
        quit_button  = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, 400, button_width, button_height)

        # Draw the buttons
        pygame.draw.rect(screen, BLUE, start_button)
        pygame.draw.rect(screen, BLUE, rules_button)
        pygame.draw.rect(screen, BLUE, quit_button)

        # Button texts (the first button shows "Resume" if resume is True)
        start_label = "Resume" if resume else "Start"
        start_render = small_font.render(start_label, True, WHITE)
        rules_render = small_font.render("Rules", True, WHITE)
        quit_render  = small_font.render("Quit", True, WHITE)
        screen.blit(start_render, start_render.get_rect(center=start_button.center))
        screen.blit(rules_render, rules_render.get_rect(center=rules_button.center))
        screen.blit(quit_render, quit_render.get_rect(center=quit_button.center))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.collidepoint(pos):
                    return "start"
                if rules_button.collidepoint(pos):
                    return "rules"
                if quit_button.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

def rules_screen():
    # Shows the rules and returns to the menu when a key is pressed.
    rules_active = True
    while rules_active:
        screen.fill(WHITE)
        title = font.render("Rules", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(title, title_rect)
        rules_lines = [
            "Use left/right arrow keys to move.",
            "Avoid red obstacles.",
            "Collect green (100 points) and orange (shield) items.",
            "Press UP/DOWN to adjust obstacle speed.",
            "Press SPACE to pause the game.",
            "When shield is active, one hit is absorbed.",
            "Press any key to return to the menu."
        ]
        for i, line in enumerate(rules_lines):
            line_render = small_font.render(line, True, BLACK)
            screen.blit(line_render, (50, 100 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                rules_active = False
        clock.tick(FPS)
        
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

def game_over_screen():
    #Display game over screen and wait for a key press.
    over = True
    game_over_text = font.render("PELI OHI! Paina mitä tahansa näppäintä palataksesi valikkoon." , True, BLACK)
    continue_text = small_font.render("Sait kerättyä pisteitä: " + str(score), True, BLACK)
    while over:
        screen.fill(WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                over = False
        clock.tick(FPS)
        
# Pelilooppi
def peli_looppi():
    global obstacles, score, highscore, player_x, player_y, kilpi_paalla, obstacle_speed, player_lives, game_started
    obstacles = []
    playing = True
    soita_musiikkia()
    while playing:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    obstacle_speed = min(max_vertical_speed, obstacle_speed + 1)
                if event.key == pygame.K_UP:
                    obstacle_speed = max(1, obstacle_speed - 1)
                if event.key == pygame.K_SPACE:
                    return "pause"
                
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
            game_started = False
            game_over_screen()
            reset_game()
            return "game_over"
             # Pause kunnes pelaaja painaa nappia
            is_paused = True
            while is_paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        reset_game()  # Nollaa peli ja aloita alusta
                        is_paused = False
                    if event.type == pygame.QUIT:
                        is_paused = False
                        playing = False  

def soita_musiikkia():
    global m_vol
    mixer.init() 
    mixer.music.load("game.mp3") 
    mixer.music.set_volume(m_vol) 
    mixer.music.play() 

running = True
while running:
    if game_state == "menu":
        menu_choice = main_menu(resume=game_started)
        if menu_choice == "start":
            if not game_started:
                reset_game()
                game_started = True
            game_state = "playing"
        elif menu_choice == "rules":
            game_state = "rules"
    elif game_state == "rules":
        rules_screen()
        game_state = "menu"
    elif game_state == "playing":
        result = peli_looppi()
        if result == "pause":
            game_state = "menu"
        elif result == "game_over":
            game_state = "menu"
            
# Tallenna korkein pistemäärä
save_score(highscore)

pygame.quit()