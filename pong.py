import pygame
from pygame.locals import *

pygame.init()

#game window size and font

window_width = 900
window_height = 600

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('PONG')

font = pygame.font.SysFont("Comic Sans MS", 25, True)

paddle_color = (255,255,255)
black = (0,0,0)


clock = pygame.time.Clock()
frame_rate = 60

my_ball = False
game_over = 0
score = 0

class Ball:
    #Ball class

    def __init__(self, x, y):
        self.radius = 10
        self.x = x - self.radius
        self.y = y - 50
        self.rect = Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.x_speed = 4
        self.y_speed = -4
        self.max_speed = 5
        self.game_over = 0

    def motion(self):
        pass

class Paddle:

    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = paddle_color
        self.rect = pygame.Rect(posx,posy,width,height)
        self.blit = pygame.draw.rect(window,self.color,self.rect)

    def display(self):
        self.blit = pygame.draw.rect(window, self.color, self.rect)

    def update(self):
        pass




#Game
def main():


    run = True

    paddle1 = Paddle()
    paddle2 = Paddle()
    ball = Ball()

    PaddleList = [paddle1,paddle2]
    paddle1Score,paddle2Score = 0, 0
    paddle1Yfac, paddle2Yfac = 0, 0

    while run:
        window.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddle2Yfac = -1
                if event.key == pygame.K_DOWN:
                    paddle2Yfac = 1
                if event.key == pygame.K_w:
                    paddle1Yfac = -1
                if event.key == pygame.K_s:
                    paddle1Yfac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle2Yfac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle1Yfac = 0





if __name__ == "__main__":
    main()
    pygame.quit()