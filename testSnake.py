import pygame
import sys 
import random

# https://github.com/kiteco/python-youtube-code/blob/master/snake/snake.py 

#GLOBAL CONSTANTS
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

#LEGAL MOVES FOR THE SNAKE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

running = True

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))] # list of all positions of each block that snake is made of
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)
    
    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # when snake is one block it can go 4 directions
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        # when more, it can only go 3 directions (not reverse)
        else:
            self.direction = point

    def move(self):
        currentPos = self.get_head_position()
        x, y = self.direction
        newPos = (((currentPos[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (currentPos[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
        # check if game is over (our collision detection), [2:] checks if the new head of snake will hit a current part of the snake
        if len(self.positions) > 2 and newPos in self.positions[2:]:
            self.reset()
            running = False
        else:
            self.positions.insert(0, newPos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        #restart game, basically calling init again
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        running = False

    def draw(self, surface):
        # draw a block for each x, y block in the snake's positions list
        for pos in self.positions:
            r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)
    
    def handle_keys(self):
        # KEY EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # force a sys exit and close first the game, and then running script
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # yeah ion needa comment i think you know what's going on here
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_HEIGHT-1)*GRIDSIZE, random.randint(0, GRID_HEIGHT-1)*GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (32, 32, 32), r)
            else:
                # if a perfect grid cannot be drawn 
                r2 = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (64, 64, 64), r2)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    # draw screen and frames
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    # initialize classes, which is why we put capitals 
    snake = Snake()
    food = Food()
     
    score = 0

    FONT = pygame.font.SysFont("monospace", 16)

    while running:
        # increment our clock at 10 FPS
        clock.tick(10)
        snake.handle_keys()
        # fill background
        drawGrid(surface)
        
        snake.move()
        if snake.get_head_position() == food.position:
            # if snake head is on same x, y as a food it has eaten it 
            snake.length += 1
            score += 1
            # randomize x, y of next food bloock
            food.randomize_position()
        
        # before updating our screen/frame, we need to redraw the snake and food based on their new positions
        snake.draw(surface)
        food.draw(surface)
        
        # update screen on event
        screen.blit(surface, (0, 0))
        
        # display and update our score
        scoreDisplay = FONT.render("SCORE : {}".format(score), 1, (0, 0, 0))
        screen.blit(scoreDisplay, (5, 10))
        
        pygame.display.update()
        

main()