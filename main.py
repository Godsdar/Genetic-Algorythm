from tkinter import *
from tkinter import messagebox as mb
from geneticAlgorithm import GeneticAlgorithm

class Main:
    def __init__(self, width, height, rows, columns, h, x, y, maincolor, font1, font2, foreground, background1, background2):
        self.__width = width
        self.__height = height
        self.rows = rows
        self.columns = columns
        self.h = h
        self.__maincolor = maincolor
        self.__font1 = font1
        self.__font2 = font2
        self.__foreground = foreground
        self.__background1 = background1
        self.__background2 = background2

        self.root = Tk()
        self.root.title("Визуализация генетического алгоритма")

        # Распологаем окно по центру экрана
        self.root.geometry(f"{self.__width}x{self.__height}+{self.root.winfo_screenwidth() // 2 - self.__width // 2}+{self.root.winfo_screenheight() // 2 - self.__height // 2}")

        # Отключаем возможность изменения размеров окна
        self.root.resizable(False, False)

        # Задаем задний фон окна
        self.root["bg"] = self.__maincolor

        # Создаем и размещаем холст на котором будем рисовать поле и объекты
        self.canvas = Canvas(self.root, width=self.h * self.columns, height=self.h * self.rows, bg=self.__maincolor)
        self.canvas.place(x=0, y=50)

        # Отрисовываем поле
        for i in range(self.columns):
            for j in range(self.rows):
                self.canvas.create_rectangle((self.h * i, self.h * j), (self.h * i + self.h, self.h * j + self.h))

        """ 
        Список space будет содержать информацию о расположении объектов на поле.     
        Если элемент списка равен 0, значит клетка с индексом этого элемента пуста.   
        Если элемент списка равен 1, значит на клетка с индексом этого элементаа находится цель.
        Если элемент списка равен -1, значит на клетка с индексом этого элементаа находится препятствие.

        Изначально поле пусто, поэтому список space заполняется нулями
        """

        self.space = [0 for i in range(self.rows * self.columns)]

        self.__x = x
        self.__y = y

        self.__continuous = 0

        self.__population_size = 50
        self.__p_crossover = 0.9
        self.__p_mutation = 0.1
        self.__max_generations = 100

        self.__colors = ["orange", "pink", "red", "blue", "lightblue", "purple", "lightgreen", "yellow", "grey", "brown"]
        # Надпись показывающая номер поколения по мере выполнения цикла
        self.generation_label = Label(self.root, text="1", font=self.__font2, bg=self.__maincolor)
        self.generation_label.place(x=530, y=10)

        self.geneticAlgorithm = GeneticAlgorithm(self.root, self.canvas, self.rows, self.columns, self.h,
                    self.space, self.__x, self.__y, self.__population_size, self.__p_crossover, self.__p_mutation,
                    self.__max_generations, self.generation_label, self.__continuous, self.__colors)

        # Размещаем все нужные кнопки. К кнопке "Старт" привязываем начало выполнения главного цикла программы
        self.start_button = Button(text="Старт", font=self.__font2, fg=self.__foreground, bg=self.__background1,
                              command=self.geneticAlgorithm.mainLoop)
        self.start_button.place(x=440, y=630)

        self.generatiion_label = Label(text="Поколение: ", font=self.__font2, bg=self.__background2)
        self.generatiion_label.place(x=400, y=10)

        # К кнопке skip привязываем метод skip
        self.skip_button = Button(text="Пропустить несколько поколений", font=self.__font2, fg=self.__foreground,
                             bg=self.__background1, command=self.geneticAlgorithm.skip)
        self.skip_button.place(x=50, y=630)

        # Создаем меню
        self.main_menu = Menu(self.root, tearoff=0)
        self.root.config(menu=self.main_menu)

        # Добавляем вкладки меню
        self.help_menu = Menu(self.main_menu, tearoff=0)
        self.help_menu.add_command(label="Справка", command=self.help)
        self.help_menu.add_command(label="О разработчике", command=self.aboutTheDeveloper)

        self.main_menu.add_cascade(label="О программе", menu=self.help_menu)

        self.random_button = Button(self.root, text="Сгенерировать случайное расположение", font=self.__font2,
                                    fg=self.__foreground, bg=self.__background1, command=lambda n=40: self.geneticAlgorithm.oop.generateRandomPosition(n))
        self.random_button.place(x=550, y=630)

    # Геттеры и сеттеры

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def maincolor(self):
        return self.__maincolor

    @maincolor.setter
    def maincolor(self, value):
        self.__maincolor = value

    @property
    def font1(self):
        return self.__font1

    @font1.setter
    def font1(self, value):
        self.__font1 = value

    @property
    def font2(self):
        return self.__font2

    @font2.setter
    def font2(self, value):
        self.__font2 = value

    @property
    def foreground(self):
        return self.__foreground

    @foreground.setter
    def foreground(self, value):
        self.__foreground = value

    @property
    def background1(self):
        return self.__background1

    @background1.setter
    def background1(self, value):
        self.__background1 = value

    @property
    def background2(self):
        return self.__background2

    @background2.setter
    def background2(self, value):
        self.__background2 = value

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
        self.__population_size = value

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
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, value):
        self.__colors = value

    # Эта функция выведет сообщение-справку при нажатии на вкладку "Справка"
    def help(self):
        text = (
            "    Работа программы проста. По нажатию на кнопку «Сгенерировать случайное расположение», на игровом поле генерируются препятствия (красные квадраты) и цель (синий квадрат). Нажав на кнопку «Старт» пользователь начнет наблюдать начало работы генетического алгоритма. Особи начнут двигаться к цели, натыкаясь на минимальное число препятствий. Если сходимость алгоритма происходит слишком медленно, то нажав на кнопку «Пропустить несколько поколений», пользователь пропустит показ движения трех поколений.")

        # Выводим информацию с помощью метода showinfo
        mb.showinfo("Справка", text)

    # Эта функция выведет сообщение при нажатии на вкладку "О разработчике"
    def aboutTheDeveloper(self):
        text = (
            "    Меня зовут Ильдар и я живу программированием! Начал еще в школе. Интересовался математикой, алгоритмами и структурами данных. Реализовывал вручную стек, очередь, связный список, бинарное дерево. Занимался созданием шахматной программы с нуля на С++. Изучал технологии компиляции, и архитектуру ЭВМ. Это моя первая программа с графическим интерфейсом, и это было потрясающе! Данный курсовой проект проект принёс мне море удовольствия! И да, придет день, когда я стану лучшим программистом в мире! \n\nСтудент ФДО ТУСУР \nФИО: Попов Ильдар Станиславович \nНомер группы: з-422П8-1")
        mb.showinfo("О разработчике", text)

if __name__ == "__main__":
    WIDTH = 1000
    HEIGHT = 700

    # Размер одной клетки
    H = 50
    X = 8
    Y = 6

    # Число строк и столбцов игрового поля
    ROWS = 11
    COLUMNS = 20

    MAINCOLOR = "white"
    FONT1 = "Verdana 10"
    FONT2 = "Verdana 14"
    FOREGROUND = "yellow"
    BACKGROUND1 = "red"
    BACKGROUND2 = "white"

    m = Main(WIDTH, HEIGHT, ROWS, COLUMNS, H, X, Y, MAINCOLOR, FONT1, FONT2, FOREGROUND, BACKGROUND1, BACKGROUND2)
    m.root.mainloop()