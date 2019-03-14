import pygame
import time
import random
import os

#Constants
WIDTH = 600
HEIGHT = 480
FPS = 60

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PLAYER = (75,75,75)
colors = (RED,BLUE,GREEN)
bullet_colors =[]
for i in range(90000):
    l = []
    for j in range(3):
        c = random.randrange(149,256)
        l.append(c)
    bullet_colors.append(l)
bullet_colors

font_n = pygame.font.match_font("arial")
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_n, size)
    text_surface = font.render(text,True,GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def newmob():
    mob = Mob()
    mobs.add(mob)
    all_sprites.add(mob)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((35,35))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7

        self.rect.x += self.speedx

        if self.rect.right > WIDTH :
            self.rect.right = WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


mobx = (50,100,150,200,250,300,400,500,150,250,350,450,550)
moby = (0,10,20,30,40)
class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.color = random.choice(bullet_colors)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(mobx)
        self.rect.y = random.choice(moby)
        self.speedy = random.randrange(2,6)
        self.speedx = random.randrange(-3,3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        """if self.rect.y > (HEIGHT+10) or self.rect.left < -25 or self.rect.right > WIDTH + 25 :
            self.rect.x = random.choice(mobx)
            self.rect.y = random.choice(moby)
            self.speedx = random.randrange(-2,2)"""

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx
            self.speedy = random.randrange(2,7)
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy = -self.speedy
            self.speedx = random.randrange(-3,3)


class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8,13))
        self.color = random.choice(bullet_colors)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -12

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 :
            self.kill()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pixel Wars!")
clock = pygame.time.Clock()

mobs = pygame.sprite.Group()
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()

for _ in range(8):
    newmob()
score = 0
running = True
while running :
    clock.tick(FPS)

    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 1
        newmob()
    hits = pygame.sprite.spritecollide(player,mobs,True)

    if hits :
        running = False
#update
    all_sprites.update()
    #render
    screen.fill(BLACK)
    pygame.draw.line(screen,random.choice(bullet_colors),[0,0],[0,HEIGHT],13)
    pygame.draw.line(screen,random.choice(bullet_colors),[0,HEIGHT],[WIDTH,HEIGHT],13)
    pygame.draw.line(screen,random.choice(bullet_colors),[WIDTH,HEIGHT],[WIDTH,0],13)
    pygame.draw.line(screen,random.choice(bullet_colors),[0,0],[WIDTH,0],13)
    all_sprites.draw(screen)
    draw_text(screen,str(score), 30, WIDTH/2, 30)
    pygame.display.flip()
running = True
while(running):
    clock.tick(FPS)

    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
    #render
    screen.fill(BLACK)
    pygame.draw.line(screen,random.choice(bullet_colors),[0,0],[0,HEIGHT],13)
    pygame.draw.line(screen,random.choice(bullet_colors),[0,HEIGHT],[WIDTH,HEIGHT],13)
    pygame.draw.line(screen,random.choice(bullet_colors),[WIDTH,HEIGHT],[WIDTH,0],13)
    pygame.draw.line(screen,random.choice(bullet_colors),[0,0],[WIDTH,0],13)
    draw_text(screen,str(score),60,WIDTH/2,HEIGHT/2)
    if(score < 10):
        draw_text(screen,"TRY HARDER DUDE!", 45, WIDTH /2, HEIGHT/2 +100)
    pygame.display.flip()


pygame.quit()
