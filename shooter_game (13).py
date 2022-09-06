# Jack branch
from pygame import *
from random import randint
from time import time as timer

init()
WIDTH = 700
HEIGHT = 500
scr = display.set_mode((WIDTH, HEIGHT))
display.set_caption('shooter')
background = transform.scale(image.load('galaxy.jpg'), (WIDTH, HEIGHT))

clock = time.Clock()
FPS = 100

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

max_losses = 8
losses = 0
score = 0
qwerty = font.SysFont('arial', 30)
qwertz = font.SysFont('arial', 100)
lose = qwertz.render('YOU LOSE', True, (200, 0, 0))
win = qwertz.render('YOU WIN', True, (0, 200, 0))
text_losses = qwerty.render(('lives: '+ str(max_losses - losses)), True, (200, 200, 200))
text_score = qwerty.render(('score: '+ str(score)), True, (200, 200, 200))
reload_alert = qwerty.render('reload', True, (200, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, speed, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(p_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        scr.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys =key.get_pressed()
        if keys[K_a] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < (WIDTH - self.width):
            self.rect.x += self.speed
    def shoot(self):
            bullets.add(Bullet('bullet.png', self.rect.centerx, (self.rect.y), 6, 10, 30))

class Enemy(GameSprite):
    def boof(self):
        self.rect.x = randint(1, (WIDTH - self.width))
        self.rect.y = -65
        self.speed = randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        global losses 
        if self.rect.y > HEIGHT:
            global losses, text_losses
            self.boof()
            losses += 1
            text_losses = qwerty.render(('lives:'+ str(max_losses - losses)), True, (200, 200, 200))  
            
class Asteroid(GameSprite):
    def boof(self):
        self.rect.x = randint(1, (WIDTH - self.width))
        self.rect.y = -100
        self.speed = randint(1, 2)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.boof()

bullet = transform.scale(image.load('bullet.png'), (20, 40))



enemies = sprite.Group()
for i in range(5):
    enemy_x = randint(1, 635)
    enemy_speed = randint(1, 3)
    enemies.add(Enemy('ufo.png', enemy_x, -65, enemy_speed, 65, 40))
asteroids = sprite.Group()
for i in range(3):
    asteroid_size = randint(40, 120)
    asteroids.add(Asteroid('asteroid.png', randint(1, (WIDTH- asteroid_size)), -100, randint(1, 2), asteroid_size, asteroid_size))
player = Player('rocket.png', 350, 400, 4, 65, 100)


num_fire = 0
reload = False
the_time = 1
game = True
finish = False


full_mag = 10
while game:
    for i in event.get():
        if i.type == QUIT or key.get_pressed()[K_ESCAPE]:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if reload == False:
                    num_fire += 1
                    player.shoot()
                    fire.play()
                    if num_fire >= full_mag and reload != True:
                        reload = True
                        the_time = timer()
        if losses > (max_losses - 1):
            scr.blit(lose, (175, 200))
            finish = True
        if score > 9:
            scr.blit(win, (175, 200))
            finish = True
            
    sprites_list = sprite.spritecollide(player, asteroids, True)
    for i in sprites_list:
        asteroid_size = randint(40, 120)
        asteroids.add(Enemy('asteroid.png', randint(1, (WIDTH- asteroid_size)), -100, randint(1, 2), asteroid_size, asteroid_size))
        losses += 1
        text_losses = qwerty.render(('lives:'+ str(max_losses - losses)), True, (200, 200, 200))
        
    collides = sprite.groupcollide(enemies, bullets, True, True)
    for i in collides:
        score += 1
        enemies.add(Enemy('ufo.png', randint(1, 635), -65, randint(1, 3), 65, 40))
        text_score = qwerty.render(('score: '+ str(score)), True, (200, 200, 200))
        
    collides = sprite.groupcollide(asteroids, bullets, True, True)
    for i in collides:
        asteroid_size = randint(40, 120)
        asteroids.add(Enemy('asteroid.png', randint(1, (WIDTH- asteroid_size)), -100, randint(1, 2), asteroid_size, asteroid_size))

    sprites_list = sprite.spritecollide(player, enemies, False)
    if sprites_list:
        scr.blit(lose, (175, 200))
        #player.image = transform.scale(image.load('rocket_ouch.png'), (player.width, player.height))
        finish = True


    if finish != True:
        scr.blit(background, (0,0))

        
        enemies.draw(scr)
        enemies.update()
        asteroids.draw(scr)
        asteroids.update()
        bullets.draw(scr)
        bullets.update()
        player.reset()
        player.update()
        
        if reload:
            time_to_time = timer()
            if (time_to_time - the_time) > 2:
                num_fire = 0
                reload = False
            else:
                reload_alert = qwerty.render(('reload: '+str(round((2-(time_to_time - the_time)), 1))), True, (200, 0, 0))
                scr.blit(reload_alert, (330, 480))
                
        f = 670
        if num_fire != full_mag:
            for i in range(full_mag - num_fire):
                scr.blit(bullet, (f, 10))
                f -= 25
                
        scr.blit(text_score, (10, 10))
        scr.blit(text_losses, (10, 30))

    clock.tick(FPS)
    display.update()
