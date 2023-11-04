import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainUi import Ui_MainWindow as mainui
from gameUi import Ui_MainWindow as gameui

#self.timer.timeout.connect(self.run)
#self.timer.start()

class MainMenu(QMainWindow, mainui):


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.player_counter_slider.valueChanged.connect(self.count_player)
        self.Startbutton.clicked.connect(self.run)
    def count_player(self):
        global player_count
        player_count = self.player_counter_slider.value()
        self.label.setText(f'Количество игроков:{player_count}')
    def run(self):
        self.hide()
        self.game = Game(self)
        self.game.show()






class Game(QMainWindow, gameui):
    def __init__(self,parent=None):
        self.parent = parent
        super().__init__()
        self.setupUi(self)
    def closeEvent(self, QCloseEvent):
        self.parent.show()
    def keyPressEvent(self, QKeyEvent):
        print(QKeyEvent.key())


from random import randint

"""
class board:
    def __init__(self, height, weight):
        self.matrix = [['' for i in range(height)] for j in range(weight)]
        self.height = height
        self.weight = weight
        self.snakes = []

    def __repr__(self):
        for i in range(self.height):
            for j in range(self.weight):
                if self.matrix[i][j] == '':
                    print('-', end='')
                else:
                    print(self.matrix[i][j], end='')
            print('')

    def add_snake(self):
        while True:
            try:
                player = Snake(self,ID= randint(1,10000))
                x = randint(2, self.height) - 1
                y = randint(1, self.weight) - 1
                if self.matrix[x][y] == '' and self.matrix[x - 1][y] == '' and self.matrix[x + 1][y] == '':
                    self.matrix[x][y] = player.body[0]
                    player.x, player.y = x, y
                    player.body[0].x, player.body[0].y = x, y
                    self.snakes.append(player)
                    break
            except IndexError:
                continue

    def add_apple(self):
        x = randint(1, self.height) - 1
        y = randint(1, self.weight) - 1
        if self.matrix[x][y] == '':
            self.matrix[x][y] = 'A'

    def board_step(self):
        if not (any(self.matrix[x][y] == 'A' for x in range(self.height) for y in range(self.weight))):
            self.add_apple()
        for snake in self.snakes:
            snake.snake_step()


class head:
    def __init__(self, direction='w',x=0,y=0):
        self.direction = direction
        self.x = x
        self.y = y

    def __str__(self):
        return 'H'


class part_of_body:
    def __init__(self, direction='w', corner='', x=0, y=0):
        self.direction = direction
        self.corner = corner

        self.x = x
        self.y = y

    def __str__(self):
        return 'P'


class Snake:
    def __init__(self, board, x=0, y=0,ID=0):
        self.board = board
        self.body = [head()]
        self.x = x
        self.y = y
        self.ID = ID
    def __str__(self):
        return 'S'

    def snake_step(self):
        try:
            if self.body[0].direction == 'w' and self.board.matrix[self.x - 1][self.y] not in [head, part_of_body] and 0 <= self.x - 1 <= self.board.height:
                if self.board.matrix[self.x - 1][self.y] == 'A':
                    self.body.append(part_of_body(self.x,self.y))
                self.board.matrix[self.x - 1][self.y] = self.body[0]
                if len(self.body) == 1:
                    self.board.matrix[self.x][self.y] = ''
                else:
                    self.board.matrix[self.x][self.y] = self.body[1]
                self.x -= 1
                self.body[0].x -= 1
            else:
                raise IndexError
        except IndexError:
            self.kill()
    def kill(self):
        for i in self.body:
            self.board.matrix[i.x][i.y] = ''
        del self



x = board(10, 10)
x.add_snake()
x.add_snake()
x.add_snake()
x.add_snake()
x.add_snake()
x.add_snake()
x.__repr__()

for i in range(10):
    print('|||||||||||||')
    x.__repr__()
    x.board_step()
"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())