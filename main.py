from pygame import *

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
        self.player_speed = player_speed / 2
        super().__init__(None, player_x, player_y, player_speed, width, height)

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
        
win_width = 900
win_height = 450
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-pong")

rocket_left = Player(30, 225, 1, 15, 50)
rocket_right = Player(870, 225, 1, 15, 50)

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

        window.fill(BG)

        rocket_left.reset()
        rocket_right.reset()

        display.update()

