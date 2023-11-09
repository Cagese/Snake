import sys

from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QCloseEvent, QKeyEvent, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QTableWidgetItem
from sqlite3 import connect as sqconnect
from mainUi import Ui_MainMenu as mainui
from gameUi import Ui_Game as gameui
from staticUi import Ui_Statics as staticui

from GameEngine import *


class MainMenu(QMainWindow, mainui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Главное меню")

        self.setCentralWidget(self.centralwidget)

        self.player_count = 1
        self.player_counter_slider.valueChanged.connect(self.count_player)
        self.Startbutton.clicked.connect(self.run)
        self.statisticbutton.clicked.connect(self.run_statics)

    def count_player(self):
        self.player_count = self.player_counter_slider.value()
        self.label.setText(f'Количество игроков:{self.player_count}')

    def run(self):
        self.hide()
        self.game = Game(self)
        self.game.show()

    def run_statics(self):
        self.hide()
        self.static = Statistic(self)
        self.static.show()


class Statistic(QMainWindow, staticui):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Статистика")
        self.parent = parent
        self.setupUi(self)
        self.sort.addItems(
            ["1_playergame_point", "2_playergame_point", "3_playergame_point", "4_playergame_point", "all_game_point"])
        self.connection = sqconnect("static.sqlite")
        self.sort.currentIndexChanged.connect(self.data_change)
        self.data_change()

    def data_change(self):
        sort = self.sort.currentIndex()
        query = f"""SELECT * from static"""
        res = sorted(self.connection.cursor().execute(query).fetchall(), key=lambda x: x[sort + 1], reverse=True)

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, QCloseEvent):
        self.parent.show()


class Game(QMainWindow, gameui):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        self.setWindowTitle('Snake')
        self.boardResolution = (40, 30)
        self.setupUi(self)
        self.gameboard = board(*self.boardResolution)

        controls_lables = [self.player1control, self.player2control, self.player3control, self.player4control]
        self.playercontrolhider(controls_lables)
        for i in range(parent.player_count):
            self.gameboard.add_snake()
            self.gameboard.add_apple()
            controls_lables[i].show()
            promt = "QTextBrowser { background-color: rgb(" + ', '.join(
                map(str, self.gameboard.snakes[i].body[0].color)) + ") }"
            controls_lables[i].setStyleSheet(promt)
        for index, snake in enumerate(self.gameboard.snakes):
            name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                    f"Игрок №{index + 1} введите своё имя")
            if ok_pressed:
                snake.name = name
            else:
                snake.name = ''
        self.tps = QTimer()
        self.tps.setInterval(300)
        self.tps.start()
        self.tps.timeout.connect(self.step)

        self.connection = sqconnect("static.sqlite")

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
        win = QMessageBox(self)
        if self.parent.player_count == 1:
            print('help')
            if self.gameboard.snakes[0].killed:
                win_player = self.gameboard.snakes[0]
                self.dbupdate(self.gameboard.snakes[0])
                if win_player.name.strip() != '':
                    win.setText(f"Игрок {win_player.name} выигрывает с очками: {win_player.points}")
                else:
                    win.setText(
                        f"Игрок {self.gameboard.snakes.index(win_player) + 1} выигрывает с очками: {win_player.points}")
                win.show()
                self.close()


        else:
            if sum([int(i.killed is False) for i in self.gameboard.snakes]) == 1:
                win_player = list(filter(lambda x: x.killed is False, self.gameboard.snakes))[0]
                self.dbupdate(win_player)
                if win_player.name.strip() != '':
                    win.setText(f"Игрок {win_player.name} выигрывает с очками: {win_player.points}")
                else:
                    win.setText(
                        f"Игрок {self.gameboard.snakes.index(win_player) + 1} выигрывает с очками: {win_player.points}")
                win.show()
                self.close()

    def dbupdate(self, win_player):
        if len(self.connection.cursor().execute(f"""SELECT * FROM static
    WHERE name = '{win_player.name.lower()}'""").fetchall()) == 1:
            old_data = self.connection.cursor().execute(f"""SELECT * FROM static
                WHERE name = '{win_player.name.lower()}'""").fetchone()
            need_update = ["1_playergame_point", "2_playergame_point", "3_playergame_point", "4_playergame_point"][
                len(self.gameboard.snakes) - 1]
            self.connection.cursor().execute(
                f"""UPDATE static set '{need_update}' = {max(int(win_player.points), int(old_data[len(self.gameboard.snakes)]))} WHERE name = '{win_player.name.lower()}'""")
            all_game_points = sum(old_data[1:-1])
            self.connection.cursor().execute(
                f"""UPDATE static set all_game_point = {all_game_points} WHERE name = '{win_player.name.lower()}'""")
            self.connection.commit()
        else:
            out_points = [0, 0, 0, 0, 0]
            out_points[len(self.gameboard.snakes) - 1] = win_player.points
            out_points[-1] = win_player.points
            o, t, fr, fo, all = out_points
            self.connection.cursor().execute(
                f"""INSERT INTO static VALUES('{win_player.name.lower()}',{o},{t},{fr},{fo},{all})""")
            self.connection.commit()

    def closeEvent(self, QCloseEvent):
        self.tps.stop()
        self.parent.show()

    def keyPressEvent(self, QKeyEvent):
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
