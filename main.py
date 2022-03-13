#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter import *
from random import randint as rd
from keyboard import KeyDetector
import time

WINDOW_WIDTH_NUMBER = 40
WINDOW_HEIGHT_NUMBER = 40
STARTING_SNAKE_LENGTH = 3

# root = Tk()
# w = Label(root, text=gameText)
# w.grid(row=0, column=0)
# root.mainloop()
# while True:
#     time.sleep(1)
#     random_insert()
#     update()
#     w['text'] = gameText
#     print(w['text'])
#     root.update()


class GameMap:

    def __init__(self, master, width, height, food_freq, snake_length):
        self.master = master
        self.map = [[0 for j in range(width)] for i in range(height)]
        self.mapWidth = width
        self.mapHeight = height
        self.foodFreq = food_freq
        self.turnCnt = 0
        self.foodPos = []
        self.snakeLength = snake_length
        self.snake = []
        self.direction = rd(0, 3)
        self.tailDirection = self.direction
        self.directionDict = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.turn_dict = [[[0, 0], [0, 0], [1, 0], [1, 1]],
                          [[0, 0], [0, 0], [1, 1], [1, 0]],
                          [[1, 0], [1, 1], [0, 0], [0, 0]],
                          [[1, 1], [1, 0], [0, 0], [0, 0]]]
        self.turnPointList = []
        self.other_init()
        self.update()

    def other_init(self):
        side_width = self.snakeLength
        snake_pos = [rd(0 + side_width, self.mapHeight - 1 - side_width),
                     rd(0 + side_width, self.mapWidth - 1 - side_width)]
        self.snake.append(snake_pos[:])
        # print(self.snake)
        pointing_direction = self.directionDict[self.direction]
        for i in range(self.snakeLength - 1):
            snake_pos[0] -= pointing_direction[0]
            snake_pos[1] -= pointing_direction[1]
            self.snake.append(snake_pos[:])
            # print(self.snake)

    def update(self):
        if self.master.DEBUG:
            print('self.direction = ', self.direction)
            print('direction = ', self.directionDict[self.direction])
        self.turnCnt += 1
        # if rd(1, 2) == 1:
        #     self.turn(rd(0, 1))
        # if rd(1, 5) == 1:
        #     self.snake_expand()
        self.gen_food()
        snake_pos = self.snake[0][:]
        self.snake = self.snake[:-1]
        snake_pos[0] += self.directionDict[self.direction][0]
        snake_pos[1] += self.directionDict[self.direction][1]
        if snake_pos[0] >= self.mapHeight:
            snake_pos[0] -= self.mapHeight
        if snake_pos[1] >= self.mapWidth:
            snake_pos[1] -= self.mapWidth
        if snake_pos[0] < 0:
            snake_pos[0] += self.mapHeight
        if snake_pos[1] < 0:
            snake_pos[1] += self.mapWidth
        if snake_pos in self.snake:
            return -1
        self.snake = [snake_pos[:]] + self.snake[:]
        if snake_pos in self.foodPos:
            self.foodPos.remove(snake_pos)
            self.snake_expand()
        if self.turnPointList:
            if self.snake[-1] == self.turnPointList[0][0]:
                self.tailDirection = self.turnPointList[0][1]
                self.turnPointList = self.turnPointList[1:]
        if self.master.DEBUG:
            print(self.tailDirection)
        self.update_map()
        return 0

    def update_map(self):
        self.map = [[0 for j in range(self.mapWidth)] for i in range(self.mapHeight)]
        for i in self.snake:
            self.map[i[0]][i[1]] = 1
        for i in self.foodPos:
            self.map[i[0]][i[1]] = 2

    def turn(self, direction):  # direction = 1 for left and 0 for right
        left_dict = [3, 2, 0, 1]
        right_dict = [2, 3, 1, 0]
        if direction == 1:
            self.direction = left_dict[self.direction]
        else:
            self.direction = right_dict[self.direction]
        self.turnPointList.append([self.snake[0], self.direction])

    def snake_expand(self):
        snake_pos = self.snake[-1][:]
        snake_pos[0] -= self.directionDict[self.tailDirection][0]
        snake_pos[1] -= self.directionDict[self.tailDirection][1]
        if snake_pos[0] >= self.mapHeight:
            snake_pos[0] -= self.mapHeight
        if snake_pos[1] >= self.mapWidth:
            snake_pos[1] -= self.mapWidth
        if snake_pos[0] < 0:
            snake_pos[0] += self.mapHeight
        if snake_pos[1] < 0:
            snake_pos[1] += self.mapWidth
        self.snake = self.snake[:] + [snake_pos[:]]

    def gen_food(self):
        if self.foodFreq <= 1:
            for i in range(int(1.0 / self.foodFreq)):
                pos = [rd(0, self.mapHeight - 1), rd(0, self.mapWidth - 1)]
                while pos in self.snake or pos in self.foodPos:
                    pos = [rd(0, self.mapHeight - 1), rd(0, self.mapWidth - 1)]
                self.foodPos.append(pos[:])
        elif self.turnCnt % self.foodFreq == 0:
            pos = [rd(0, self.mapHeight - 1), rd(0, self.mapWidth - 1)]
            while pos in self.snake or pos in self.foodPos:
                pos = [rd(0, self.mapHeight - 1), rd(0, self.mapWidth - 1)]
            self.foodPos.append(pos[:])

    def key_answer(self, key):
        tran_dict = {'w': 0, 's': 1, 'd': 2, 'a': 3}
        tmp_ans = tran_dict[key]
        if self.turn_dict[self.direction][tmp_ans][0] == 0:
            return
        self.turn(self.turn_dict[self.direction][tmp_ans][1])

    def answer(self, event):
        tran_dict = {'Up': 0, 'Down': 1, 'Right': 2, 'Left': 3}
        tmp_ans = tran_dict[event.widget['text']]
        # turn_dict[i][j]=[0/1, 0/1] i=cur_direction j=press
        if self.turn_dict[self.direction][tmp_ans][0] == 0:
            return
        self.turn(self.turn_dict[self.direction][tmp_ans][1])


