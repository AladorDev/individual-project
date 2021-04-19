from tkinter import * #Для создания приложения tk
from tkinter import messagebox # Импорт компонента для сообщение о закрытие окна, о выходе из игры
import time #Импорт функции time
import random # Импорт модуля random

tk = Tk()   #Создаем объект
app_running = True  #Переменная, которая отслеживает, что наша переменная работает

size_canvas_x = 800 #Переменные размеров окна в пикселях
size_canvas_y = 800
s_x = s_y = 10  #  Количество ячеек по оси X  и оси Y в игровом поле
step_x = size_canvas_x // s_x  # шаг отрисовки линий по горизонтали
step_y = size_canvas_y // s_y  # шаг отрисовки линий по вертикали
size_canvas_x = step_x * s_x # чтобы убрать остаток по делению из расчетов, пересчитываем размер игровой области (откидываем дробную часть)
size_canvas_y = step_y * s_y # - // -

txt_len_middle = "* Игрок vs Компьютер" # Переменная для расчета длины меню. За основу берется строка * Игрок vs Компьютер
size_font_x = 10 # Ширина буквы в пикселях
len_txt_x = len(txt_len_middle)*size_font_x # Длина фразы "* Игрок vs Компьютер" по х
print(len_txt_x)
delta_menu_x = len_txt_x // step_x + 1 # Смещение
menu_x = step_x * delta_menu_x  # 250  Дополнительная область для кнопок

menu_y = 40 # Меню по у. Значение в пикселях
ships = s_x // 2  # определяем максимальное кол-во кораблей
ship_len1 = s_x // 5  # длина первого типа корабля
ship_len2 = s_x // 3  # длина второго типа корабля
ship_len3 = s_x // 2  # длина третьего типа корабля
enemy_ships1 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)] # Создаем список кораблей игрока 1
enemy_ships2 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)] # Создаем список кораблей игрока 2
list_ids = []  # список объектов canvas

# points1 и 2  - списки, куда мы кликнули мышкой на поле игрока1 и игрока 2
points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
points2 = [[-1 for i in range(s_x)] for i in range(s_y)]

# boom - список попаданий по кораблям противника
boom = [[0 for i in range(s_x)] for i in range(s_y)]

# ships_list - список кораблей игрока 1 и игрока 2
ships_list = []

# hod_igrovomu_polu_1 - если Истина - то ходит игрок №2, иначе ходит игрок №1
hod_igrovomu_polu_1 = False # Переменная, обозначающая, по какому полю бьют

# computer_vs_human - если Истина - то играем против компьютера
computer_vs_human = False # Переменная Компьютер против человека. По умолчанию будет Человек против человека.
if computer_vs_human: # Если играем с компьютером, то
    add_to_label = " (Компьютер)"
    add_to_label2 = " (прицеливается)"
    hod_igrovomu_polu_1 = False # Начинает человек
else:
    add_to_label = ""
    add_to_label2 = ""
    hod_igrovomu_polu_1 = False

# print(enemy_ships1)

def on_closing(): #Функция закрытия окна
    global app_running #Делаем переменную глобальной
    if messagebox.askokcancel("Завершение игры", "Неужели вы хотите покинуть игру?"): #Если мы выходим из игры
        app_running = False #Переменная получает значение False, чтобы приложение закрылось
        tk.destroy() #Объект tk уничтожается

# * * *  Эта часть относится к импорту в строке 1 from tkinter import *  Здесь задаем параметры нашего приложения
tk.protocol("WM_DELETE_WINDOW", on_closing)  #Вызов функции on_closing на событие WM_DELETE_WINDOW
tk.title("Морской бой") #Название игры
tk.resizable(0, 0) #Возможность изменять (растягивать) окно. При 0,0 не растягивается.
tk.wm_attributes("-topmost", 1) #Окно поверх всех окон
canvas = Canvas(tk, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0,
                highlightthickness=0) # Задаем параметры рабочей области нашего приложения
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="lightyellow") #Создаем прямоугольник светло-желтого цвета (можно менять значение fill)
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                        fill="lightyellow")
canvas.pack() #Запакуем поле приложения
tk.update() #Обновление tk
# * * *

