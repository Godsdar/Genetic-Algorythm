class Obstacles:
    def __init__(self, root, canvas, rows, columns, h, space, color="red"):
        self.root = root
        self.canvas = canvas
        self.rows = rows
        self.columns = columns
        self.h = h
        self.space = space
        self.__color = color

    # Геттеры и сеттеры

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    def createObstacle(self, x, y):
        pos_index = self.columns * (y - 1) + x - 1

        # Если поле не занято, то устанавливаем там препятствие
        if self.space[pos_index] == 0:
            obstacle = self.canvas.create_rectangle((self.h * (x - 1), self.h * (y - 1)), (self.h * (x - 1) + self.h, self.h * (y - 1) + self.h), fill=self.__color)
            self.space[pos_index] = -1