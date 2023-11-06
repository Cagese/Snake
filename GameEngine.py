from random import randint, sample


class board:
    def __init__(self, height, weight):
        self.matrix = [['' for i in range(height)] for j in range(weight)]
        self.height = height
        self.weight = weight
        self.direction = ''
        self.snakes = []

    def __repr__(self):
        print('\n')
        for i in range(self.weight):
            for j in range(self.height):
                if self.matrix[i][j] == '':
                    print('-', end='')
                else:
                    print(self.matrix[i][j], end='')
            print('')
        return ''

    def add_snake(self):
        while True:
            try:
                player = Snake(self, color=(randint(100, 200), randint(100, 200), randint(100, 200)))
                x = randint(2, self.weight) - 1
                y = randint(1, self.height) - 1
                if self.matrix[x][y] == '' and self.matrix[x - 1][y] == '' and self.matrix[x + 1][y] == '':
                    self.matrix[x][y] = player.body[0]
                    player.x, player.y = x, y
                    player.body[0].x, player.body[0].y = x, y
                    self.snakes.append(player)
                    break
            except IndexError:
                continue

    def add_apple(self):
        x = randint(1, self.weight) - 1
        y = randint(1, self.height) - 1
        if self.matrix[x][y] == '' or self.matrix[x][y] == 'A':
            self.matrix[x][y] = 'A'

    def board_step(self):
        for snake in sample(self.snakes, len(self.snakes)):
            snake.snake_step()


class head:
    def __init__(self, direction='x-', x=0, y=0, color=(0, 0, 0)):
        self.direction = direction
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return 'H'


class part_of_body:
    def __init__(self, x=0, y=0, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return 'P'


class Snake:
    def __init__(self, board, x=0, y=0, color=(0, 0, 0)):
        self.board = board
        self.body = [head(color=tuple(randint(1, 50) + i for i in color))]
        self.x = x
        self.y = y
        self.points = 0
        self.color = color
        self.killed = False
        self.name=''

    def __str__(self):
        return 'S'

    def snake_step(self):
        if not (self.killed):
            saturated = False
            coefficient = {'x-': (-1, 0), 'x+': (1, 0), 'y+': (0, 1), 'y-': (0, -1)}
            x0, y0 = coefficient[self.body[0].direction]
            try:
                if str(self.board.matrix[self.x + x0][self.y + y0]) not in ['H',
                                                                            'P'] and 0 <= self.x + x0 <= self.board.weight and 0 <= self.y + y0 <= self.board.height:
                    if self.board.matrix[self.x + x0][self.y + y0] == 'A':
                        self.points += 20
                        self.board.add_apple()
                        saturated = True
                    self.body.insert(1, part_of_body(x=self.x, y=self.y, color=self.color))
                    self.board.matrix[self.x + x0][self.y + y0] = self.body[0]
                    self.board.matrix[self.x][self.y] = self.body[1]
                    if not saturated:
                        self.board.matrix[self.body[-1].x][self.body[-1].y] = ''
                        del self.body[-1]
                    self.y += y0
                    self.x += x0
                    self.body[0].y += y0
                    self.body[0].x += x0
                else:
                    raise IndexError
            except IndexError:
                self.kill()

    def kill(self):
        self.killed = True
        for i in self.body:
            self.board.matrix[i.x][i.y] = ''
