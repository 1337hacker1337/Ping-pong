from time import time as timer
from pygame import *
from random import choice

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        if player_image != None:
            self.image = transform.scale(image.load(player_image), (width, height))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_x, player_y, player_speed, width, height):
        self.image = Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_speed = player_speed

    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 20:
            self.rect.y -= self.player_speed
        if keys[K_s] and self.rect.y < 380:
            self.rect.y += self.player_speed

    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 20:
            self.rect.y -= self.player_speed
        if keys[K_DOWN] and self.rect.y < 380:
            self.rect.y += self.player_speed
        
class Ball(GameSprite):
    def __init__(self, player_x, player_y, player_speed_x, player_speed_y, width, height):
        self.image = Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y
        self.height = height
        self.width = width
        self.player_speed_x = player_speed_x
        self.player_speed_y = player_speed_y

    def update(self):
        self.rect.x += self.player_speed_x
        self.rect.y += self.player_speed_y
        
win_width = 900
win_height = 450
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-pong")

rocket_left = Player(30, 225, 3, 15, 50)
rocket_right = Player(870, 225, 3, 15, 50)

ball = Ball(450, 225, 4, 4, 18, 18)

player_left_score = 0
player_right_score = 0

score_timer = None
score_delay = 3

font.init()
font = font.Font("Kenney Mini.ttf", 24)

game = True
finish = False
clock = time.Clock()
FPS = 60
BG = (0, 0, 0)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        rocket_left.update_left()
        rocket_right.update_right()
        ball.update()

        if sprite.collide_rect(rocket_left, ball) or sprite.collide_rect(rocket_right, ball):
            ball.player_speed_x *= -1
            ball.player_speed_y *= -1

        if ball.rect.y > win_height - 15 or ball.rect.y < 0:
            ball.player_speed_y *= -1

        if ball.rect.x < 0:
            player_left_score += 1
            ball.rect.x = (win_width - ball.width) // 2
            ball.rect.y = (win_height - ball.height) // 2
            score_timer = timer()
            ball.player_speed_x = 0
            ball.player_speed_y = 0
            

        if ball.rect.x > win_width:
            player_right_score += 1
            ball.rect.x = (win_width - ball.width) // 2
            ball.rect.y = (win_height - ball.height) // 2
            score_timer = timer()
            ball.player_speed_x = 0
            ball.player_speed_y = 0

        if score_timer is not None and timer() - score_timer >= score_delay:
            finish = False
            score_timer = None
            ball.player_speed_x = choice([-4, 4])
            ball.player_speed_y = choice([-4, 4])

        window.fill(BG)

        rocket_left.reset()
        rocket_right.reset()
        ball.reset()

        score_left = font.render(f'score: {player_left_score}', True, (255, 255, 255))
        score_right = font.render(f'score: {player_right_score}', True, (255, 255, 255))

        window.blit(score_left, (0, 0))
        window.blit(score_right, (900 - score_right.get_width(), 0))

        display.update()
        clock.tick(FPS)

