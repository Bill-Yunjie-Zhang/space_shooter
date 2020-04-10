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
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
SCREEN_COLOR = WHITE
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
#player
PLAYER_RADIUS = 10
PLAYER_SPEED = 2
PLAYER_INITIAL_X_LOCATION = int(SCREEN_WIDTH / 2)
PLAYER_INITIAL_Y_LOCATION = SCREEN_HEIGHT - PLAYER_RADIUS
#bullets
BULLETS_WIDTH = 5
BULLETS_HEIGHT = 10
#enemies
ENEMY_RANDIUS = 10
NUMBER_OF_ENEMIES = 25
ENEMY_SPEED = 1
ENEMY_COLOR = BLACK
X_RANGE_MIN = ENEMY_RANDIUS
X_RANGE_MAX = SCREEN_WIDTH - ENEMY_RANDIUS
Y_RANGE_MIN = -1000
Y_RANGE_MAX = -ENEMY_RANDIUS
#bullet
BULLET_SPEED = 3

def draw_bullets(bullets, bullet_motion, screen):
    for bullet in bullets:
        pygame.draw.rect(screen, ENEMY_COLOR, (bullet.x - (BULLETS_WIDTH / 2), bullet.y, BULLETS_WIDTH, BULLETS_HEIGHT))
        bullet.move(bullet_motion)

def create_enemies(num):
    enemy_list = []
    for ii in range(num):
        enemy_list.append(freegames.vector(randint(X_RANGE_MIN, X_RANGE_MAX), randint(Y_RANGE_MIN, Y_RANGE_MAX)))
    return enemy_list

def draw_enemies(enemies, enemy_motion, screen):
    for enemy in enemies:
        pygame.draw.circle(screen, ENEMY_COLOR, enemy, ENEMY_RANDIUS)
        enemy.move(enemy_motion)

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Space Shooter")

    player_loc = freegames.vector(PLAYER_INITIAL_X_LOCATION, PLAYER_INITIAL_Y_LOCATION)
    player_motion = freegames.vector(0, 0)

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
                    elif event.key == pygame.K_SPACE:
                        bullets.append(player_loc.copy())
                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or
                        event.key == pygame.K_RIGHT):
                        player_motion.x = 0
        screen.fill(SCREEN_COLOR)  # same as clearing the screen
        draw_enemies(enemies, enemy_motion, screen)
        draw_bullets(bullets, bullet_motion, screen)
        for enemy in enemies:
            for bullet in bullets:
                if (enemy.x - ENEMY_RANDIUS) < bullet.x and (enemy.x + ENEMY_RANDIUS) > (bullet.x - BULLETS_WIDTH) and enemy.y >= bullet.y:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
            if enemy.y >= SCREEN_HEIGHT:
                end = True

        if len(enemies) == 0:
            enemy_motion.y = 0
            bullet_motion.y = 0
            player_motion.x = 0

        if end:
            enemy_motion.y = 0
            bullet_motion.y = 0
            player_motion.x = 0
            PLAYER_COLOR = RED

        pygame.draw.circle(screen, PLAYER_COLOR, player_loc, PLAYER_RADIUS)
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