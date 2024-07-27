import time
from individual import Individual
from overcomingObstaclesProblem import OvercomingObstaclesProblem

# В этом проекте мы воспользуемся фреймворком DEAP для реализации генетических алгоритмов
from deap import base
from deap import creator
from deap import tools

import random

class GeneticAlgorithm:
    def __init__(self, root, canvas, rows, columns, h, space, x, y, population_size, p_crossover, p_mutation, max_generations, generation_label, continuous, colors):
        self.root = root
        self.canvas = canvas
        self.rows = rows
        self.columns = columns
        self.h = h
        self.space = space

        # Координаты начальной клетки
        self.__x = x
        self.__y = y
        self.__population_size = population_size # Размер популяции в каждом поколении
        self.__p_crossover = p_crossover # Вероятность кроссинговера
        self.__p_mutation = p_mutation # Вероятность мутации
        self.__max_generations = max_generations # Максимальное число поколений
        self.__generation_counter = 1 # Счетчик поколений
        self.__generation_label = generation_label
        self.__continuous = continuous # Число поколений, показанных до нажатия кнопки "Пропустить несколько поколений"
        self.__colors = colors # Список возможных цветов индивидов

        # Создаем экземпляр задачи
        self.__oop = OvercomingObstaclesProblem(self.root, self.canvas, self.rows, self.columns, self.h, self.space, self.__x, self.__y)

        # Создаем экземпляр класса Toolbox, для создания операторов генетического алгоритма
        self.__toolbox = base.Toolbox()

        # Создаем оператор случайно генерирующий число от 1 до 4
        self.__toolbox.register("direction", random.randint, 1, 4)

        # Определяем стратегию приспособления
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

        # Создаем класс индивидуумов на базе класса list
        creator.create("Individual", list, fitness=creator.FitnessMin)

        # Создаемм оператор individualCreator который создает экземляр класса Individual
        self.__toolbox.register("individualCreator", tools.initRepeat, creator.Individual, self.__toolbox.direction,
                              len(self.space))

        # Создаем оператор populationCreator который генерирует список индивидуумов
        self.__toolbox.register("populationCreator", tools.initRepeat, list, self.__toolbox.individualCreator)

        self.__toolbox.register("evaluate", self.cost)

        self.__toolbox.register("select", tools.selTournament, tournsize=2)
        self.__toolbox.register("crossover", tools.cxUniformPartialyMatched, indpb=2.0 / len(self.space))
        self.__toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0 / len(self.space))

    # Геттеры и сеттеры

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
    def population_size(self):
        return self.__population_size

    @population_size.setter
    def population_size(self, value):
        self.__population_size= value

    @property
    def p_crossover(self):
        return self.__p_crossover

    @p_crossover.setter
    def p_crossover(self, value):
        self.__p_crossover = value

    @property
    def p_mutation(self):
        return self.__p_mutation

    @p_mutation.setter
    def p_mutation(self, value):
        self.__p_mutation = value

    @property
    def max_generations(self):
        return self.__max_generations

    @max_generations.setter
    def max_generations(self, value):
        self.__max_generations = value

    @property
    def generation_counter(self):
        return self.__generation_counter

    @generation_counter.setter
    def generation_counter(self, value):
        self.__generation_counter = value

    @property
    def generation_label(self):
        return self.__generation_label

    @generation_label.setter
    def generation_label(self, value):
        self.__generation_label = value

    @property
    def continuous(self):
        return self.__continuous

    @continuous.setter
    def continuous(self, value):
        self.__continuous = value

    @property
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, value):
        self.__colors = value

    @property
    def oop(self):
        return self.__oop

    @oop.setter
    def oop(self, value):
        self.__oop = value

    @property
    def toolbox(self):
        return self.__toolbox

    @toolbox.setter
    def toolbox(self, value):
        self.__toolbox = value

    # Метод, отвечающий за пропуск некоторого числа поколений
    def skip(self):
        self.__continuous = 0 # Обнуляем переменную CONTINUOUS

    # Метод, вычисляющий значения целевой функции
    def cost(self, route):
        return self.__oop.cost(route),

    # Метод, отвечающий за анимацию движения индивидов. В качестве параметров принимает популяцию и список индивидуумов
    def animation(self, population, individuals_list):
        route = [0 for i in range(self.__population_size)] # Список, в котором будет недекодированный путь (саму хромосому)
        complete = 0 # Число индивидуумов добравшихся до цели
        i = 0  # Инициализируем переменную внешнего цикла while
        # Пока до цели добралось меньше двух индивидуумов и число непрерывно показываемых поколений не меньше трех, выполняется цикл
        while i < len(self.space) and complete < 2 and self.__continuous >= 3:
            j = 0 # Обнуляем j
            # Пока мы не прошлись по всем индивидуумам и число добравшихся меньше двух, выполняется внутренний цикл
            while j < len(individuals_list) and complete < 2:
                # Перемещаем j-го индивидуума
                route[j] = individuals_list[j].move(population[j][i])
                # Если он добрался до цели, то увеличиваем complete
                if individuals_list[j].complete == True:
                    complete += 1
                j += 1 # Увеличиваем j

            # После выполнения внутреннего цикла while выполняется анимация движения всех индивидов в один момент времени, с частотой 30 кадров в секунду
            for k in range(30):
                for l in range(self.__population_size):
                    if route[l] == 1:
                        self.canvas.move(individuals_list[l].image, 0, -self.h / 30)
                    elif route[l] == 2:
                        self.canvas.move(individuals_list[l].image, 0, self.h / 30)
                    elif route[l] == 3:
                        self.canvas.move(individuals_list[l].image, -self.h / 30, 0)
                    elif route[l] == 4:
                        self.canvas.move(individuals_list[l].image, self.h / 30, 0)
                time.sleep(0.01) # Пауза в 0.01 секунды
                self.root.update() # Обновление окна
            i += 1 # Увеличиваем i (переменную внешнего цикла while)

        # После выполнения всего цикла, удаляем иконки индивидуумов
        for i in range(self.__population_size):
            self.canvas.delete(individuals_list[i].image)

    # Метод, выполняющий основной цикл генетического алгоритма
    def mainLoop(self):
        individuals_list = [] # Список индивидуумов
        population = self.__toolbox.populationCreator(n=self.__population_size)
        self.__continuous = 3

        # С помощью функции map, применим метод evaluate к каждому индивидууму популяции
        fitness_values = list(map(self.__toolbox.evaluate, population))
        # с помощью функции zip, сопоставим каждого индивидуума с его значением приспособленности
        for individual, fitness_value in zip(population, fitness_values):
            individual.fitness.values = fitness_value

        # Так как в нашем случае имеет место приспособляемость всего
        # с одной целью, то извлекаем первое значение из каждого кортежа приспособленности для сбора статистики
        fitness_values = [individual.fitness.values[0] for individual in population]

        # Начинаем главный цикл алгоритма. Условия остановки:
        # 1) достигнуто максимальное число поколений
        while self.__generation_counter < self.__max_generations:
            self.__generation_counter += 1 # Увеличиваем счетчик поколений

            # Заполняем список индивидуумов
            for i in range(self.__population_size):
                individuals_list.append(Individual(self.root, self.canvas, self.rows, self.columns, self.h, self.space, random.choice(self.__colors), self.__x, self.__y))

            # Применяем оператор отбора
            offspring = self.__toolbox.select(population, len(population))
            """
            отобранные индивидуумы, которые находятся в  списке offspring, клонируются, чтобы можно было применить к ним
            следующие генетические операторы, не затрагивая исходную популяцию.
            Несмотря на имя offspring, это пока еще клоны индивидуумов из
            предыдущего поколения, и к ним еще только предстоит применить оператор кроссинговера для создания потомков.
            """
            offspring = list(map(self.__toolbox.clone, offspring))
            """
            Следующий генетический оператор – кроссинговер. Ранее мы определили его в  атрибуте toolbox.crossover как псевдоним одноточечного
            кроссинговера. С помощью среза объеденим в  пары каждый элемент списка offspring
            с  четным индексом со следующим за ним элементом с  нечетным
            индексом. Затем с помощью функции random() мы «подбросим монету» с вероятностью, заданной константой P_CROSSOVER, и тем самым
            решим, применять к паре индивидуумов скрещивание или оставить
            их как есть. И наконец, удалим значения приспособленности потомков, потому что они были модифицированы и старые значения уже
            не актуальны.
            """
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.__p_crossover:
                    self.__toolbox.crossover(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            """
            Последний генетический оператор – мутация, ранее мы определили
            его в атрибуте toolbox.mutate как псевдоним инвертирования бита. Мы должны обойти всех потомков и применить оператор мутации 
            с вероятностью P_MUTATION. Если индивидуум подвергся мутации, то нужно удалить значение его приспособленности (если оно существует), 
            поскольку оно могло быть перенесено из предыдущего поколения, а после мутации уже не актуально.
            """
            for mutant in offspring:
                if random.random() < self.__p_mutation:
                    self.__toolbox.mutate(mutant)
                    del mutant.fitness.values
            """
            Те индивидуумы, к которым не применялось ни скрещивание, ни мутация, остались неизменными, поэтому их приспособленности, вычисленные в предыдущем 
            поколении, не нужно заново пересчитывать. В  остальных индивидуумах значение приспособленности будет пустым. Мы находим этих индивидуумов, 
            проверяя свойство valid класс Fitness, после чего вычисляем новое значение приспособленности так же, как делали это ранее.
            """
            fresh_individuals = [ind for ind in offspring if not ind.fitness.valid]
            fresh_fitness_values = list(map(self.__toolbox.evaluate, fresh_individuals))

            for individual, fitness_value in zip(fresh_individuals, fresh_fitness_values):
                individual.fitness.values = fitness_value

            # После того как все генетические операторы применены, нужно заменить старую популяцию новой
            population[:] = offspring
            """
            Прежде чем переходить к  следующей итерации, учтем в статистике
            текущие значения приспособленности. Поскольку приспособленность
            представлена кортежем (из одного элемента), необходимо указать индекс [0]
            """
            fitness_values = [individual.fitness.values[0] for individual in population]

            self.animation(population, individuals_list) # Анимируем движение индивидуумов
            self.__continuous += 1 # Увеличиваем число непрерывно показанных поколений

            self.__generation_label["text"] = str(self.__generation_counter) # Изменяем показываемый номер поколения
            individuals_list = [] # Делаем список индивидуумов пустым, чтобы заполнить его на следующей итерации цикла