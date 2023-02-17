import pygame
import random
from math import *
import time

''' IMPORTNT NOTE: This game uses Pygame Version 2.1.2  '''

''' define width and height  '''
width = 1000
height = 600

''' define colors  '''
black =  (0, 0, 0)
red = (255, 0, 0)
green = (95, 224, 72)
blue =  (41, 145, 254)
pink =  (240, 93, 254)               
yellow =  (241, 215, 36)
orange = (253, 96, 0)
white = (230, 230, 230)

''' define Ballon  '''
class Ballon():
    
    def __init__(self, dimension, range, speed):
        # randomly generate a color for the ballon
        self.color = random.choice([black, red, green, blue, pink, yellow, orange])
        # ballon's moving speed  
        self.speed = speed
        # ballon's moving direction
        self.direction = -1
        # dimensions
        self.range = range
        # ballon object
        self.ballon = pygame.Rect(dimension)
        # ballon line
        self.length = 70
        # ballon's state
        self.burst = False

    # move the ballon up and down
    def move(self):                  
        self.ballon.y += self.speed * self.direction

        if self.ballon.top <= self.range[0]:
            self.ballon.top = self.range[0]
            self.direction = 1   
        if self.ballon.bottom >= self.range[1]:
            self.ballon.bottom = self.range[1]
            self.direction = -1 

    # draw the ballon and line 
    def show(self):
        pygame.draw.line(display, (27, 172, 203), (self.ballon.x + self.ballon.w/2, self.ballon.y + self.ballon.h), (self.ballon.x + self.ballon.w/2, self.ballon.y + self.ballon.h + self.length))
        pygame.draw.ellipse(display, self.color, self.ballon)

    def check_bullet_collision(self, bullet):
        if pygame.Rect.colliderect(self.ballon, bullet) == True:
            self.burst = True

''' define Bullet  '''
class Bullet():
    
    def __init__(self, pos_x, pos_y, speed):
        self.color = random.choice([black, red, green, blue, pink, yellow, orange])
        self.bullet = pygame.Rect((pos_x, pos_y, 16, 16))
        self.direction = -1
        self.speed = speed

    def show(self):
        pygame.draw.rect(display, self.color, self.bullet)

    def move(self):
        self.bullet.x += self.speed * self.direction

''' define Cannon  '''   
class Cannon():

    def __init__(self, muzzle_dim, body_dimension):
        self.color = random.choice([black, red, green, blue, pink, yellow, orange])
        self.muzzle = pygame.Rect(muzzle_dim)
        self.body= pygame.Rect(body_dimension)

    def show(self):
        pygame.draw.rect(display, self.color, self.muzzle)
        pygame.draw.rect(display, self.color, self.body)

    def create_bullet(self):
        return Bullet(self.muzzle.x, self.muzzle.y + 12, 80)

''' main function '''
def game():  

    ''' Show missed shots on screen '''
    def show_missed_shots():

        scoreText = font.render("Missed Shots : " + str(missed_shots), True, black)
        display.blit(scoreText, (150, height - 100 + 50))

    ''' Show pygame version on screen '''
    def show_version():
        pg_version = font.render("Pygame Version : 2.1.2", True, black)
        display.blit(pg_version, (250, 30))

    ''' create game objects'''
    ballon = Ballon((30, 400, 60, 80), [0, 600], 8)
    cannon = Cannon((790, 470, 40, 40), (820, 450, 160, 80))

    bullet_group = []

    next_bullet_threshold = 0

    missed_shots = 0

    run = True

    while run:

        for event in pygame.event.get():             
            if event.type == pygame.QUIT:
                run = False 

        display.fill(white)  

        # stores keys pressed 
        keys = pygame.key.get_pressed()    

        # if down arrow key is pressed   
        if keys[pygame.K_UP] and cannon.body.y > 0:
            # move the cannon down
            cannon.muzzle.y -= 6
            cannon.body.y -= 6
          
        # if up arrow key is pressed   
        if keys[pygame.K_DOWN] and cannon.body.y < height - 80:
            # move the cannon up
            cannon.muzzle.y += 6
            cannon.body.y += 6

        bullet_current_time = pygame.time.get_ticks()
        # if the space key is pressed
        if keys[pygame.K_SPACE] and bullet_current_time > next_bullet_threshold:

            bullet_delay = 500 
            next_bullet_threshold = bullet_current_time + bullet_delay

            # shoot bullet
            bullet_group.append(cannon.create_bullet())

            # increase the count for missed shot 
            if not ballon.burst:
                missed_shots += 1

        cannon.show()

        ballon.show()
        ballon.move()

        for bullet in bullet_group:

            bullet.show()
            bullet.move()                      

             # check whether the bullet hits the ballon 
            ballon.check_bullet_collision(bullet.bullet)

            # stop the game when the bullet hits the ballon
            if ballon.burst:
                missed_shots -= 1
                run = False                        

        show_version()

        show_missed_shots()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

    exit()

if __name__ == "__main__":

    ''' initilize the pygame '''
    pygame.init()

    ''' set up the display '''
    display = pygame.display.set_mode((width, height), pygame.SCALED)
    pygame.display.set_caption("Balloon Shooter Game")
    clock = pygame.time.Clock()

    ''' initilize the font '''
    font = pygame.font.Font(None, 32)

    ''' run the main game function '''
    game()
