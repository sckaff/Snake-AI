import pygame, random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

# Score font
font = pygame.font.Font('avenir.ttf', 25)
# Snake body sprite
body = pygame.image.load('./img/body.png')
# Fruit sprite
fruit = pygame.image.load('./img/fruit.png')
# Screen coordinates
Point = namedtuple('Point', 'x, y')
# Size of each "box" in the game
BOX = 20
# Speed of the game
SPEED = 10000
# The background is white
BACKGROUND_COLOR = (255, 255, 255)
# The score text is black
TEXT_COLOR = (0, 0, 0)

# Enum for directions
class Directions(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Snake:
    
    # ---------- INITIALIZING THE SNAKE GAME ----------
    def __init__(self):
        self.w = 720
        self.h = 480
        windowSize = (self.w, self.h)
        
        self.display = pygame.display.set_mode(windowSize)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Snake's Bootcamp")
        
        self.reset()
        
    
    def reset(self):
        self.score = 0
        self.direction = Directions.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.body = [self.head, 
                        Point(self.head.x-BOX, self.head.y),
                        Point(self.head.x-(2*BOX), self.head.y)]
        
        self.food = None
        self.place_food()
        self.frame_iteration = 0
         
    # ---------- MOVING TO THE NEXT FRAME ----------
    def next_frame(self, action):
        self.frame_iteration += 1
        # 1. Check user input / events
        for event in pygame.event.get():
            # Qutting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        # 2. Moving the snake
        self.move(action)
        self.body.insert(0, self.head)
        
        # 3. Checking for game over
        reward = 0
        game_over = False
        if self.collision() or self.frame_iteration > 100*len(self.body):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. Checking for food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.body.pop()
        
        # 5. Updating the UI
        self.updateUI()
        self.clock.tick(SPEED)
        
        return reward, game_over, self.score
    
    # ---------- FUNCTION DEFINITIONS ----------
    
    # Updating the user interface
    def updateUI(self):
        self.display.fill(BACKGROUND_COLOR)
        for sb in self.body:
            self.display.blit(body, (sb.x,sb.y))
        self.display.blit(fruit, (self.food.x, self.food.y))
        
        text = font.render("Score: " + str(self.score), True, TEXT_COLOR)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    
    # Placing the food in the screen 
    def place_food(self):
        x = random.randint(0, (self.w-BOX )//BOX )*BOX 
        y = random.randint(0, (self.h-BOX )//BOX )*BOX
        self.food = Point(x, y)
        if self.food in self.body:
            self.place_food()
    
    # Checking for collision
    def collision(self, pt=None):
        if pt == None:
            pt = self.head
        if pt.x > self.w - BOX or pt.x < 0 or pt.y > self.h - BOX or pt.y < 0:
            return True
        if pt in self.body[1:]:
            return True
        return False
        
    # Updating the direction of the snake 
    def move(self, action):
        
        clock_wise = [Directions.RIGHT, Directions.DOWN, Directions.LEFT, Directions.UP]
        idx = clock_wise.index(self.direction)
        
        if np.array_equal(action, [1, 0, 0]):
            newdir = clock_wise[idx]
        elif np.array_equal(action, [1, 0, 0]):
            next_index = (idx + 1) % 4
            newdir = clock_wise[next_index]
        else:
            next_index = (idx - 1) % 4
            newdir = clock_wise[next_index]
            
        self.direction = newdir
        
        x = self.head.x
        y = self.head.y
        if self.direction == Directions.RIGHT:
            x += BOX
        elif self.direction == Directions.LEFT:
            x -= BOX
        elif self.direction == Directions.DOWN:
            y += BOX
        elif self.direction == Directions.UP:
            y -= BOX
            
        self.head = Point(x, y)