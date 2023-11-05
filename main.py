import sys
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QCloseEvent, QKeyEvent, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
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
        self.boardResolution = (40, 30)
        self.setupUi(self)
        self.tps = QTimer()
        self.tps.setInterval(300)
        self.tps.start()
        self.gameboard = board(*self.boardResolution)
        self.tps.timeout.connect(self.step)
        controls_lables = [self.player1control, self.player2control, self.player3control, self.player4control]
        self.playercontrolhider(controls_lables)
        for i in range(parent.player_count):
            self.gameboard.add_snake()
            self.gameboard.add_apple()
            controls_lables[i].show()
            promt = "QTextBrowser { background-color: rgb(" + ', '.join(
                map(str, self.gameboard.snakes[i].body[0].color)) + ") }"
            controls_lables[i].setStyleSheet(promt)

    def playercontrolhider(self, players):
        for i in players:
            i.hide()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_matrix(qp)
        qp.end()

    def draw_matrix(self, qp):
        qp.setBrush(QColor(0, 255, 0))
        qp.drawRect(QRect(100, 100, 800, 600))
        for x in range(self.gameboard.weight):
            for y in range(self.gameboard.height):
                if str(self.gameboard.matrix[x][y]) == '':
                    continue
                if str(self.gameboard.matrix[x][y]) == 'A':
                    qp.setBrush(QColor(255, 0, 0))
                else:
                    qp.setBrush(QColor(*self.gameboard.matrix[x][y].color))
                qp.drawRect(100 + y * 20, 100 + x * 20, 20, 20)

    def step(self):
        self.gameboard.board_step()
        self.update()
        self.game_over_check()

    def game_over_check(self):
        if self.parent.player_count == 1:
            if self.gameboard.snakes[0].killed:
                self.close()
        else:
            if sum([int(i.killed is False) for i in self.gameboard.snakes]) == 1:
                win_player = list(filter(lambda x: x.killed is False,self.gameboard.snakes))[0]
                win = QMessageBox(self)
                win.setText(f"Игрок {self.gameboard.snakes.index(win_player)} выигрывает с очками: {win_player.points}")
                win.show()
                self.close()


    def closeEvent(self, QCloseEvent):
        self.tps.stop()
        self.parent.show()

    def keyPressEvent(self, QKeyEvent):
        print(QKeyEvent.key())
        players_directions = {1: {87: 'x-', 83: 'x+', 68: 'y+', 65: 'y-'},
                              2: {56: 'x-', 53: 'x+', 54: 'y+', 52: 'y-'},
                              3: {70: 'x-', 86: 'x+', 66: 'y+', 67: 'y-'},
                              4: {79: 'x-', 76: 'x+', 59: 'y+', 75: 'y-'}}
        for index, i in enumerate(self.gameboard.snakes):
            try:
                new_direction = players_directions[index + 1][int(QKeyEvent.key())]
                if not (i.body[0].direction[:1] == new_direction[:1] and i.body[0].direction[1:] != new_direction[1:]):
                    i.body[0].direction = players_directions[index + 1][int(QKeyEvent.key())]
            except KeyError:
                continue


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())
