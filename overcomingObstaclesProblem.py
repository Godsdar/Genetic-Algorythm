from target import Target
from obstacles import Obstacles
from random import randint
import math

class OvercomingObstaclesProblem:
    def __init__(self, root, canvas, rows, columns, h, space, x, y, collision_weight=0.3):
        self.root = root
        self.canvas = canvas
        self.rows = rows
        self.columns = columns
        self.h = h
        self.space = space

        # В данной модели будет присутствовать вес столкновения, для правильной расстановки приоритетов (сократить дистанцию важнее, чем обойти все препятствия)
        self.__collision_weight = collision_weight
        self.__x = x
        self.__y = y
        self.__pos_index = self.columns * (y - 1) + x - 1

        # Инициализируем классы Target и Obstacles
        self.__target = Target(self.root, self.canvas, self.rows, self.columns, self.h, self.space)
        self.__obstacles = Obstacles(self.root, self.canvas, self.rows, self.columns, self.h, self.space)

    # Геттеры и сеттеры
    @property
    def collision_weight(self):
        return self.__collision_weight

    @collision_weight.setter
    def collision_weight(self, value):
        self.__target = value

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
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def obstacles(self):
        return self.__obstacles

    @obstacles.setter
    def obstacles(self, value):
        self.__obstacles = value

    # Метод, генерирующий случайное расположение цели и препятствий
    def generateRandomPosition(self, number_of_obstaсles):
        # Размещаем цель
        self.__target.createTarget(randint(1, self.columns), randint(1, self.rows))
        count = 0

        while count < number_of_obstaсles:
            x = randint(1, self.columns)
            y = randint(1, self.rows)
            index = self.columns * (y - 1) + x - 1

            # Если индекс, куда мы хотим установить препятствие не равен начальной позиции индивидуумов и не равен позиции цели, то устанавливаем там препятствие
            if index != self.__pos_index and self.space[index] != 1:
                self.__obstacles.createObstacle(x, y)
                count += 1

    # Данный метод нужен для трансформации хромосомы решения в последовательность координат местонахождения индивида
    def decodingRoute(self, route):
        current_pos = self.__pos_index # в этой переменной будет храниться текущая координата индивида
        decoded = [current_pos] # это список в котором хранится декодированная хромосома. Каждый элемент в нем, это новое значение переменной current_pos

        # В этом цикле мы в зависимости от значения элемента списка route, будем добавлять в список decoded декодированный аналог изначального элемента
        for i in range(len(route)):
            if route[i] == 1:
                decoded.append(current_pos - self.columns)
            elif route[i] == 2:
                decoded.append(current_pos + self.columns)
            elif route[i] == 3:
                decoded.append(current_pos - 1)
            elif route[i] == 4:
                decoded.append(current_pos + 1)

            # Изменяем значение current_pos на то, которое мы только что добавили в список decoded
            current_pos = decoded[i + 1]

        for i in range(len(route)):
            # Если декодированный индекс находится за пределами поля, то изменяем stop_index и выходим из цикла.
            # В условии можно наблюдать индексацию i + 1. Это связано с тем, что первый элемент decoded_route - начальная точка расположения индивида
            # Если в списке space по декодированному индексу располагается цель, то изменяем target_index и выходим из цикла
            if (decoded[i + 1] < 0 or decoded[i + 1] >= len(self.space) or i >= 1 and decoded[
                i] != 0 and
                    decoded[i] % self.columns == 0
                    and decoded[i + 1] + 1 == decoded[i] or i >= 1 and
                    decoded[i] % self.columns == 19 and decoded[i] != 0 and decoded[i + 1] - 1 ==
                    decoded[i]):
                decoded = decoded[:i + 1]
                break

        return decoded # Из-за того, что первый элемент decoded, это начальное положение индивида, длина decoded будет на 1 больше длины исходного списка

    # Данный метод вычисляет расстояние между двумя точками, по классической математической формуле
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Метод вычисляющий значения целевой функции
    def cost(self, route):
        # Декодируем хромосому
        decoded_route = self.decodingRoute(route)
        max_moves = len(route)

        stop_index = max_moves # Индекс остановки цикла
        target_index = max_moves # Индекс нахождения цели
        collisions = 0

        for i in range(len(decoded_route)):
            if self.space[decoded_route[i]] == 1:
                target_index = i
                break
            elif self.space[decoded_route[i]] == -1: # Если в списке space по декодированному индексу располагается препятствие, то увеличиваем collisions и выходим из цикла
                collisions += 1
        # Если мы достигли цели, то возвращаем значение целевой функции
        if target_index < max_moves:
            return collisions - (max_moves - target_index) / max_moves
        else:
            decoded_route = decoded_route[:stop_index]
            for i in range(max_moves):
                if self.space[i] == 1:
                    target_index = i

            target_x = (target_index + 1) % self.columns
            target_y = target_index // self.columns + 1
            current_x = (decoded_route[-1] + 1) % self.columns
            current_y = decoded_route[-1] // self.columns + 1

            # Если мы не достигли цели, то возвращаем расстояние между целью и индивидом сложенное с количеством столкновений умноженным на вес столкновения
            return self.distance(current_x, current_y, target_x, target_y) + collisions * self.__collision_weight