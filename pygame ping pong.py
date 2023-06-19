import pygame
import random
import time
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Ping Pong with pygame")

fontObj = pygame.font.Font("freesansbold.ttf",20)

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Striker:
    def __init__(self , xpos ,ypos , width, height ,speed , color):
        self.xpos=xpos
        self.ypos=ypos
        self.width=width
        self.height=height
        self.speed=speed
        self.color=color

        self.rect=pygame.Rect(xpos,ypos,width,height)
        self.player=pygame.draw.rect(screen,self.color,self.rect)
    def display(self):
        self.player=pygame.draw.rect(screen,self.color,self.rect)
    def update(self,yFac):
        self.ypos=self.ypos + yFac*self.speed
        if self.ypos<0:
            self.ypos=0
        elif self.ypos+self.height>HEIGHT:
            self.ypos=HEIGHT-self.height
        self.rect=pygame.Rect(self.xpos,self.ypos,self.width,self.height)   
    def displayScore(self,text,score,x,y,color):
        text=fontObj.render(text+str(score),True,color)
        textRect=text.get_rect()
        textRect.center=(x,y)
        screen.blit(text,textRect)
    def getRect(self):
        return self.rect
    

class Ball:
    def __init__(self,x,y,radius,speed,color) :
        self.x=x
        self.y=y
        self.radius=radius
        self.speed=speed
        self.color=color
        self.xFac=1
        self.yFac=-1
        self.ball=pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)
        self.firsthit=1

    def display(self):
        self.ball=self.ball=pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

    def update(self):
        self.x += self.speed*self.xFac
        self.y += self.speed*self.yFac

        if self.y<=0 or self.y>=HEIGHT:
            self.yFac=-self.yFac

        if self.x<=0 and self.firsthit:
            self.firsthit=0
            return 1
        elif self.x>=WIDTH and self.firsthit:
            self.firsthit=0
            return -1 
        else:
            return 0
    
    def reset(self):
        self.x=WIDTH//2
        self.y=HEIGHT//2
        self.xFac=-self.xFac
        self.firsthit=1
    
    def hit(self):
        self.xFac=-self.xFac
    
    def getRect(self):
        return self.ball
    
    
def main():
    loop = True
    player1=Striker(20,0,10,100,10,GREEN)
    player2=Striker(WIDTH-30,0,10,100,10,RED)
    ball=Ball(WIDTH//2,HEIGHT//2,7,7,WHITE)

    players=[player1 , player2]

    score_p1,score_p2=0,0
    p1_yfac,p2_yfac=0,0

    while loop:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop=False
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p2_yfac=-1
                if event.key == pygame.K_DOWN:
                    p2_yfac=1
                if event.key == pygame.K_w:
                    p1_yfac = -1
                if event.key == pygame.K_s:
                    p1_yfac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    p2_yfac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    p1_yfac = 0
            
        #collision detect
        for player in players:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()

        player1.update(p1_yfac)
        player2.update(p2_yfac)
        point = ball.update()


        if point == -1 :
            score_p1 +=1
        elif point == 1 :
            score_p2 +=1
        
        if point:
            ball.reset()

        player1.display()
        player2.display()
        ball.display()

        player1.displayScore("Player 1:",score_p1,100,20,WHITE)
        player2.displayScore("Player 2:",score_p2,WIDTH-100,20,WHITE)
        pygame.display.update()
        clock.tick(30)
    pygame.quit()

    
main()