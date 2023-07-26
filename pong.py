import pygame
from pygame.locals import *

pygame.init()

#game specifications

window_width,window_height = 900,600

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('PONG')

font = pygame.font.SysFont("Comic Sans MS", 25, True)

paddle_color = (255,255,255)
white = paddle_color
black = (0,0,0)


clock = pygame.time.Clock()
frame_rate = 60

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

        if self.posx  <=0 or self.resetVar:
            self.resetVar = 0 
            return 1

        if self.posy <= 0 or self.posy >= window_height:
            self.yFac *=-1
        
        elif self.posx >= window_width and self.resetVar:
            self.resetVar = 0
            return -1
        
        else:
            return 0

    def reset(self):
        self.posx = window_width // 2
        self.posy = window_height // 2
        self.xFac *= -1
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
        self.rect = pygame.Rect(posx, posy, width, height)
        self.blit = pygame.draw.rect(window,self.color,self.rect)

    def display(self):
        self.blit = pygame.draw.rect(window, self.color, self.rect)

    def update(self,Yfac):
        self.posy = self.posy + self.speed * Yfac

        if self.posy <= 0:
            self.posy = 0

        elif self.posy + self.height >= window_height:
            self.posy = window_height - self.height

        self.rect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        window.blit(text, textRect)

    def getRect(self):
        return self.rect


#Game
def main():
    run = True

    paddle1 = Paddle(20,0,10,100,10,paddle_color)
    paddle2 = Paddle(window -30, 0, 10, 100, 10, paddle_color)
    ball = Ball(window_width // 2 , window_height // 2, 7, 7,white)

    paddleList = [paddle1, paddle2]
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

            paddle1.display()
            paddle2.display()
            ball.display()

        paddle1.displayScore("Paddle 1 : ", paddle1Score, 100, 20, white)
        paddle2.displayScore("Paddle 2 : ", paddle2Score, window_width - 100, 20, white)

        pygame.display.update()
        clock.tick(frame_rate)



if __name__ == "__main__":
    main()
    pygame.quit()