import random
import sys
import time

import pygame

pygame.init()

FPS = 60
WIDTH = 500  # ширина экрана
HEIGHT = 500  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)

balance = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_image = pygame.image.load("player.png")
player = player_image.get_rect()
player.x = 250
player.y = 220

# floor_image = pygame.image.load("platform.png")
# floor=floor_image.get_rect()
floor = pygame.Rect(0 + 5, 500 - 35, 500, 30)

rock_image = pygame.image.load('rock2.png')
rock = pygame.Rect(0, random.randint(60, 450), 80, 45)


def up_collision(player, obstacle):
    if player[0] > obstacle[0] + obstacle[3] and player[0] > obstacle[0] + obstacle[3]:
        print("sdddsd")


class platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 20)

    def draw(self):
        pygame.draw.rect(screen, (70, 255, 70), self.rect, 4)


class Coin:
    def __init__(self):
        self.x = random.randint(0, 480)
        self.y = random.randint(0, 350)
        self.rect = pygame.Rect(self.x, self.y, 50, 28)
        self.coin = pygame.image.load('coin2.png')

    def draw(self):
        screen.blit(self.coin, self.rect)


def collision(player, obstacle):
    if player[0] < obstacle[0] + obstacle[2] and player[0] + player[2] > obstacle[0] and obstacle[1] < obstacle[1] + \
            obstacle[3] and player[1] + player[3] > obstacle[2]:
        return True

    """if x1 <= x2+h2 and x1+ w1 <= x2+h2:
        return True"""
    # колизия верхней части игрока с нижней частью припятсвия


def dead():
    global balance
    screen.blit(death, (WIDTH / 4.3, HEIGHT / 3.5))
    pygame.display.update()
    with open('text.txt', "a") as file:
        file.write('los with {} coins\n'.format(balance))
    time.sleep(2)
    balance = 0
    player.x = 250
    player.y = 220
    rock.x = random.randint(60, 450)
    rock.y = 0


def walls():
    global y, x, player

    if player.x <= 0:
        player.x = WIDTH - player.width - 10
    if player.x >= WIDTH - player.width:
        player.x = 10


def move():
    global y, x, player, speed

    if keys[pygame.K_UP]:
        player.y -= speed+2
    if keys[pygame.K_DOWN]:
        player.y += speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= speed


w = 40
h = 40

speed = 6

is_jump = False
jump_count = 20
jump_count_static = jump_count
jump_speed = 4

stand = True
gravity = 6

rock_fall = True

list_obstacle = []

coin = Coin()

obstacle1 = platform(400, 405)
obstacle2 = platform(250, 350)
obstacle3 = platform(100, 300)
obstacle4 = platform(360, 280)
obstacle5 = platform(200, 200)
obstacle6 = platform(370, 100)
obstacle7 = platform(50, 100)
obstacle8 = platform(50, 400)

list_obstacle.append(obstacle1.rect)
list_obstacle.append(obstacle2.rect)
list_obstacle.append(obstacle3.rect)
list_obstacle.append(obstacle4.rect)
list_obstacle.append(obstacle5.rect)
list_obstacle.append(obstacle6.rect)
list_obstacle.append(obstacle7.rect)
list_obstacle.append(obstacle8.rect)

font = pygame.font.SysFont('serif', 32)
font1 = pygame.font.SysFont('serif', 50)

death = font1.render('Вы проиграли', True, (255, 0, 0))


while True:

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    move()
    walls()

    if keys[pygame.K_SPACE]:
        if stand:
            is_jump = True

    if is_jump:
        # gravity = False
        # print(jump_count)
        # print("Hello")
        if jump_count <= jump_count_static and jump_count > 0:
            player.y -= (jump_speed ** 2) / 4
            player.y -= gravity
            jump_count -= 1
        if jump_count <= 0 and jump_count >= -jump_count_static:
            player.y += (jump_speed ** 2) / 4
            player.y -= gravity
            jump_count -= 1
            if jump_count <= -jump_count_static / 2:
                is_jump = False
                # gravity = True
                jump_count = jump_count_static

    if not stand:
        player.y += gravity

    screen.fill(WHITE)
    screen.blit(player_image, player)
    screen.blit(rock_image, rock)

    label = font.render('Монет:{}'.format(balance), True, (0, 0, 0))
    screen.blit(label, (10, 10))

    pygame.draw.rect(screen, (255, 0, 0), floor, 6)

    coin.draw()

    if random.randint(0, 60) == 1 and rock_fall == False:
        rock.y = 0
        rock.x = random.randint(60, 450)
        rock_fall = True

    if rock_fall:
        rock.y += gravity * 0.8
        if rock.y >= HEIGHT:
            rock_fall = False

    obstacle1.draw()
    obstacle2.draw()
    obstacle3.draw()
    obstacle4.draw()
    obstacle5.draw()
    obstacle6.draw()
    obstacle7.draw()
    obstacle8.draw()

    if player.colliderect(floor) or player.colliderect(rock):
        dead()

    elif player.collidelist(list_obstacle) >= 0:
        stand = True
    else:
        stand = False

    if player.colliderect(coin.rect):
        balance += 1
        coin = Coin()

    pygame.display.update()
    clock.tick(FPS)
