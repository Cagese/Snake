import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainUi import Ui_MainWindow as mainui
from gameUi import Ui_MainWindow as gameui


from GameEngine import board

# self.timer.timeout.connect(self.run)
# self.timer.start()
class MainMenu(QMainWindow, mainui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setCentralWidget(self.centralwidget)

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
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        self.boardResolution = (10,10)
        self.setupUi(self)
        self.tps = QTimer()
        self.tps.setInterval(1000)
        self.tps.start()
        self.gameboard = board(*self.boardResolution)
        self.tps.timeout.connect(self.step)
    def step(self):
        pass
    def closeEvent(self, QCloseEvent):
        self.tps.stop()
        self.parent.show()

    def keyPressEvent(self, QKeyEvent):
        print(QKeyEvent.key())





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())