class MainWindow:

    def __init__(self, master):
        self.master = master
        self.current_version = '1.0.1 Alpha Test'
        master.title('SNAKE by Feiyang Wu ' + self.current_version)
        self.FONT = ('Comic Sans', 15)
        self.DEBUG = 0
        self.WINDOW_WIDTH = WINDOW_WIDTH_NUMBER
        self.WINDOW_HEIGHT = WINDOW_HEIGHT_NUMBER
        self.BUTTON_WIDTH = 5
        self.BUTTON_HEIGHT = 3
        self.STARTING_SNAKE_LENGTH = STARTING_SNAKE_LENGTH
        self.BLANK = '□'
        self.FULL = '■'
        self.FOOD = '★'
        self.REFRESH_TIME = 100  # ms
        self.FOOD_FREQUENCY = 5  # turn per food
        self.gameMap = GameMap(self, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.FOOD_FREQUENCY, self.STARTING_SNAKE_LENGTH)
        self.gameText = ""
        self.mainLabel = Label(master=self.master, font=self.FONT)
        # self.buttonFrame = Frame(master=self.master)
        # self.buttonUp = Button(master=self.buttonFrame, text='Up', width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, font=self.FONT)
        # self.buttonDown = Button(master=self.buttonFrame, text='Down', width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, font=self.FONT)
        # self.buttonLeft = Button(master=self.buttonFrame, text='Left', width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, font=self.FONT)
        # self.buttonRight = Button(master=self.buttonFrame, text='Right', width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, font=self.FONT)
        self.keyDetector = KeyDetector()
        self.keyDetector.start()
        self.gameEnd = False
        self.other_init()

    def other_init(self):
        self.update()
        self.mainLabel.grid(row=0, column=0)
        # self.buttonFrame.grid(row=1, column=0)
        # self.buttonUp.grid(row=0, column=1)
        # self.buttonUp.bind('<Button-1>', self.gameMap.answer)
        # self.buttonDown.grid(row=2, column=1)
        # self.buttonDown.bind('<Button-1>', self.gameMap.answer)
        # self.buttonLeft.grid(row=1, column=0)
        # self.buttonLeft.bind('<Button-1>', self.gameMap.answer)
        # self.buttonRight.grid(row=1, column=2)
        # self.buttonRight.bind('<Button-1>', self.gameMap.answer)
        self.master.after(self.REFRESH_TIME, self.refresh)

    def refresh(self):
        # self.random_insert()
        for active_key in self.keyDetector.active_key:
            if active_key in ['w', 'a', 's', 'd']:
                self.gameMap.key_answer(active_key)
        self.keyDetector.clear()
        return_val = self.update()
        if return_val == -1:
            return
        self.mainLabel.update()
        self.master.after(self.REFRESH_TIME, self.refresh)

    def update(self):
        return_val = self.gameMap.update()
        if self.DEBUG:
            print(self.gameMap.snake)
        self.gameText = ""
        for i in range(self.WINDOW_HEIGHT):
            if return_val == -1 and i == int(self.WINDOW_HEIGHT / 2) - 1:
                blanks = self.BLANK * (int(self.WINDOW_WIDTH / 2 - 5))
                self.gameText += blanks + "GAME OVER" + blanks + "\n"
            else:
                for j in range(self.WINDOW_WIDTH):
                    self.gameText += self.FULL if self.gameMap.map[i][j] == 1 else self.FOOD if self.gameMap.map[i][j] == 2 else self.BLANK
                self.gameText += '\n'
        self.mainLabel['text'] = self.gameText
        return return_val

    def random_insert(self):
        for i in range(self.WINDOW_HEIGHT):
            for j in range(self.WINDOW_WIDTH):
                self.gameMap.map[i][j] = rd(0, 1)


root = Tk()
app = MainWindow(root)
root.mainloop()
