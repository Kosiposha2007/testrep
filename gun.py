from random import choice
from random import randint
from math import *

import pygame as pg

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
DARK_GREEN = 0x006400
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1080
HEIGHT = 720


def rotate_rect(scr, x, y, a, b, ang, color):
    pg.draw.polygon(scr, color, [(x, y), (x + a * cos(ang), y + a * sin(ang)),
                                 (x + a * cos(ang) - b * sin(ang), y + a * sin(ang) + b * cos(ang)),
                                 (x - b * sin(ang), y + b * cos(ang)), (x, y)])


class Ball:
    def __init__(self, screen: pg.Surface):
        global bullet_type
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        acs - ускорение мяча
        r - радиус мяча
        vx, vy - проекции скорости мяча на оси x и y
        type - тип мяча-пули
        """
        self.acs = 1
        self.screen = screen
        self.x = gun.gunpos
        self.y = HEIGHT - 50
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.type = bullet_type

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна.
        """
        self.vy += self.acs
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        """Добавляет спрайт мяча на экран в зависимости от типа пули.
        """
        if self.type == 1:
            pg.draw.circle(self.screen, BLACK, (self.x, self.y), self.r)
            pg.draw.circle(self.screen, RED, (self.x, self.y), self.r, 6)
            pg.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 4)

        else:
            pg.draw.circle(self.screen, BLACK, (self.x, self.y), self.r)
            pg.draw.circle(self.screen, YELLOW, (self.x, self.y), self.r, 6)
            pg.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 4)

    def hittest(self, obj, i):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x[i]) ** 2 + (self.y - obj.y[i]) ** 2 <= (self.r + obj.r[i]) ** 2:
            return True
        else:
            return False

    def bombhittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + 15) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen, lives):
        """ Конструктор класса gun
            Args:
            f2_power - мощность выстрела
            f2_on - принимает значения 1 и 0 в зависимости от того, заряжается пушка или нет
            gunpos - x-координата пушки танка
            lives - количество жизней танка
            """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.ang = 1
        self.color = DARK_GREEN
        self.gunpos = WIDTH / 2
        self.lives = lives

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.ang = atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * cos(self.ang)
        new_ball.vy = self.f2_power * sin(self.ang)
        balls.append(new_ball)
        self.f2_power = 10
        self.f2_on = 0

    def aiming(self, event):
        """Прицеливание. Зависит от положения мыши.
        """
        if event:
            if event.pos[1] < HEIGHT - 50:
                self.ang = -acos((event.pos[0] - self.gunpos)
                                 / sqrt((event.pos[1] - HEIGHT + 50) ** 2 + (event.pos[0] - self.gunpos) ** 2))
        if self.f2_on:
            self.color = RED
        else:
            self.color = DARK_GREEN

    def draw(self):
        """Рисует танк и пушку, пушка изменяет цвет(заряжается) в зависимости от продолжительности нажатия на экран
        """
        rotate_rect(self.screen, self.gunpos + 10, HEIGHT - 50, 15, 100, -pi / 2 + self.ang, DARK_GREEN)
        rotate_rect(self.screen, self.gunpos + 10, HEIGHT - 50, 15, self.f2_power, -pi / 2 + self.ang, self.color)
        pg.draw.ellipse(self.screen, DARK_GREEN, (self.gunpos - 50, HEIGHT - 65, 100, 50))
        pg.draw.ellipse(self.screen, DARK_GREEN, (self.gunpos - 100, HEIGHT - 30, 200, 60))

    def power_up(self):
        """Увеличивает мощность пушки.
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 3
            self.color = RED
        else:
            self.color = DARK_GREEN

    def draw_lives(self):
        """В левом верхнем углу экрана рисует количество жизней в виде красных кружочков.
        """
        for i in range(self.lives):
            pg.draw.circle(self.screen, RED, (25 + 20 * i, 25), 10)

    def tank_hit(self):
        """Отнимает от счетчика жизней одну жизнь при попадании бомбочки по танку.
        Returns:
            True - если жизней не осталось
            False - если жизни еще есть
        """
        self.lives -= 1
        if self.lives > 0:
            return False
        else:
            return True


class Target:
    def __init__(self):
        """ Конструктор класса gun
        Args:
        x - массив x-координат целей
        y - массив y-координат целей
        r - радиус целей
        spx, spy - массивы проекций скоростей целей на оси x и y
        """
        self.color = RED
        self.screen = screen
        self.x = []
        self.y = []
        self.r = []
        self.spx = []
        self.spy = []

    def shot(self):
        """Прибавляет к счетчику живых мишеней 1 и добавляет в массивы значения для новой мишени.
        """
        self.live += 1
        self.new_target()

    def new_target(self):
        """ Создание новой цели.
        """
        self.x.append(randint(200, WIDTH - 200))
        self.y.append(randint(200, HEIGHT - 200))
        self.r.append(randint(10, 30))
        self.spx.append(randint(-5, 5))
        self.spy.append(randint(-5, 5))

    def hit(self):
        """При попадании снаряда в мишень удаляется мишень
        Returns:
            количество очков за уничтоженную мишень
        """
        self.x = self.x[:i] + self.x[i + 1:]
        self.y = self.y[:i] + self.y[i + 1:]
        self.r = self.r[:i] + self.r[i + 1:]
        self.spx = self.spx[:i] + self.spx[i + 1:]
        self.spy = self.spy[:i] + self.spy[i + 1:]
        return 1

    def draw(self, i):
        """Перемещение i-ой мишени и изображение на экране ее спрайта.
        """
        self.x[i] += self.spx[i]
        self.y[i] += self.spy[i]
        if self.x[i] < self.r[i] or self.x[i] > WIDTH - self.r[i]:
            self.spx[i] = -self.spx[i]
        if self.y[i] < self.r[i] or self.y[i] > HEIGHT - 150 - self.r[i]:
            self.spy[i] = -self.spy[i]
        pg.draw.circle(self.screen, self.color, (self.x[i], self.y[i]), self.r[i])
        pg.draw.circle(self.screen, BLACK, (self.x[i], self.y[i]), self.r[i] / 4)
        pg.draw.circle(self.screen, BLACK, (self.x[i], self.y[i]), self.r[i], 2)


class BonusTarget:
    def __init__(self):
        """ Конструктор класса gun
        Args:
        x - массив x-координат целей
        y - массив y-координат целей
        r - радиус целей
        spx, spy - массивы проекций скоростей целей на оси x и y
        """
        self.screen = screen
        self.x = []
        self.y = []
        self.r = []
        self.spx = []
        self.spy = []

    def shot(self):
        """Прибавляет к счетчику живых мишеней 1 и добавляет в массивы значения для новой мишени.
        """
        self.live += 1
        self.new_target()

    def new_target(self):
        """ Создание новой цели.
        """
        self.x.append(randint(200, WIDTH - 200))
        self.y.append(randint(200, HEIGHT - 200))
        self.r.append(randint(15, 20))
        self.spx.append(randint(-30, 30))
        self.spy.append(randint(-30, 30))
        self.color = YELLOW

    def hit(self, points=1):
        """При попадании снаряда в мишень удаляется мишень
            Returns:
                количество очков за уничтоженную мишень
        """
        self.points = points
        self.x = self.x[:i] + self.x[i + 1:]
        self.y = self.y[:i] + self.y[i + 1:]
        self.r = self.r[:i] + self.r[i + 1:]
        self.spx = self.spx[:i] + self.spx[i + 1:]
        self.spy = self.spy[:i] + self.spy[i + 1:]
        return 2

    def draw(self, i):
        """Перемещение i-ой мишени и изображение на экране ее спрайта.
        """
        self.x[i] += self.spx[i]
        self.y[i] += self.spy[i]
        if self.x[i] < self.r[i] or self.x[i] > WIDTH - self.r[i]:
            self.spx[i] = -self.spx[i]
        if self.y[i] < self.r[i] or self.y[i] > HEIGHT - 150 - self.r[i]:
            self.spy[i] = -self.spy[i]
        pg.draw.circle(self.screen, self.color, (self.x[i], self.y[i]), self.r[i])
        pg.draw.circle(self.screen, BLACK, (self.x[i], self.y[i]), self.r[i] / 4)
        pg.draw.circle(self.screen, BLACK, (self.x[i], self.y[i]), self.r[i], 2)


class Bomb(Ball, Target):
    def __init__(self):
        super().__init__(screen)
        """ Конструктор класса bomb
            Args:
            acs - ускорение бомб
            x - случайная координат бомб
            y - координата бомб
            vx, vy - проекция скорости бомбы на ось y
        """
        self.acs = 0.5
        self.screen = screen
        self.x = randint(0, WIDTH)
        self.y = 30
        self.vy = 0
        self.color = BLACK

    def create(self):
        """Создание новой бомбы и добавление ее в массив.
        """
        global bombs
        new_bomb = Bomb()
        bombs.append(new_bomb)

    def move(self):
        """Удаление бомбы, если она упала на землю.
        """
        global bombs
        self.vy += self.acs
        self.y += self.vy
        if self.y > HEIGHT:
            bombs = bombs[1:]

    def draw(self):
        """Изображение спрайта бомбы на экране.
        """
        pg.draw.circle(self.screen, self.color, (self.x, self.y), 15)
        pg.draw.polygon(self.screen, self.color,
                        [(self.x, self.y), (self.x - 15, self.y - 25), (self.x + 15, self.y - 25)])
        pg.draw.circle(self.screen, YELLOW, (self.x, self.y), 7)
        pg.draw.line(self.screen, self.color, (self.x - 10.6, self.y - 10.6), (self.x + 10.6, self.y + 10.6))
        pg.draw.line(self.screen, self.color, (self.x + 10.6, self.y - 10.6), (self.x - 10.6, self.y + 10.6))


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

balls = []
bombs = []

bullet = 0
bullet_type = 1
counter = 0
number_of_targets = 2
number_of_bonus_targets = 1

gun = Gun(screen, 3)
bonus_target = BonusTarget()
bonus_target.live = 0
target = Target()
target.live = 0
bomb = Bomb()

finished = False
left = False
right = False

while not finished:
    clock.tick(FPS)

    screen.fill(WHITE)
    gun.draw()
    gun.draw_lives()

    while target.live < number_of_targets:
        target.shot()
    while bonus_target.live < number_of_bonus_targets:
        bonus_target.shot()

    for i in range(target.live):
        target.draw(i)

    for i in range(bonus_target.live):
        bonus_target.draw(i)

    for b in balls:
        b.draw()

    if randint(1, 20) == 10:
        bomb.create()

    for bomb in bombs:
        bomb.draw()

    pg.display.update()


    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            gun.fire2_start()

        elif event.type == pg.MOUSEBUTTONUP:
            gun.fire2_end(event)

        elif event.type == pg.MOUSEMOTION:
            gun.aiming(event)

        elif event.type == pg.QUIT:
            finished = True

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                left = True

            elif event.key == pg.K_d:
                right = True

            elif event.key == pg.K_1:
                bullet_type = 1

            elif event.key == pg.K_2:
                bullet_type = 2

        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                left = False

            if event.key == pg.K_d:
                right = False

    if left is True:
        gun.gunpos -= 15
    if right is True:
        gun.gunpos += 15

    gun.power_up()

    for b in balls:
        b.move()
        for i in range(number_of_targets):
            if b.hittest(target, i) and target.live > 0 and bullet_type == 1:
                target.live -= 1
                counter += target.hit()
                target.shot()

        for i in range(number_of_bonus_targets):
            if b.hittest(bonus_target, i) and target.live > 0 and bullet_type == 2:
                bonus_target.live -= 1
                counter += bonus_target.hit()
                bonus_target.shot()

    for bomb in bombs:
        bomb.move()
        if gun.gunpos - 100 <= bomb.x <= gun.gunpos + 100:
            if bomb.y >= HEIGHT - 65:
                bombs = bombs[:bombs.index(bomb)] + bombs[bombs.index(bomb) + 1:]
                if gun.tank_hit():
                    finished = True

finished = False

while not finished:
    screen.fill(WHITE)
    f1 = pg.font.Font(None, 50)
    f2 = pg.font.Font(None, 36)
    text1 = f1.render('GAME OVER', True, (180, 0, 0))
    text2 = f2.render('Ваш счёт: ' + str(counter), True, (180, 0, 0))
    screen.blit(text1, (WIDTH / 3, HEIGHT / 2))
    screen.blit(text2, (WIDTH / 3, HEIGHT / 2 + 50))
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
pg.quit()
