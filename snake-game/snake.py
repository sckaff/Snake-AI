import pygame, random
from enum import Enum
from collections import namedtuple

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
SPEED = 20
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
        
        self.score = 0
        self.display = pygame.display.set_mode(windowSize)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("The game of snakes!")
        
        self.direction = Directions.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.body = [self.head, 
                        Point(self.head.x-BOX, self.head.y),
                        Point(self.head.x-(2*BOX), self.head.y)]
        
        self.place_food()
         
    # ---------- MOVING TO THE NEXT FRAME ----------
    def next_frame(self):
        # 1. Check user input / events
        for event in pygame.event.get():
        
            # Qutting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # Pressing a key
            if event.type == pygame.KEYDOWN: 
                if self.direction == Directions.RIGHT or self.direction == Directions.LEFT:  
                    if event.key == pygame.K_UP:
                        self.direction = Directions.UP
                    if event.key == pygame.K_DOWN:
                        self.direction = Directions.DOWN
                elif self.direction == Directions.UP or self.direction == Directions.DOWN:  
                    if event.key == pygame.K_LEFT:
                        self.direction = Directions.LEFT
                    if event.key == pygame.K_RIGHT:
                        self.direction = Directions.RIGHT
                
        # 2. Moving the snake
        self.move(self.direction) # update the head
        self.body.insert(0, self.head)
        
        # 3. Checking for game over
        game_over = False
        if self.collision():
            game_over = True
            return game_over, self.score

        # 4. Checking for food
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.body.pop()
        
        # 5. Updating the UI
        self.updateUI()
        self.clock.tick(SPEED)
        
        return game_over, self.score
    
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
    def collision(self):
        if self.head.x > self.w - BOX or self.head.x < 0 or self.head.y > self.h - BOX or self.head.y < 0:
            return True
        if self.head in self.body[1:]:
            return True
        return False
        
    # Updating the direction of the snake 
    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Directions.RIGHT:
            x += BOX
        elif direction == Directions.LEFT:
            x -= BOX
        elif direction == Directions.DOWN:
            y += BOX
        elif direction == Directions.UP:
            y -= BOX
            
        self.head = Point(x, y)

# ---------- RUNNING THE GAME ----------
if __name__ == "__main__":
    snake = Snake()
    # Game loop
    while True:
        game_over, score = snake.next_frame()
        if (game_over == True):
            break
    # Quitting the game
    print("Final Score: " + str(score))
    pygame.quit()