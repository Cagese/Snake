import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCloseEvent, QKeyEvent, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainUi import Ui_MainWindow as mainui
from gameUi import Ui_MainWindow as gameui


from GameEngine import *

# self.timer.timeout.connect(self.run)
# self.timer.start()
class MainMenu(QMainWindow, mainui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setCentralWidget(self.centralwidget)

        self.player_count = 1
        self.player_counter_slider.valueChanged.connect(self.count_player)
        self.Startbutton.clicked.connect(self.run)


    def count_player(self):
        self.player_count = self.player_counter_slider.value()
        self.label.setText(f'Количество игроков:{self.player_count}')

    def run(self):
        self.hide()
        self.game = Game(self)
        self.game.show()


class Game(QMainWindow, gameui):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        self.boardResolution = (10,10)
        self.setupUi(self)
        self.tps = QTimer()
        self.tps.setInterval(1000)
        self.tps.start()
        self.gameboard = board(*self.boardResolution)
        #self.tps.timeout.connect(self.step)
        for i in range(80):
            self.gameboard.add_apple()
        for i in range(parent.player_count):
            self.gameboard.add_snake(i)
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_flag(qp)
        qp.end()

    def draw_flag(self, qp):
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(30, 30, 120, 30)
        qp.setBrush(QColor(0, 255, 0))
        qp.drawRect(30, 60, 120, 30)
        qp.setBrush(QColor(0, 0, 255))
        qp.drawRect(30, 90, 120, 30)
    def step(self):
        print('\n')
        print(self.gameboard.snakes)
        self.gameboard.board_step()
        repr(self.gameboard)
    def closeEvent(self, QCloseEvent):
        self.tps.stop()
        self.parent.show()

    def keyPressEvent(self, QKeyEvent):
        players_directions = {1:{87:'x-',83:'x+',68:'y+',65:'y-'},
                              2:{16777235: 'x-', 16777237: 'x+', 16777236: 'y+', 16777234: 'y-'},
                              3:{70: 'x-', 86: 'x+', 66: 'y+', 67: 'y-'},
                              4:{79: 'x-', 76: 'x+', 59: 'y+', 75: 'y-'}}
        for index,i in enumerate(self.gameboard.snakes):
            try:
                new_direction=players_directions[index+1][int(QKeyEvent.key())]
                if not(i.body[0].direction[:1] == new_direction[:1] and i.body[0].direction[1:] != new_direction[1:]):
                    i.body[0].direction = players_directions[index+1][int(QKeyEvent.key())]
            except KeyError:
                continue
        self.step()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())
