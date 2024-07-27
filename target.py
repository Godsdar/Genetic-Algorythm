class Target:
    def __init__(self, root, canvas, rows, columns, h, space, color="blue"):
        self.root = root
        self.canvas = canvas
        self.rows = rows
        self.columns = columns
        self.h = h
        self.space = space
        self.__color = color

        # Атрибут показывает установлена ли цель
        self.__set = False

    # Геттеры и сеттеры

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    @property
    def set(self):
        return self.__set

    @set.setter
    def set(self, value):
        self.__set = value


    def createTarget(self, x, y):
        pos_index = self.columns * (y - 1) + x - 1

        # Если поле пусто и цель еще не установлена, то устанавливаем ее
        if self.space[pos_index] == 0 and self.__set == False:
            target = self.canvas.create_rectangle((self.h * (x - 1), self.h * (y - 1)), (self.h * (x - 1) + self.h, self.h * (y - 1) + self.h), fill=self.__color)
            self.space[pos_index] = 1
            self.__set = True