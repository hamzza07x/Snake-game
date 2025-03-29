import tkinter as tk
import random
import pygame
import snakeGame as game

pygame.mixer.init()
def main():
    window = tk.Tk()
    window.title("Snake Game - Upgraded")
    window.resizable(False, False)

    score = 0
    level = 1
    direction = random.choice(['up', 'down', 'left', 'right'])
    SPEED = game.INITIAL_SPEED

    scoreLabel = tk.Label(window, text=f"Score: {score}  Level: {level}", font=('consolas', 30))
    scoreLabel.pack()

    canvas = tk.Canvas(window, bg=game.BACKGROUND_COLOR, width=game.GAME_WIDTH, height=game.GAME_HEIGHT)
    canvas.pack()

    window.update()
    window.geometry(f"{game.GAME_WIDTH}x{game.GAME_HEIGHT}+{(window.winfo_screenwidth() // 2) - (game.GAME_WIDTH // 2)}+{(window.winfo_screenheight() // 2) - (game.GAME_HEIGHT // 2)}")

    game.init_game(window, canvas, scoreLabel)

    window.bind('<Left>', lambda event: game.changeDirection('left'))
    window.bind('<Right>', lambda event: game.changeDirection('right'))
    window.bind('<Up>', lambda event: game.changeDirection('up'))
    window.bind('<Down>', lambda event: game.changeDirection('down'))

    window.bind('A', lambda event: game.changeDirection('left'))
    window.bind('D', lambda event: game.changeDirection('right'))
    window.bind('W', lambda event: game.changeDirection('up'))
    window.bind('S', lambda event: game.changeDirection('down'))
    window.bind('a', lambda event: game.changeDirection('left'))
    window.bind('d', lambda event: game.changeDirection('right'))
    window.bind('w', lambda event: game.changeDirection('up'))
    window.bind('s', lambda event: game.changeDirection('down'))

    game.mainMenu()
    window.mainloop()

if __name__ == '__main__':
    main()
