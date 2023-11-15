import pygame
import random

pygame.init()

screen_size = (800,600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Tank Parachute Game")

#game properties
health = 3
parachute_frequency = 180
frame_rate = 60
timer = 0
game_over_screen = pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\Dead Screenpng.png")
game_over = False

#Health images
health_image_full = pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\Health indicator full.png")
health_image_half = pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\health indicator half.png")
health_image_low= pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\health_indicator low.png")
health_image_none = pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\Health indicator.png")

#Scoring
font = pygame.font.Font(None, 36)
score = 0

#tank properties
tank = pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\tank.png")
tank_x = -15
tank_y = 350
tank_health = 3

#projectile properties
projectile_image = pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\projectile.png")
projectile_image = pygame.transform.scale(projectile_image,(80,40))
projectile_x = tank_x + 380
projectile_y = tank_y + 200
projectile_speed = 10
projectiles = []
projectile = projectile_x, projectile_y
shoot_delay = 30  # Adjust this value to change the shooting cooldown
shoot_cooldown = 0

#parachute properties
parachute_bomb = pygame.image.load(r"C:\Users\danie\Desktop\Pygames\tank parachute game\parachute bomb.png")
parachute_counter = 0
parachute_bombs = []
parachute_bomb_speed = 3
bomb_x = 0
bomb_y = 0

#Object rectangles
projectile_rect = pygame.Rect(0,0, 100, 100)
bomb_rect = pygame.Rect(bomb_x, bomb_y, 50, 50)

def game_over_function():
    global running, game_over

    quit_region = pygame.Rect(170, 350, 500, 125)
    play_again_region = pygame.Rect(170, 225, 500, 120)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen.blit(game_over_screen, (-280, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if quit_region.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                running = False
                game_over = False  
            if play_again_region.collidepoint(mouse_x, mouse_y):
                reset_game()

def reset_game():
    global tank_x, tank_y, score, health, game_over, projectiles, shoot_cooldown, parachute_bombs, parachute_frequency, timer
    
    tank_x = -15
    tank_y = 350
    health = 3
    score = 0

    projectiles = []
    parachute_bombs = []

    game_over = False
    timer = 0
    shoot_cooldown = 0
    parachute_frequency = 180

    
def parachute_bombs_function():
    global parachute_counter, parachute_frequency, timer, health
    if (parachute_counter == parachute_frequency):
        random_x = random.randint(1, 500)
        parachute_bombs.append([random_x, 0])
        parachute_counter = 0
        
    parachute_counter += 1
    if (timer >= 3):
        parachute_frequency -= 5
        timer = 0
        
    for bomb in parachute_bombs:
        bomb_x, bomb_y = bomb
        bomb_y += parachute_bomb_speed  # Fall speed
        bomb[1] = bomb_y  # Update the y coordinate of the bomb
        bomb[0] = bomb_x
        if bomb_y > screen_size[1]:
            parachute_bombs.remove(bomb)
            health -= 1
            
def movement_function():
    global shoot_cooldown, tank_x, tank_y, tank_health
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and tank_x > -390:
            tank_x -= 5
    if keys[pygame.K_RIGHT] and tank_x < 355:
            tank_x += 5
    if keys[pygame.K_SPACE] and shoot_cooldown <= 0:
                projectiles.append([tank_x + 380, tank_y + 200])
                shoot_cooldown = shoot_delay

    if shoot_cooldown > 0:
            shoot_cooldown -= 1

def projectile_function():
     global projectile_x, projectile_y, projectile_rect
     for projectile in projectiles:
            projectile_x, projectile_y = projectile
            projectile_y -= projectile_speed 
            projectile[1] = projectile_y
            projectile[0] = projectile_x

            projectile_rect = pygame.Rect(projectile_x, projectile_y, 10, 10)

    #Resetting projectile's position
     if projectile_y < -20:
        projectile_x = tank_x + 380
        projectile_y = tank_y + 200

def collision_function():
    global score
    for projectile in projectiles:
        projectile_x, projectile_y = projectile
        projectile_rect = pygame.Rect(projectile_x, projectile_y, 10, 10)    
        for bomb in parachute_bombs:
                bomb_x, bomb_y = bomb
                bomb_rect = pygame.Rect(bomb_x, bomb_y, 50, 50)
                bomb_rect.x = bomb_x + 20
                if projectile_rect.colliderect(bomb_rect):
                # Handle collision here
                    parachute_bombs.remove(bomb)
                    projectiles.remove(projectile)
                    score += 1
                    break

running = True
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    timer += 1 / frame_rate
    
    #Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  

    if health <= 0:
        game_over = True
    else:
        game_over = False
    if not game_over:
        
        movement_function()
        projectile_function()
        parachute_bombs_function()
        collision_function()
        
        screen.fill((135,206,235))
        screen.blit(tank, (tank_x, tank_y))
        if health == 3:
             screen.blit(health_image_full, (-35,-20))
        elif health == 2:
                screen.blit(health_image_half, (-35,-20))
        elif health == 1:
                screen.blit(health_image_low, (-35,-20))
        elif health == 1:
                screen.blit(health_image_none, (-35,-20))
        screen.blit(score_text, (690, 10))  
        for projectile in projectiles:
            screen.blit(projectile_image, (projectile[0], projectile[1]))
        for bomb in parachute_bombs:
            screen.blit(parachute_bomb, (bomb[0], bomb[1]))
    else:
        game_over_function()
    
    clock.tick(frame_rate)
    pygame.display.update()

pygame.quit()

