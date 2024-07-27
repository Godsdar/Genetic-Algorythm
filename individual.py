from tkinter import *

class Individual:
    def __init__(self, root, canvas, rows, columns, h, space, color, x, y):
        self.root = root
        self.canvas = canvas
        self.rows = rows
        self.columns = columns
        self.h = h
        self.space = space
        self.__color = color
        self.__x = x
        self.__y = y
        self.__pos_index = self.columns * (y - 1) + x - 1
        self.__image = self.canvas.create_oval((15 + self.h * (x - 1), 15 + self.h * (y - 1)), (35 + self.h * (x - 1), 35 + self.h * (y - 1)), fill=self.__color)
        self.__collisions = 0
        self.complete = False # цель еще не достигнута

    # Геттеры и сеттеры

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def pos_index(self):
        return self.__pos_index

    @pos_index.setter
    def pos_index(self, value):
        self.__pos_index = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def collisions(self):
        return self.__collisions

    @collisions.setter
    def collisions(self, value):
        self.__collisions = value

    # Метод реализующий движение индивида в зависимости от выбранного направления. Возвращает направление движения
    def move(self, direction):
        if direction == 1:
            self.__pos_index -= self.columns
            self.__y -= 1
        elif direction == 2:
            self.__pos_index += self.columns
            self.__y += 1
        elif direction == 3:
            self.__pos_index -= 1
            self.__x -= 1
        elif direction == 4:
            self.__pos_index += 1
            self.__x += 1

        if self.__x <= 0 or self.__x > self.columns or self.__y <= 0 or self.__y > self.rows: # Если после движения, индивид оказывается за пределами поля, это приравнивается к пяти столкновениям
            self.__collisions += 5
        elif self.space[self.__pos_index] == -1: # Если, совершив движение, индивид натыкается на препятствие, то счетчик столкновений увеличивается на единицу
            self.__collisions += 1
        elif self.space[self.__pos_index] == 1: # Если, совершив движение, индивид достигает цели, то атрибут complete принимает значение True
            self.complete = True

        return direction