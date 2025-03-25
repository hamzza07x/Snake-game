import tkinter as tk
import random
import pygame
import os

GAME_WIDTH, GAME_HEIGHT = 1024, 768
INITIAL_SPEED = 300
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
HIGH_SCORE_FILE = "highscore.txt"
LEVEL_UP_SCORE = 15

pygame.mixer.init()
eatSound = pygame.mixer.Sound("eat.wav")
gameOverSound = pygame.mixer.Sound("game_over.wav")

window = None
canvas = None
scoreLabel = None

class Snake:
    def __init__(self):
        self.bodySize = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = [canvas.create_rectangle(0, 0, SPACE_SIZE, SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
                        for _ in range(BODY_PARTS)]

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def loadHighScore():
    if not os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write("0")
    with open(HIGH_SCORE_FILE, 'r') as f:
        return int(f.read())

def saveHighScore(new_score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(new_score))

def nextTurn():
    global score, food_obj, SPEED, level, direction

    x,y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food_obj.coordinates[0] and y == food_obj.coordinates[1]:
        score += 1
        scoreLabel.config(text=f"Score: {score}  Level: {level}")
        canvas.delete("food")
        food_obj = Food()
        eatSound.play()
        window.after(300, lambda: eatSound.stop())

        if score % LEVEL_UP_SCORE == 0:
            level += 1
            SPEED = max(50, SPEED - 10)

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if checkCollisions():
        gameOver()
    else:
        window.after(SPEED, nextTurn)

def changeDirection(new_direction):
    global direction
    opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    if new_direction != opposites.get(direction):
        direction = new_direction

def checkCollisions():
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    if (x, y) in snake.coordinates[1:]:
        return True
    return False

def gameOver():
    pygame.mixer.music.stop()
    gameOverSound.play()
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50, font=('consolas', 50), fill="red", text="GAME OVER")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 10, font=('consolas', 30), fill="white", text=f"Your Score: {score}")

    if score > loadHighScore():
        saveHighScore(score)
        canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50, font=('consolas', 25), fill="yellow", text="New High Score!")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 100, font=('consolas', 20), fill="white",
                       text="Press R to Restart or M for Menu or Q to Quit")

    window.bind('r', lambda event: restartGame())
    window.bind('m', lambda event: mainMenu())
    window.bind('q', lambda event: window.destroy())

def startGame():
    global snake, food_obj, direction, score, SPEED, level
    canvas.delete(tk.ALL)
    score = 0
    level = 1
    SPEED = INITIAL_SPEED
    direction = 'down'
    scoreLabel.config(text=f"Score: {score}  Level: {level}")
    snake = Snake()
    food_obj = Food()
    nextTurn()

def restartGame():
    startGame()

def showHighScore():
    high = loadHighScore()
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=('consolas', 40), fill="yellow", text=f"High Score: {high}")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 60, font=('consolas', 20), fill="white", text="Press M for Menu")
    window.bind('m', lambda event: mainMenu())

def mainMenu():
    pygame.mixer.music.stop()
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 100, font=('consolas', 50), fill="green", text="SNAKE GAME")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=('consolas', 30), fill="white", text="1. Play")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50, font=('consolas', 30), fill="white", text="2. High Score")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 100, font=('consolas', 30), fill="white", text="3. Quit")

    window.bind('1', lambda event: startGame())
    window.bind('2', lambda event: showHighScore())
    window.bind('3', lambda event: window.destroy())

def init_game(game_window, game_canvas, game_scoreLabel):
    global window, canvas, scoreLabel
    window = game_window
    canvas = game_canvas
    scoreLabel = game_scoreLabel