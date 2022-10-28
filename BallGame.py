import pygame
from pygame.draw import *
from random import randint


pygame.init()

FPS = 60
screen = pygame.display.set_mode((1068, 601))


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
color = COLORS[randint(0, 5)]


def new_ball(): # Создает случайный первый круг
    global x, y, r, color
    x = randint(100, 500)
    y = randint(100, 300)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def new_ball2(): # Создает случайный второй круг
    global x2, y2, r2, color2
    x2 = randint(100, 500)
    y2 = randint(100, 300)
    r2 = randint(30, 50)
    color2 = COLORS[randint(0, 5)]
    circle(screen, color2, (x2, y2), r2)


def new_rectangle(): # Создает случайный прямоугольник
    global x3, y3, w, h, color3
    x3 = randint(100, 500)
    y3 = randint(100, 300)
    w = randint(70, 150)
    h = randint(40, 80)
    color3 = COLORS[randint(0, 5)]
    rect(screen, color3, (x3, y3, w, h))


def click(event): # Выводит был ли нажат первый круг
    s = pygame.mouse.get_pos()
    if x - r <= s[0] <= x + r and y - r <= s[1] <= y + r:
        return True
    else:
        return False


def click2(event): # Выводит был ли нажат второй круг
    s = pygame.mouse.get_pos()
    if x2 - r2 <= s[0] <= x2 + r2 and y2 - r2 <= s[1] <= y2 + r2:
        return True
    else:
        return False


def click3(event):  # Выводит был ли нажат прямоугольник
    s = pygame.mouse.get_pos()
    if x3 <= s[0] <= x3 + w and y3 <= s[1] <= y3 + h:
        return True
    else:
        return False


clock = pygame.time.Clock()
finished = False
count = 0
x1 = False


while not finished:
    clock.tick(FPS)

    new_ball()
    new_ball2()
    new_rectangle()

    x1 = False

    vx1 = randint(1, 30)
    vy1 = randint(1, 30)
    vx2 = randint(1, 30)
    vy2 = randint(1, 30)
    vx3 = randint(10, 40)
    vy3 = randint(10, 40)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click(pygame.MOUSEBUTTONDOWN) is True or click2(pygame.MOUSEBUTTONDOWN) is True:
                    count += 1
                    x1 = True
                if click3(pygame.MOUSEBUTTONDOWN) is True:
                    count += 5
                    x1 = True
            elif event.type == pygame.QUIT:
                finished = True
        x += vx1
        y += vy1
        if x + r >= 1068:
            vx1 = - randint(1, 15)
            x = 1068 - r
        if x - r <= 0:
            vx1 = randint(1, 15)
            x = r
        if y - r <= 0:
            vy1 = randint(1, 15)
            y = r
        if y + r >= 601:
            vy1 = - randint(1, 15)
            y = 601 - r

        x2 += vx2
        y2 += vy2
        if x2 + r2 >= 1068:
            vx2 = - randint(1, 15)
            x2 = 1068 - r2
        if x2 - r2 <= 0:
            vx2 = randint(1, 15)
            x2 = r2
        if y2 - r2 <= 0:
            vy2 = randint(1, 15)
            y2 = r2
        if y2 + r2 >= 601:
            vy2 = - randint(1, 15)
            y2 = 601 - r2

        x3 += vx3
        y3 += vy3
        if x3 + w >= 1068:
            vx3 = - randint(10, 20)
            x3 = 1068 - w
        if x3 <= 0:
            vx3 = randint(10, 20)
            x3 = 0
        if y3 <= 0:
            vy3 = randint(10, 20)
            y3 = 0
        if y3 + h >= 601:
            vy3 = - randint(10, 20)
            y3 = 601 - h

        screen.fill(BLACK)

        circle(screen, color, (x, y), r)
        circle(screen, color2, (x2, y2), r2)
        rect(screen, color3, (x3, y3, w, h))

        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('Ваш счёт:' + str(count), 1, (180, 0, 0))
        screen.blit(text1, (10, 50))

        pygame.display.update()

        clock.tick(FPS)
        if x1 is True:
            x1 = False
            break
pygame.quit()