def draw_table(offset_x=0): #Функция, создающая клеточное поле
    for i in range(0, s_x + 1): #итерируемся по шагу по х
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y) # вертикальные линии
    for i in range(0, s_y + 1): #итерируемся по шагу по y
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i) # 0 и size_canvas_x - горизонтальные линии


draw_table() #Вызываем функцию draw_table
draw_table(size_canvas_x + menu_x) # Чтобы сдвинуться правее на размер игровой области + меню

t0 = Label(tk, text="Игрок №1", font=("Helvetica", 16)) # Выводим под первым полем имя первого игрока,
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3) # а здесь координаты, где будет надпись
t1 = Label(tk, text="Игрок №2"+add_to_label, font=("Helvetica", 16)) # Выводим под первым полем имя второго игрока,
t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3) # а здесь координаты, где будет надпись

t0.configure(bg="red") # Фон надписи игрока, который будет стрелять
t0.configure(bg="#f0f0f0") # Фон надписи игрока, который не стреляет

t3 = Label(tk, text="@@@@@@@", font=("Helvetica", 16))
t3.place(x=size_canvas_x + menu_x//2 - t3.winfo_reqwidth() // 2, y= size_canvas_y)


def change_rb(): # Функция смены режима игры
    global computer_vs_human, add_to_label, add_to_label2 # Делаем переменные глобальными, чтобы использовать их в других частях программы
    print(rb_var.get())
    if rb_var.get(): # Если играем против компьютера, то переменным присваеиваем следующие значения
        computer_vs_human = True
        add_to_label = " (Компьютер)"
        add_to_label2 = " (прицеливается)"
    else: # Если играем против человека, то эти переменные обнуляются
        computer_vs_human = False
        add_to_label = ""
        add_to_label2 = ""

rb_var = BooleanVar() # Создаем кнопку переключения между режимами с человеком и компьютером.
rb1 = Radiobutton(tk, text="Игрок vs Компьютер", variable = rb_var, value=1, command=change_rb)
rb2 = Radiobutton(tk, text="Игрок vs Игрок", variable = rb_var, value=0, command=change_rb)
rb1.place(x=size_canvas_x + menu_x // 2 - rb1.winfo_reqwidth() // 2, y=140)
rb2.place(x=size_canvas_x + menu_x // 2 - rb2.winfo_reqwidth() // 2, y=160)
if computer_vs_human:
    rb1.select()


def mark_igrok(igrok_mark_1): # Функция, маркирующая ходящего игрока
    if igrok_mark_1:
        t0.configure(bg="yellow")
        t0.configure(text="Море Игрока №1"+add_to_label2)
        t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t1.configure(text="Море Игрока №2" + add_to_label)
        t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t1.configure(bg="#f0f0f0")
        t3.configure(text="Ход Игрока №2"+add_to_label) # Выводит надпись, что ходит Игрок 2
        t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y) # Место вывода надписи
    else:
        t1.configure(bg="yellow")
        t0.configure(bg="#f0f0f0")
        t0.configure(text="Море Игрока №1")
        t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t1.configure(text="Море Игрока №2" + add_to_label)
        t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t3.configure(text="Ход Игрока №1") # Выводит надпись, что ходит Игрок 1
        t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y) # Место вывода надписи
mark_igrok(hod_igrovomu_polu_1)


def button_show_enemy1(): # Функция вывода кораблей, когда мы кликаем на кнопку Увидеть корабли Игрока 1
    for i in range(0, s_x): # Пишем двойной цикл, чтобы пройти по нашему списку enemy_ships1
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0: # если больше 0, то в переменную id мы сохраняем то, что нарисуем на экране
                color = "red"
                if points1[j][i] != -1: # Если по этим координатам значение не равняется -1, то color станет другого цвета
                    color = "green"
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color) # координаты с заливкой
                list_ids.append(_id) # Сохраняем в список id отображаемых элементов на canvas. Теперь при нажатии на кнопку мы увидим вражеские корабли


