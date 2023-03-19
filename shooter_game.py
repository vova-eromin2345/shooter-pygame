#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed,):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < w - 85:
            self.rect.x += self.speed

    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global score

        self.rect.y += self.speed
        if self.rect.y > h:
            self.rect.y = -50
            self.rect.x = randint(20, w-100)
            score += 1
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

w, h = 700, 500
window = display.set_mode((w, h))
display.set_caption('Shooter')
background = transform.scale(
    image.load('galaxy.jpg'), (w, h)
)

clock = time.Clock()

score = 0
killed = 0
goal = 10
max_lost = 3

life = 3
rel_time = False
num_fire = 0


mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
font.init()
text1 = font.Font(None, 36)
text2 = font.Font(None, 80)

win = text2.render('YOU WIN!', True, (138, 65, 5), (43, 240, 195))
lose = text2.render('ENEMY WIN!', True, (249, 100, 30), (199, 60, 128))
#! *****
text_name = text2.render('SHOOTER', True, (57, 190, 173), (40, 16, 70))
text_play = text2.render('PLAY - press "s"', True, (57, 190, 173), (40, 16, 70))
text_exit = text2.render('EXIT - press "e"', True, (57, 190, 173), (40, 16, 70))
#! *****

player = Player('rocket.png', 200, h-100, 80, 100, 5)
monsters = sprite.Group()
bullets = sprite.Group()

def respawn_enemy():
    
    monster = Enemy('ufo.png', randint(20, w-100), -50, 80, 50, randint(1, 4))
    monsters.add(monster)

def menu():
    global w, h
    background_menu = transform.scale( image.load('menu.jpg'), (w, h))
    
    menu = True
    while menu:
        window.blit(background_menu, (0, 0))
        for e in event.get():
            if e.type == QUIT:
                menu = False
            elif e.type == KEYDOWN :
                if e.key == K_s:
                    menu = False
                    game()  
                if e.key == K_e:
                    menu = False
        window.blit(text_name, (w//2-100, 100))
        window.blit(text_play, (w//2-150, 150))
        window.blit(text_exit, (w//2-150, 210))
        display.update()
def game():
    global score, killed, goal, max_lost, rel_time, num_fire, life
    for i in range(1, 6):
        respawn_enemy()
    finish = True
    game = True
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN :
                if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_fire += 1
                        fire_sound.play()
                        player.fire()
                    elif num_fire >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
        if not finish:
            window.blit(background, (0, 0))
            bullets.draw(window)
            bullets.update()
            
            player.reset()
            player.update()
            monsters.draw(window)
            monsters.update()
            
            if rel_time:
                now_time = timer()
                if now_time - last_time < 3:
                    reload = text1.render(f'Wait, reloading...', True, (127, 211, 123), (223, 65, 40))
                    window.blit(reload, (w//2-150, h-50))
                else:
                    num_fire = 0
                    rel_time = False
            text_killed = text1.render(f'Рахунок: {killed}', True, (255, 255, 255), Color('orange'))
            window.blit(text_killed, (20, 20))
            
            text_lost = text1.render(f'Пропущено: {score}', True, (135, 145, 240), (255, 255, 255))
            window.blit(text_lost, (20, 50))
            
            if score >= max_lost or sprite.spritecollide(player, monsters, True):
                
                window.blit(lose, (150, 200))
                display.update()
                time.delay(3000)
                finish = True
                game = False
                menu()
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for collide in collides:
                killed += 1
                respawn_enemy()
            if killed >= goal:
                finish = True
                window.blit(win, (150, 200))
                display.update()
                time.delay(3000)
        else:
            #time.delay(3000)
            killed = 0
            score = 0
            finish = False
            last_time = 0
            num_fire = 0
            bullets.empty()
            monsters.empty()
            for i in range(1, 6):
                respawn_enemy()
        display.update()
        clock.tick(40)
menu()