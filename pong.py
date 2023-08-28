import sys
import random
import pygame
from pygame.locals import *

pygame.init()

#Game specifications

window_width,window_height = 1000,600

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('PONG')

font = pygame.font.SysFont("ubuntumono", 20, True)
font2 = pygame.font.SysFont("ubuntumono", 35, True)

paddle_color = (255, 255, 255)
ball_color = (50,255,255)
white = paddle_color
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)


clock = pygame.time.Clock()
frame_rate = 35

#Ball Class
class Ball:

    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.ball = pygame.draw.circle(window, self.color,(self.posx, self.posy), self.radius)
        self.resetVar = 1
        self.xFac = 1
        self.yFac = -1

    def display(self):
        self.ball = pygame.draw.circle(window, self.color,(self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= window_height:
            self.yFac *= -1

        if self.posx <= 0 and self.resetVar:
            self.resetVar = 0
            return 1
        elif self.posx >= window_width and self.resetVar:
            self.resetVar = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = (window_width // 2)
        self.posy = (window_height // 2)
        self.xFac *= random.choice([-1, 1])
        self.resetVar = 1

    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball


#Paddle Class
class Paddle:

    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.prect = pygame.Rect(posx, posy, width, height)
        self.plit = pygame.draw.rect(window,self.color,self.prect)

    def display(self):
        self.plit = pygame.draw.rect(window, self.color, self.prect)

    def update(self,Yfac):
        self.posy = self.posy + self.speed * Yfac

        if self.posy <= 0:
            self.posy = 0

        elif self.posy + self.height >= window_height:
            self.posy = window_height - self.height

        self.prect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        window.blit(text, textRect)

    def getRect(self):
        return self.prect

# Middle Lines
def draw_lines():
    line_thickness = 3
    line_length = 30
    gap_length = 20

    num_lines = window_height // (line_length + gap_length)

    start_y = (window_height - (num_lines * (line_length + gap_length))) // 2

    for i in range(num_lines):
        y = start_y + i * (line_length + gap_length)

        pygame.draw.line(window, white, (window_width // 2, y),(window_width // 2, y + line_length // 2),line_thickness)

        pygame.draw.line(window, white,(window_width // 2, y + line_length // 2 + gap_length),(window_width // 2, y + line_length), line_thickness)

def draw_text(text,font,x,y):
    text = font.render(text, True,blue,green)
    window.blit(text, (x,y))


#Game
def main():
    running = False
    click = True

    paddle1 = Paddle(20, 0, 10, 100, 10, paddle_color)
    paddle2 = Paddle(window_width -30, 0, 10, 100, 10, paddle_color)
    ball = Ball(window_width // 2 , window_height // 2, 7, 7,ball_color)

    paddleList = [paddle1, paddle2]
    paddle1Score,paddle2Score = 0, 0
    paddle1Yfac, paddle2Yfac = 0, 0

    while click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                click = False
                running = True

        window.fill(black)
        draw_text('Click Anywhere to Start', font2, window_width // 2 - 200 , window_height // 2 - 50 )
        # draw_text('Use keys: W, S, Up, Down To handle Paddle',font, window_width // 3 , window_height // 3)
        pygame.display.flip()


    while running:
        window.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

        for paddle in paddleList:
            if pygame.Rect.colliderect(ball.getRect(),paddle.getRect()):
                ball.hit()

        paddle1.update(paddle1Yfac)
        paddle2.update(paddle2Yfac)

        point = ball.update()

        if point == -1:
            paddle1Score += 1
        elif point == 1:
            paddle2Score +=1


        if point:
            ball.reset()

        draw_lines()
        paddle1.display()
        paddle2.display()
        ball.display()

        paddle1.displayScore("Player 1 : ", paddle1Score, 100, 20, white)
        paddle2.displayScore("Player 2 : ", paddle2Score, window_width - 100, 20, white)

        pygame.display.update()
        clock.tick(frame_rate)
        pygame.display.flip()



if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()