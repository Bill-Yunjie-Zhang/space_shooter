import freegames
import pygame
from random import randint

pygame.init()

############## Global ##############
#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
#screen
SCREEN_COLOR = WHITE
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (300, 600)
#player
PLAYER_HEIGHT = 43
PLAYER_WIDTH = 49
PLAYER_SPEED = 3
PLAYER_INITIAL_X_LOCATION = int(SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2) 
PLAYER_INITIAL_Y_LOCATION = SCREEN_HEIGHT - PLAYER_HEIGHT
#bullets
BULLETS_WIDTH = 5
BULLETS_HEIGHT = 24
BULLETS_COLOR = BLACK
BULLET_SPEED = 5
#enemies
ENEMY_WIDTH = 70
ENEMY_HEIGHT = 33
NUMBER_OF_ENEMIES = 25
ENEMY_SPEED = 3
ENEMY_COLOR = BLACK
X_RANGE_MIN = ENEMY_WIDTH
X_RANGE_MAX = SCREEN_WIDTH - ENEMY_WIDTH
Y_RANGE_MIN = -1000
Y_RANGE_MAX = -ENEMY_HEIGHT
#directory
HERE = "c:/Users/Bill/Documents/ZhongXi/class/Python/spaceshooter/"

def draw_bullets(bullets, bullet_motion, screen):
    bullet_image = pygame.image.load(HERE + "pics/bullet.png")
    for bullet in bullets:
        screen.blit(bullet_image, (bullet.x + (PLAYER_WIDTH / 2) - (BULLETS_WIDTH / 2), bullet.y))
        bullet.move(bullet_motion)

def create_enemies(num):
    enemy_list = []
    for ii in range(num):
        enemy_list.append(freegames.vector(randint(X_RANGE_MIN, X_RANGE_MAX), randint(Y_RANGE_MIN, Y_RANGE_MAX)))
    return enemy_list

def draw_enemies(enemies, enemy_motion, screen):
    enemy_image = pygame.image.load(HERE + "pics/Mothership.png")
    for enemy in enemies:
        screen.blit(enemy_image, enemy)
        enemy.move(enemy_motion)

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Space Shooter")

    background_image = pygame.image.load(HERE + "pics/th.png")

    music_path = HERE + "/Track.mp3"
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loops=-1)

    score = 0
    font = pygame.font.SysFont(None, 24)
    score_render = font.render("Score: %i" %(score), True, RED)

    player_loc = freegames.vector(PLAYER_INITIAL_X_LOCATION, PLAYER_INITIAL_Y_LOCATION)
    player_motion = freegames.vector(0, 0)
    player_image = pygame.image.load(HERE + "pics/spaceship-small.png")

    bullets = []
    bullet_motion = freegames.vector(0, -BULLET_SPEED)
    enemies = create_enemies(NUMBER_OF_ENEMIES)
    enemy_motion = freegames.vector(0, ENEMY_SPEED)

    done = False
    end = False
    while not done:
        PLAYER_COLOR = BLUE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if not end:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_motion.x = -PLAYER_SPEED
                    elif event.key == pygame.K_RIGHT:
                        player_motion.x = PLAYER_SPEED
                    elif event.key == pygame.K_UP:
                        player_motion.y = -PLAYER_SPEED
                    elif event.key == pygame.K_DOWN:
                        player_motion.y = PLAYER_SPEED
                    elif event.key == pygame.K_SPACE:
                        bullets.append(player_loc.copy())
                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or
                        event.key == pygame.K_RIGHT):
                        player_motion.x = 0
                    if (event.key == pygame.K_UP or
                        event.key == pygame.K_DOWN):
                        player_motion.y = 0
        screen.blit(background_image, (0, 0))
        draw_enemies(enemies, enemy_motion, screen)
        draw_bullets(bullets, bullet_motion, screen)

        for enemy in enemies:
            for bullet in bullets:
                if (enemy.x - ENEMY_WIDTH / 2) < bullet.x and (enemy.x + ENEMY_WIDTH / 2) > (bullet.x - BULLETS_WIDTH) and (enemy.y + ENEMY_HEIGHT / 2) >= bullet.y and enemy.y <= (bullet.y + BULLETS_HEIGHT):
                    score += 1
                    score_render = font.render("Score: %i" %(score), True, RED)
                    enemy.y = Y_RANGE_MIN
                    bullets.remove(bullet)
                if bullet.y <= -BULLETS_HEIGHT:
                    bullets.remove(bullet)
            if (enemy.y + ENEMY_HEIGHT) >= SCREEN_HEIGHT:
                end = True
            if (enemy.y + ENEMY_HEIGHT / 2) > player_loc.y and enemy.y < (player_loc.y + PLAYER_HEIGHT / 2) and (enemy.x + ENEMY_WIDTH / 2) > player_loc.x and enemy.x < (player_loc.x + PLAYER_WIDTH / 2):
                end = True

        if len(enemies) == 0:
            enemy_motion.y = 0
            bullet_motion.y = 0
            player_motion.x = 0
            player_motion.y = 0

        if end:
            enemy_motion.y = 0
            bullet_motion.y = 0
            player_motion.x = 0
            player_motion.y = 0

        if player_loc.x > SCREEN_WIDTH + PLAYER_WIDTH:
            player_loc.x = - PLAYER_WIDTH
        elif player_loc.x < - PLAYER_WIDTH:
            player_loc.x = SCREEN_WIDTH + PLAYER_WIDTH

        screen.blit(player_image, player_loc)
        screen.blit(score_render, (10, 10))
        
        player_loc.move(player_motion)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()

#any player meets end dead
#bullet hit enmy enemy dead
#enemy bottom turn red
#turn red when touches player