def button_show_enemy2(): # Функция вывода кораблей, когда мы кликаем на кнопку Увидеть корабли Игрока 2 (Так же как в функции button_show_enemy1)
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                color = "red"
                if points2[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(size_canvas_x + menu_x + i * step_x, j * step_y,
                                              size_canvas_x + menu_x + i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_begin_again(): # Функция, позволяющая начинать игру сначала
    global list_ids # Делаем глобальными следующие переменные (списки)
    global points1, points2
    global boom
    global enemy_ships1, enemy_ships2
    for el in list_ids: # Для каждого элемента в этом списке
        canvas.delete(el) # мы будем удалять его из canvas. Удаляем из canvas все нарисованные корабли
    list_ids = [] # Обнуляем (очищаем) список. Он почистится после того как из canvas  удалятся все элементы, которые имеют id , сохранненые в списке list_ids
    generate_ships_list() # Вызывается функция сгенерировать корабли противника вновь
    # print(ships_list)
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(s_x)] for i in range(s_y)] # При нажатии кнопки Начать заново обнуляется список points1 наших кликов
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)] # При нажатии кнопки Начать заново обнуляется список points2 наших кликов
    boom = [[0 for i in range(s_x)] for i in range(s_y)] # При нажатии кнопки Начать заново обнуляется список bool


b0 = Button(tk, text="Увидеть корабли \n Игрока №1", command=button_show_enemy1) #Создание кнопки Увидеть корабли игрока. После command укажем функцию, которая сработает после нажатии этой кнопки
b0.place(x=size_canvas_x + menu_x // 2 - b0.winfo_reqwidth() // 2, y=10) #Расположение кнопки на экране

b1 = Button(tk, text="Увидеть корабли \n Игрока №2", command=button_show_enemy2) #Создание кнопки Увидеть корабли противника
b1.place(x=size_canvas_x + menu_x // 2 - b1.winfo_reqwidth() // 2, y=60) #Расположение кнопки на экране

b2 = Button(tk, text="Начать заново!", command=button_begin_again) #Создание кнопки Начать заново
b2.place(x=size_canvas_x + menu_x // 2 - b2.winfo_reqwidth() // 2, y=110) #Расположение кнопки на экране


def draw_point(x, y): #  Функция, рисующая крестик, если в клетке корабль противника, и кружок (нолик), если в клетке пусто
    # print(enemy_ships1[y][x])
    if enemy_ships1[y][x] == 0: # Если равен 0, то рисуем в клетке кружок
        color = "blue" # Цвет кружка
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)  # id кружка
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3, x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white") # id маленького кружка внутри большого
        list_ids.append(id1) # Для очищения списка после нажатия клавиши Начать заново
        list_ids.append(id2)
    if enemy_ships1[y][x] > 0: # Если больше нуля, то рисуем в клетке крестик
        color = "blue"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,   # id крестика (1-го прямоугольника)
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)   # id крестика (2-го прямоугольника)
        list_ids.append(id1) # Для очищения списка после нажатия клавиши Начать заново
        list_ids.append(id2)


def draw_point2(x, y, offset_x=size_canvas_x + menu_x): #  Функция, рисующая крестик, если в клетке корабль противника, и кружок (нолик), если в клетке пусто на втором поле для второго игрока
    # print(enemy_ships1[y][x])
    if enemy_ships2[y][x] == 0:
        color = "black"
        id1 = canvas.create_oval(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x, y * step_y + step_y,
                                 fill=color)
        id2 = canvas.create_oval(offset_x + x * step_x + step_x // 3, y * step_y + step_y // 3,
                                 offset_x + x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships2[y][x] > 0:
        color = "black"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 10,
                                      offset_x + x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      offset_x + x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y,
                                      fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def check_winner(x, y): # Функция проверки на победителя. Эта функция не только проверяет на победу, но и обновляет список boom
    win = False # Создаем переменную win со значением False. Мы не победили.
    if enemy_ships1[y][x] > 0: # Если у нас по координатам, куда мы выстрелили, находится не ноль, то
        boom[y][x] = enemy_ships1[y][x] # в этот список записываем тоже самое число. В этом списке записываем наши выстрелы (куда мы кликнули и там был корабль врага)
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))  # Сумма всех элементов многомерного списка enemy_ships1
    sum_boom = sum(sum(i) for i in zip(*boom)) # Сумма всех элементов многомерного списка boom
    # print(sum_enemy_ships1, sum_boom)
    if sum_enemy_ships1 == sum_boom: # Если сумма этих элементов (наших врагов в обоих списках) совпадает, то
        win = True # переменная win принимает значение True, если не совпадает, то False
    return win


