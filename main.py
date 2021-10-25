import pygame, sys
from pygame.locals import *
import random
import time

pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()
icon = pygame.image.load('icon.png')
bg = pygame.image.load('spacebg2.png')
pygame.display.set_icon(icon)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
W, H = 400, 600
bgY = H
bgY2 = 2 * H
pygame.display.set_icon(icon)
dp = pygame.display.set_mode((W, H))
dp.fill(WHITE)
pygame.display.set_caption("Dog Invader")
SPEED = 3
lives = 1000
deaths = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kj.png")
        self.surf = pygame.Surface(self.image.get_rect().size)
        self.rect = self.surf.get_rect(center=(random.randint(40, 360), 0))
        self.collided = False

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom >= 600:
            self.rect.center = (random.randint(10, 390), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = W / 2
        self.y = H
        self.image = pygame.image.load("player.png")
        self.surf = pygame.Surface(self.image.get_rect().size)
        self.rect = self.surf.get_rect(center=((W / 2), H))
        self.shooting = False

    def move(self):
        global fired
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            if self.rect.top > 0:
                self.rect.move_ip(0, -5)
                self.y -= 5
        if pressed_keys[K_DOWN]:
            if self.rect.bottom <= H:
                self.rect.move_ip(0, 5)
                self.y += 5
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
                self.x -= 5
        if self.rect.right < W:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
                self.x += 5
        if pressed_keys[K_SPACE] and bullets < 5:
            fired = True

    def detect_collision(self, components):
        if pygame.sprite.spritecollide(self, components, False):
            return True


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.surf = pygame.Surface(self.image.get_rect().size)
        self.rect = self.surf.get_rect(center=(P1.x, P1.y))

    def move(self):
        global bullets, fired
        if self.rect.top > 0:
            self.rect.move_ip(0, -5)
        else:
            self.kill()
            bullets -= 1


P1 = Player()
E1 = Enemy()
bullets = 0
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(P1)
pygame.mixer.Sound('ass1.wav').play(loops=-1, fade_ms=1000)
INC_SPEED = pygame.USEREVENT + 1
collision = pygame.USEREVENT + 2
BulletFire = pygame.USEREVENT + 3
pygame.time.set_timer(BulletFire, 500)
pygame.time.set_timer(collision, 2000)
pygame.time.set_timer(INC_SPEED, 2000)
fired = False


def redrawWindow():
    dp.blit(bg, (0, bgY))
    dp.blit(bg, (0, bgY2))
    for entity in all_sprites:
        entity.move()
        dp.blit(entity.image, entity.rect)
    pygame.display.update()


run = True
while run:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.1
        if event.type == collision:
            E1.collided = False
        if event.type == BulletFire and fired:
            if bullets < 5:
                bullets += 1
                bu = Bullet()
                all_sprites.add(bu)
            fired = False
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if P1.detect_collision(enemies):
        if deaths < lives and E1.collided == False:
            deaths += 1
            E1.collided = True
            print(deaths)
        elif deaths == lives:
            dp.fill(RED)
            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            time.sleep(2)
            pygame.quit()
            sys.exit()
    redrawWindow()
    bgY += 1.4
    bgY2 += 1.4
    if bgY >= H:
        bgY = bgY2 - H
    if bgY2 >= H:
        bgY2 = bgY - H
    FramePerSec.tick(FPS)
