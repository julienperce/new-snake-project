import pygame
import sys
import random
import time

# https://github.com/kiteco/python-youtube-code/blob/master/snake/snake.py

# GLOBAL CONSTANTS
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# COLOR CONSTANTS
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)

# LEGAL MOVES FOR THE SNAKE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake(object):
    currentColor = RED
    score = 0

    def __init__(self):
        self.length = 1
        self.positions = [
            ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
        ]  # list of all positions of each block that snake is made of
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = RED
        """self.score = 0"""

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
        newPos = (
            ((currentPos[0] + (x * GRIDSIZE)) % SCREEN_WIDTH),
            (currentPos[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT,
        )
        # check if game is over (our collision detection), [2:] checks if the new head of snake will hit a current part of the snake
        if len(self.positions) > 2 and newPos in self.positions[2:]:
            deathSound = pygame.mixer.Sound("sounds/snake_hits_itself.wav")
            deathSound.set_volume(0.2)
            deathSound.play()
            time.sleep(1)
            pygame.mixer.stop()
            end_game()
        else:
            self.positions.insert(0, newPos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        # restart game, basically calling init again
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        # draw a block for each x, y block in the snake's positions list
        for pos in self.positions:
            r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.currentColor, r)
            pygame.draw.rect(surface, (255, 255, 255), r, 1)

    def handle_keys(self):
        # KEY EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # force a sys exit and close first the game, and then running script
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # yeah ion needa comment i think you know what's going on here
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.turn(RIGHT)


class Food(object):
    foodCurrentColor = ORANGE
    foodCurrentColorName = "ORANGE"  # make sure to set as str
    r2color = random.choice(COLORS)
    r2colorHard = random.choice(COLORS)
    r3colorHard = random.choice(COLORS)
    r4colorHard = random.choice(COLORS)

    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.randomize_position()

    def randomize_position(self):
        self.position1 = (
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
        )
        self.position2 = (
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
        )

    def draw(self, surface):
        r1 = pygame.Rect((self.position1[0], self.position1[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.foodCurrentColor, r1)
        pygame.draw.rect(surface, (0, 0, 0), r1, 1)
        r2 = pygame.Rect((self.position2[0], self.position2[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.r2color, r2)
        pygame.draw.rect(surface, (0, 0, 0), r2, 1)

    def randomize_position_hard(self):
        self.hardposition1 = (
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
        )
        self.hardposition2 = (
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
        )
        self.hardposition3 = (
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
        )
        self.hardposition4 = (
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
        )

    def draw_hard(self, surface):
        r1hard = pygame.Rect(
            (self.hardposition1[0], self.hardposition1[1]), (GRIDSIZE, GRIDSIZE)
        )
        pygame.draw.rect(surface, self.foodCurrentColor, r1hard)
        pygame.draw.rect(surface, (0, 0, 0), r1hard, 1)
        r2hard = pygame.Rect(
            (self.hardposition2[0], self.hardposition2[1]), (GRIDSIZE, GRIDSIZE)
        )
        pygame.draw.rect(surface, self.r2colorHard, r2hard)
        pygame.draw.rect(surface, (0, 0, 0), r2hard, 1)
        r3hard = pygame.Rect(
            (self.hardposition3[0], self.hardposition3[1]), (GRIDSIZE, GRIDSIZE)
        )
        pygame.draw.rect(surface, self.r3colorHard, r3hard)
        pygame.draw.rect(surface, (0, 0, 0), r3hard, 1)
        r4hard = pygame.Rect(
            (self.hardposition4[0], self.hardposition4[1]), (GRIDSIZE, GRIDSIZE)
        )
        pygame.draw.rect(surface, self.r4colorHard, r4hard)
        pygame.draw.rect(surface, (0, 0, 0), r4hard, 1)


def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (32, 32, 32), r)
            else:
                # if a perfect grid cannot be drawn
                r2 = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (64, 64, 64), r2)


def main():
    # draw screen and frames
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    # initialize classes, which is why we put capitals
    snake = Snake()
    food = Food()

    pygame.display.set_caption("SNAKE 3001 -- easy")

    loopOST = pygame.mixer.Sound("sounds/easy_diff.wav")
    loopOST.set_volume(0.1)
    loopOST.play(-1)  # -1 makes the sound loop forever when it ends

    while True:
        # increment our clock at x FPS
        clock.tick(10)
        snake.handle_keys()
        # fill background
        drawGrid(surface)

        snake.move()
        if (
            snake.get_head_position() == food.position1
            or snake.get_head_position() == food.position2
        ):
            if (
                snake.get_head_position() == food.position2
                and food.r2color != food.foodCurrentColor
            ):
                pygame.mixer.stop()
                deathSound = pygame.mixer.Sound("sounds/eats_wrong_color.wav")
                deathSound.set_volume(0.2)
                deathSound.play()
                time.sleep(1)
                end_game()
            else:
                if snake.currentColor == RED:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = ORANGE
                    food.foodCurrentColor = YELLOW
                    food.foodCurrentColorName = "YELLOW"
                    food.r2color = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position()
                elif snake.currentColor == ORANGE:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = YELLOW
                    food.foodCurrentColor = GREEN
                    food.foodCurrentColorName = "GREEN"
                    food.r2color = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position()
                elif snake.currentColor == YELLOW:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = GREEN
                    food.foodCurrentColor = BLUE
                    food.foodCurrentColorName = "BLUE"
                    food.r2color = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position()
                elif snake.currentColor == GREEN:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = BLUE
                    food.foodCurrentColor = INDIGO
                    food.foodCurrentColorName = "INDIGO"
                    food.r2color = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position()
                elif snake.currentColor == BLUE:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = INDIGO
                    food.foodCurrentColor = VIOLET
                    food.foodCurrentColorName = "VIOLET"
                    food.r2color = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position()
                elif snake.currentColor == INDIGO:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = VIOLET
                    food.foodCurrentColor = RED
                    food.foodCurrentColorName = "RED"
                    food.r2color = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position()
                elif snake.currentColor == VIOLET:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = RED
                    food.foodCurrentColor = ORANGE
                    food.foodCurrentColorName = "ORANGE"
                    food.r2color = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position()
                collectSound = pygame.mixer.Sound("sounds/collect_food.wav")
                collectSound.set_volume(0.05)
                collectSound.play()

        # before updating our screen/frame, we need to redraw the snake and food based on their new positions
        snake.draw(surface)
        food.draw(surface)

        # update screen on event
        screen.blit(surface, (0, 0))

        # display and update our score
        scoreDisplay = FONT.render("SCORE : {}".format(snake.score), 1, (255, 255, 255))
        # for asthetic effect, put nextColor in the color (possibly find a new way to structure this one day?)
        if food.foodCurrentColor == RED:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, RED
            )
        if food.foodCurrentColor == ORANGE:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, ORANGE
            )
        if food.foodCurrentColor == YELLOW:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, YELLOW
            )
        if food.foodCurrentColor == GREEN:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, GREEN
            )
        if food.foodCurrentColor == BLUE:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, BLUE
            )
        if food.foodCurrentColor == INDIGO:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, INDIGO
            )
        if food.foodCurrentColor == VIOLET:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, VIOLET
            )

        screen.blit(scoreDisplay, (5, 10))
        screen.blit(nextDisplay, (550, 10))

        pygame.display.update()