def check_winner2(): # 2 способ проверки: пройдя по многомерному списку и смотрим везде ли мы кликнули по нашим элементам (всем клеткам кораблей противника)
    win = True       # если да, то Победа
    for i in range(0, s_x): # Через два цикла проходим по списку вражеских кораблей
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0: #  Если по координатам, где мы кликаем мышкой, находится вражеский корабль
                if points1[j][i] == -1: # (значение отличное от -1), то мы побеждаем
                    win = False
    # print(win)
    return win


def check_winner2_igrok_2(): # Для игрока номер 2
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    # print(win)
    return win


def hod_computer(): # Функция, реализующая ходы компьютера
    global points1, points2, hod_igrovomu_polu_1 # Делаем переменные глобальными
    tk.update() # Обновление tk
    time.sleep(1) # Задержка из модуля Time - 1c. Можно поменять на другое значение.
    hod_igrovomu_polu_1 = False
    ip_x = random.randint(0, s_x-1)
    ip_y = random.randint(0, s_y-1)
    #print(ip_x, ip_y)
    while not points1[ip_y][ip_x] == -1: # Пока значение не -1, определяем координаты заново
        ip_x = random.randint(0, s_x-1)
        ip_y = random.randint(0, s_y-1)
    points1[ip_y][ip_x] = 7 # 7 -кой мы обозначаем компьютер. При генерации случайных чисел компьютер не будет стрелять в одно место дважды.
    draw_point(ip_x, ip_y)
    if check_winner2(): # Проверка на победу (человек или компьютер).
        winner = "Победа Игрока №2"+add_to_label
        winner_add = "Корабли Игрока №1 уничтожены."
        print(winner, winner_add)
        points1 = [[10 for i in range(s_x)] for i in range(s_y)]
        points2 = [[10 for i in range(s_x)] for i in range(s_y)]
        id1 = canvas.create_rectangle(step_x * 3, step_y * 3, size_canvas_x + menu_x + size_canvas_x - step_x * 3,
                                      size_canvas_y - step_y, fill="blue")
        list_ids.append(id1)
        id2 = canvas.create_rectangle(step_x * 3 + step_x // 2, step_y * 3 + step_y // 2,
                                      size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x // 2,
                                      size_canvas_y - step_y - step_y // 2, fill="yellow")
        list_ids.append(id2)
        id3 = canvas.create_text(step_x * 10, step_y * 5, text=winner, font=("Arial", 50), justify=CENTER)
        id4 = canvas.create_text(step_x * 10, step_y * 6, text=winner_add, font=("Arial", 25), justify=CENTER)
        list_ids.append(id3)
        list_ids.append(id4)


def add_to_all(event): #Функция, вызываемая при нажатии кнопки мыши. Позволяет определить координаты,  куда мы кликнули мышкой
    global points1, points2, hod_igrovomu_polu_1
    _type = 0  # ЛКМ в этой переменной хранится нажатие, которое мы произвели
    if event.num == 3:
        _type = 1  # ПКМ  Переменная хранит 0, если нажали ЛКМ и 1, если нажали ПКМ. То есть здесь определяется тип нажатия.
    #print(_type)
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()  # Координаты мышки. Для получения координат внутри окна. Это координаты относительно нашего игрового поля
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    #print(mouse_x, mouse_y)
    ip_x = mouse_x // step_x # Определяем точные координаты наших ячеек. Пременная Игровое поле х (ip_x). Делим на step_x, чтобы определить ту часть, в которую мы кликнули по экрану.
    ip_y = mouse_y // step_y # Таким образом получаем целочисленные координаты каждой ячейки поля. Верхняя левая ячейка имеет координаты 0, 0, следующая 1,0 и т. д.
    # print(ip_x, ip_y, "_type:", _type)

    # первое игровое поле
    if ip_x < s_x and ip_y < s_y and hod_igrovomu_polu_1: # Проверяем, что наш клик находится в пределах первого поля
        if points1[ip_y][ip_x] == -1: # Если эти координаты равны -1 , то отрисовываем точку. Это проверка на случай, если по этим координатам уже кликали!
            points1[ip_y][ip_x] = _type # то в эти координаты игоровго поля мы записываем тип нажего нажатия
            hod_igrovomu_polu_1 = False # Передаем ход другому игроку
            draw_point(ip_x, ip_y) # Рисуем в этих координатах (игровое поле х и игровое поле у) наш элемент (нолик или крестик)
            # if check_winner(ip_x, ip_y):
            if check_winner2(): # Здесь вызывается функция check_winner2 Происходит проверка на победителя
                hod_igrovomu_polu_1 = True
                winner = "Победа Игрока №2"
                winner_add = "Корабли Игрока №1 уничтожены."
                print(winner, winner_add)
                points1 = [[10 for i in range(s_x)] for i in range(s_y)] # Заполняем наши списки кликов десятками, чтобы нельзя было больше кликать
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
                id1 = canvas.create_rectangle(step_x*3, size_canvas_y // 2, size_canvas_x + menu_x + size_canvas_x-step_x*3, size_canvas_y // 2+step_y+step_y // 2 + 50 + 25 + step_y // 2, fill="blue")
                list_ids.append(id1)
                id2 = canvas.create_rectangle(step_x * 3+step_x//2, size_canvas_y // 2 +step_y//2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x//2,
                                              size_canvas_y // 2+step_y+step_y // 2 + 50 + 25 + step_y // 2 - step_y//2, fill="yellow")
                list_ids.append(id2)
                id3 = canvas.create_text(size_canvas_x+menu_x//2, size_canvas_y // 2+step_y+step_y // 2, text=winner, font=("Arial", 50), justify=CENTER)
                id4 = canvas.create_text(size_canvas_x+menu_x//2, size_canvas_y // 2+step_y+step_y // 2 + 50, text=winner_add, font=("Arial", 25), justify=CENTER)
                list_ids.append(id3)
                list_ids.append(id4)

        # print(len(list_ids))

    # второе игровое поле
    if ip_x >= s_x + delta_menu_x and ip_x <= s_x + s_x + delta_menu_x and ip_y < s_y and not hod_igrovomu_polu_1:
        # print("ok")
        if points2[ip_y][ip_x - s_x - delta_menu_x] == -1:
            points2[ip_y][ip_x - s_x - delta_menu_x] = _type
            hod_igrovomu_polu_1 = True
            draw_point2(ip_x - s_x - delta_menu_x, ip_y)
            # if check_winner(ip_x, ip_y):
            if check_winner2_igrok_2():
                hod_igrovomu_polu_1 = False
                winner = "Победа Игрока №1"
                winner_add = "Корабли Игрока №2 уничтожены."
                print(winner, winner_add)
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
                id1 = canvas.create_rectangle(step_x * 3, size_canvas_y // 2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3,
                                              size_canvas_y // 2 + step_y + step_y // 2 + 50 + 25 + step_y // 2,
                                              fill="blue")
                list_ids.append(id1)
                id2 = canvas.create_rectangle(step_x * 3 + step_x // 2, size_canvas_y // 2 + step_y // 2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x // 2,
                                              size_canvas_y // 2 + step_y + step_y // 2 + 50 + 25 + step_y // 2 - step_y // 2,
                                              fill="yellow")
                list_ids.append(id2)
                id3 = canvas.create_text(size_canvas_x + menu_x // 2, size_canvas_y // 2 + step_y + step_y // 2,
                                         text=winner, font=("Arial", 50), justify=CENTER)
                id4 = canvas.create_text(size_canvas_x + menu_x // 2, size_canvas_y // 2 + step_y + step_y // 2 + 50,
                                         text=winner_add, font=("Arial", 25), justify=CENTER)
                list_ids.append(id3)
                list_ids.append(id4)
            elif computer_vs_human:
                mark_igrok(hod_igrovomu_polu_1)
                hod_computer() # Вызов функции Ход компьютера
    mark_igrok(hod_igrovomu_polu_1)

# * * * Привязка нажатие кнопок нашим canvas
canvas.bind_all("<Button-1>", add_to_all)  # ЛКМыши какую кнопку нажимаем и какая функция будет срабатывать add_to_all
canvas.bind_all("<Button-3>", add_to_all)  # ПКМыши


def generate_ships_list():
    global ships_list
    ships_list = [] # Создаем пустой список
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3])) # Добваляем в список случайне длины кораблей, которые генерируются с помощью функции random.choice из модуля random
    # print(ships_list)


def generate_enemy_ships(): # Функция, которая будет расставлять (генерировать) корабли врагов на поле в игровой области
    global ships_list # Делаем переменную ships_list глобальной, чтобы работа с ней перенеслась в эту функцию и чтобы не создавалась ее новая копия
    enemy_ships = [] # Обнуляем список

    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0

    # print("sum: ", sum_1_all_ships)

    while sum_1_enemy != sum_1_all_ships: # Цикл пока сумма кораблей противника нерана сумме длин всех кораблей, чтобы корабли не пересекались друг с  другом
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in
                       range(s_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

            primerno_x = random.randrange(0, s_x) # Сюда мы записываем координату расположение нашего корабля по х
            if primerno_x + len > s_x: # Если координата по х с учетом длины корабля превышает количество ячеек поля по х
                primerno_x = primerno_x - len # то мы сдвигаем координату х влево, чтобы корабль поместился

            primerno_y = random.randrange(0, s_y) # Сюда мы записываем координату расположение нашего корабля по у
            if primerno_y + len > s_y: # Если координата по х с учетом длины корабля превышает количество ячеек поля по у
                primerno_y = primerno_y - len # то мы сдвигаем координату у по оси, чтобы корабль поместился

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1: # Если у нас горизонтальное расположение, то мы выполняем код ниже
                if primerno_x + len <= s_x:  # Проверяем, что мы не вышли за границы
                    for j in range(0, len): # Запускаем цикл, который
                        try:  # пытается проверить, что по соседним координатам у нас нет противника
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля, i берем из строки 410 ( for i in range(0, ships): )
                        except Exception: # Если возниктнет исключение, то ничего не делаем
                            pass
            if horizont_vertikal == 2: # Если у нас вертикальное расположение,  то мы выполняем код ниже
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля, i берем из строки 425 (for j in range(0, len): )
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

        # print(sum_1_enemy)
        # print(ships_list)
        # print(enemy_ships)
    return enemy_ships


generate_ships_list()
enemy_ships1 = generate_enemy_ships() # При вызове функции generate_enemy_ships записываем ее значения в переменную для игрока 1
enemy_ships2 = generate_enemy_ships() # При вызове функции generate_enemy_ships записываем ее значения в переменную для игрока 2


while app_running:  #Цикл пока приложение работает
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005) #Задержка из модуля Time