def main_hard():
    # draw screen and frames
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    # initialize classes, which is why we put capitals
    snake = Snake()
    food = Food()

    pygame.display.set_caption("SNAKE 3001 -- hard")

    loopOST = pygame.mixer.Sound("sounds/hard_diff.wav")
    loopOST.set_volume(0.2)
    loopOST.play(-1)

    food.randomize_position_hard()  # call this before drawing to make sure our position variables exist before being referenced

    while True:
        # increment our clock at x FPS
        clock.tick(30)
        snake.handle_keys()
        # fill background
        drawGrid(surface)

        snake.move()
        if (
            snake.get_head_position() == food.hardposition1
            or snake.get_head_position() == food.hardposition2
            or snake.get_head_position() == food.hardposition3
            or snake.get_head_position() == food.hardposition4
        ):
            if (
                snake.get_head_position() == food.hardposition2
                and food.r2colorHard != food.foodCurrentColor
            ):
                pygame.mixer.stop()
                deathSound = pygame.mixer.Sound("sounds/eats_wrong_color.wav")
                deathSound.set_volume(0.2)
                deathSound.play()
                print(snake.score)
                time.sleep(1)
                end_game()
            if (
                snake.get_head_position() == food.hardposition3
                and food.r3colorHard != food.foodCurrentColor
            ):
                pygame.mixer.stop()
                deathSound = pygame.mixer.Sound("sounds/eats_wrong_color.wav")
                deathSound.set_volume(0.2)
                deathSound.play()
                print(snake.score)
                time.sleep(1)
                end_game()
            if (
                snake.get_head_position() == food.hardposition4
                and food.r4colorHard != food.foodCurrentColor
            ):
                pygame.mixer.stop()
                deathSound = pygame.mixer.Sound("sounds/eats_wrong_color.wav")
                deathSound.set_volume(0.2)
                deathSound.play()
                print(snake.score)
                time.sleep(1)
                end_game()
            else:
                if snake.currentColor == RED:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = ORANGE
                    food.foodCurrentColor = YELLOW
                    food.foodCurrentColorName = "YELLOW"
                    food.r2color = random.choice(COLORS)
                    food.r3colorHard = random.choice(COLORS)
                    food.r4colorHard = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position_hard()
                elif snake.currentColor == ORANGE:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = YELLOW
                    food.foodCurrentColor = GREEN
                    food.foodCurrentColorName = "GREEN"
                    food.r2color = random.choice(COLORS)
                    food.r3colorHard = random.choice(COLORS)
                    food.r4colorHard = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position_hard()
                elif snake.currentColor == YELLOW:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = GREEN
                    food.foodCurrentColor = BLUE
                    food.foodCurrentColorName = "BLUE"
                    food.r2color = random.choice(COLORS)
                    food.r3colorHard = random.choice(COLORS)
                    food.r4colorHard = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position_hard()
                elif snake.currentColor == GREEN:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = BLUE
                    food.foodCurrentColor = INDIGO
                    food.foodCurrentColorName = "INDIGO"
                    food.r2color = random.choice(COLORS)
                    food.r3colorHard = random.choice(COLORS)
                    food.r4colorHard = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position_hard()
                elif snake.currentColor == BLUE:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = INDIGO
                    food.foodCurrentColor = VIOLET
                    food.foodCurrentColorName = "VIOLET"
                    food.r2color = random.choice(COLORS)
                    food.r3colorHard = random.choice(COLORS)
                    food.r4colorHard = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position_hard()
                elif snake.currentColor == INDIGO:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = VIOLET
                    food.foodCurrentColor = RED
                    food.foodCurrentColorName = "RED"
                    food.r2color = random.choice(COLORS)
                    food.r3colorHard = random.choice(COLORS)
                    food.r4colorHard = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position_hard()
                elif snake.currentColor == VIOLET:
                    # if snake head is on same x, y as a food it has eaten it
                    snake.currentColor = RED
                    food.foodCurrentColor = ORANGE
                    food.foodCurrentColorName = "ORANGE"
                    food.r2color = random.choice(COLORS)
                    food.r3colorHard = random.choice(COLORS)
                    food.r4colorHard = random.choice(COLORS)
                    snake.length += 1
                    snake.score += 1
                    # randomize x, y of next food block
                    food.randomize_position_hard()
                collectSound = pygame.mixer.Sound("sounds/collect_food.wav")
                collectSound.set_volume(0.05)
                collectSound.play()

        # before updating our screen/frame, we need to redraw the snake and food based on their new positions
        snake.draw(surface)
        food.draw_hard(surface)

        # update screen on event
        screen.blit(surface, (0, 0))
        # display and update our score
        scoreDisplay = FONT.render("SCORE : {}".format(snake.score), 1, (255, 255, 255))
        # for asthetic effect, put nextColor in the color (possibly find a new way to structure this one day?)
        if food.foodCurrentColor == RED:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, RED
            )
        if food.foodCurrentColor == ORANGE:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, ORANGE
            )
        if food.foodCurrentColor == YELLOW:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, YELLOW
            )
        if food.foodCurrentColor == GREEN:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, GREEN
            )
        if food.foodCurrentColor == BLUE:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, BLUE
            )
        if food.foodCurrentColor == INDIGO:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, INDIGO
            )
        if food.foodCurrentColor == VIOLET:
            nextDisplay = FONT.render(
                "NEXT : {}".format(food.foodCurrentColorName), 1, VIOLET
            )

        screen.blit(scoreDisplay, (5, 10))
        screen.blit(nextDisplay, (550, 10))

        pygame.display.update()


def main_menu():
    menu = True
    selected = "easy"
    clock.tick(10)

    pygame.display.set_caption("SNAKE 3001")

    menuOST = pygame.mixer.Sound("sounds/title_screen.wav")
    menuOST.set_volume(0.2)
    menuOST.play(-1)

    eventTypes = (pygame.QUIT, pygame.KEYDOWN)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = "easy"
                    pygame.mixer.stop()
                    main()
                if event.key == pygame.K_2:
                    selected = "hard"
                    pygame.mixer.stop()
                    main_hard()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)

        title = pygame.image.load("img/new_title.png")
        screen.blit(title, (0, 0))

        pygame.display.update()


def end_game():
    endMenu = True
    clock.tick(10)

    pygame.display.set_caption("SNAKE 3001 -- game over")

    endOST = pygame.mixer.Sound("sounds/Space.mp3")
    endOST.set_volume(0.1)
    endOST.play(-1)

    endQuotes = [
        "'We are healed of a suffering only by experiencing it in full.' - Marcel Proust",
        "'Suffering is one of life's greatest teachers.' - Bryant McGill",
        "'Success is not final, failure is not fatal: it is the courage to continue that counts.' - Winston Churchill",
        "'A bend in the road is not the end of the road... unless you fail to make the turn.' - Helen Keller",
        "'Failure is only the opportunity to begin again, this time more intelligently.' - Henry Ford",
        "'Fall seven times and stand up eight.' - Japanese Proverb",
        "'Perseverance, secret of all triumphs.' - Victor Hugo",
        "'In general, any form of exercise, if pursued continuously, will help us train in perseverance.' - Mao Zedong",
        "'Every accomplishment starts with the decision to try. ' - John F. Kennedy",
        "'With every death, comes honor. With honor - redemption.' - Hanzo Shimada",
    ]
    quote = random.choice(endQuotes)

    while endMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.mixer.stop()
                    main()
                if event.key == pygame.K_2:
                    pygame.mixer.stop()
                    main_hard()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_c:
                    credits_menu()
                if event.key == pygame.K_m:
                    pygame.mixer.stop()
                    main_menu()

        screen.fill(BLACK)

        snake = Snake()

        quoteFONT = pygame.font.SysFont("DejaVu Serif", 13, bold=False, italic=True)
        quoteShow = quoteFONT.render(quote, 1, WHITE)

        endScreen = pygame.image.load("img/end_screen.png")

        scoreText = quoteFONT.render("Score: embarassingly low", 1, WHITE)

        # Main Menu Text
        screen.blit(endScreen, (0, 0))
        screen.blit(quoteShow, (10, 250))
        screen.blit(scoreText, (10, 220))
        pygame.display.update()


def credits_menu():
    creditsMenu = True

    clock.tick(10)
    pygame.display.set_caption("SNAKE 3001 -- credits")

    while creditsMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.mixer.stop()
                    main()
                if event.key == pygame.K_2:
                    pygame.mixer.stop()
                    main_hard()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_m:
                    pygame.mixer.stop()
                    main_menu()

        screen.fill(BLACK)

        creditImg = pygame.image.load("img/test_end1.png")
        screen.blit(creditImg, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()  # init mixer to play sound
    FONT = pygame.font.SysFont("arial", 16, bold=True)
    clock = pygame.time.Clock()
    main_menu()
