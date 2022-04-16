import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import colorchooser, messagebox

from dda import DDA
from brezenhem import *
from vu import VU
from draw import *
from config import *

root = tk.Tk()
root.title("КГ Лабораторная работа 3")
root["bg"] = MAIN_COLOUR

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(height=False, width=False)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
def clearScreen():
    canvasFiled.delete("all")
    drawAxes()


def drawAxes():
    color = 'gray'
    canvasFiled.create_line(0, 3, CANVAS_WIDTH, 3, width=1, fill='light gray', arrow=tk.LAST)
    canvasFiled.create_line(3, 0, 3, CANVAS_HEIGHT, width=1, fill='light gray', arrow=tk.LAST)
    for i in range(50, int(CANVAS_WIDTH), 50):
        canvasFiled.create_text(i, 15, text=str(abs(i)), fill=color)
        canvasFiled.create_line(i, 0, i, 5, fill=color)

    for i in range(50, int(CANVAS_HEIGHT), 50):
        canvasFiled.create_text(20, i, text=str(abs(i)), fill=color)
        canvasFiled.create_line(0, i, 5, i, fill=color)


def drawLine():

    algorithm = algorithmsRB.get()
    xStart = xsEntry.get()
    yStart = ysEntry.get()
    xEnd = xeEntry.get()
    yEnd = yeEntry.get()

    if not xStart or not yStart:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты начала отрезка!')
    elif not xEnd or not yEnd:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты конца отрезка!')
    else:
        try:
            xStart, yStart = float(xStart), float(yStart)
            xEnd, yEnd = float(xEnd), float(yEnd)
        except all:
            messagebox.showwarning('Ошибка ввода',
                                   'Координаты заданы неверно!')
        if algorithm == 0:
            drawLineBy_algorithm(canvasFiled, DDA(xStart, yStart, xEnd, yEnd, colour=LINE_COLOUR))
        elif algorithm == 1:
            drawLineBy_algorithm(canvasFiled, BrezenhemFloat(xStart, yStart, xEnd, yEnd, colour=LINE_COLOUR))
        elif algorithm == 2:
            drawLineBy_algorithm(canvasFiled, BrezenhemInteger(xStart, yStart, xEnd, yEnd, colour=LINE_COLOUR))
        elif algorithm == 3:
            drawLineBy_algorithm(canvasFiled, BrezenhemSmooth(canvasFiled, xStart, yStart, xEnd, yEnd, LINE_COLOUR))
        elif algorithm == 4:
            drawLineBy_algorithm(canvasFiled, VU(canvasFiled, xStart, yStart, xEnd, yEnd, fill=LINE_COLOUR))
        elif algorithm == 5:
            drawLineBy_StandartAlgorithm(canvasFiled, xStart, yStart, xEnd, yEnd, colour=LINE_COLOUR)


def drawSpecter():
    algorithm = algorithmsRB.get()
    xStart = xsEntry.get()
    yStart = ysEntry.get()
    xEnd = xeEntry.get()
    yEnd = yeEntry.get()
    angle = angleEntry.get()

    if not xStart or not yStart:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты начала отрезка!')
    elif not xEnd or not yEnd:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты конца отрезка!')
    else:
        try:
            xStart, yStart = float(xStart), float(yStart)
            xEnd, yEnd = float(xEnd), float(yEnd)
            angle = float(angle)
        except all:
            messagebox.showwarning('Ошибка ввода',
                                   'Координаты заданы неверно!')

        if algorithm == 0:
            drawSpecterBy_Method(canvasFiled, DDA,
                                 xStart, yStart,
                                 xEnd, yEnd, angle,
                                 LINE_COLOUR)
        elif algorithm == 1:
            drawSpecterBy_Method(canvasFiled, BrezenhemFloat,
                                 xStart, yStart,
                                 xEnd, yEnd, angle,
                                 LINE_COLOUR)
        elif algorithm == 2:
            drawSpecterBy_Method(canvasFiled, BrezenhemInteger,
                                 xStart, yStart,
                                 xEnd, yEnd, angle,
                                 LINE_COLOUR)
        elif algorithm == 3:
            drawSpecterBy_Method(canvasFiled, BrezenhemSmooth,
                                 xStart, yStart,
                                 xEnd, yEnd, angle,
                                 LINE_COLOUR, intensive=True)
        elif algorithm == 4:
            drawSpecterBy_Method(canvasFiled, VU,
                                 xStart, yStart,
                                 xEnd, yEnd, angle,
                                 LINE_COLOUR, intensive=True)
        elif algorithm == 5:
            drawSpecterBy_StardartMethod(canvasFiled, xStart, yStart, xEnd, yEnd, angle, LINE_COLOUR)


def timeInput(mode):
    try:
        length = int(lengthEntry.get())

        if length <= 0:
            messagebox.showwarning('Ошибка ввода',
                                       'Длина для измерений должна быть больше нуля!')
        else:
            if mode == 1:
                time_bar(length)
            else:
                step_bar(length)
    except all:
        messagebox.showwarning('Ошибка ввода',
                               'Длина для измерений задана неверно!')


def close_plt():
    plt.figure("Исследование времени работы алгоритмов построения.",)
    plt.close()
    plt.figure("Исследование ступенчатости алгоритмов построение.")
    plt.close()


# гистограмма времени
def time_bar(length):
    close_plt()

    plt.figure("Исследование времени работы алгоритмов построения.", figsize=(9, 7))
    times = list()
    angle = 1
    pb = [375, 200]
    pe = [pb[0] + length, pb[0]]

    times.append(drawSpecterBy_Method(canvasFiled, DDA, pb[0], pb[1], pe[0], pe[1], angle, CANVAS_COLOUR, draw=False))
    times.append(drawSpecterBy_Method(canvasFiled, BrezenhemFloat, pb[0], pb[1], pe[0], pe[1], angle, CANVAS_COLOUR, draw=False))
    times.append(drawSpecterBy_Method(canvasFiled, BrezenhemInteger, pb[0], pb[1], pe[0], pe[1], angle, CANVAS_COLOUR, draw=False))
    times.append(drawSpecterBy_Method(canvasFiled, BrezenhemSmooth, pb[0], pb[1], pe[0], pe[1], angle, CANVAS_COLOUR, draw=False, intensive=True))
    times.append(drawSpecterBy_Method(canvasFiled, VU, pb[0], pb[1], pe[0], pe[1], angle, CANVAS_COLOUR, draw=False, intensive=True))
    for i in range(len(times)):
        times[i] *= 100

    Y = range(len(times))

    L = ('ЦДА', 'Брезенхем с\nдействительными\nкоэффицентами',
         'Брезенхем с\nцелыми\nкоэффицентами', 'Брезенхем с\nс устранением\nступенчатости', 'Ву')
    plt.bar(Y, times, align='center')
    plt.xticks(Y, L)
    plt.ylabel("Cекунды (длина линии " + str(length) + ")")
    plt.show()


def step_bar(length):
    close_plt()

    angle = 0
    step = 2
    pb = [0, 0]
    pe = [pb[0], pb[1] + length]

    angles = []
    DDA_steps = []
    BrezenhemInteger_steps = []
    BrezenhemFloat_steps = []
    BrezenhemSmooth_steps = []
    VU_steps = []

    for j in range(90 // step):
        DDA_steps.append(DDA(pb[0], pb[1], pe[0], pe[1], stepmode=True))
        BrezenhemInteger_steps.append(BrezenhemInteger(pb[0], pb[1], pe[0], pe[1], stepmode=True))
        BrezenhemFloat_steps.append(BrezenhemFloat(pb[0], pb[1], pe[0], pe[1], stepmode=True))
        BrezenhemSmooth_steps.append(BrezenhemSmooth(canvasFiled, pb[0], pb[1], pe[0], pe[1], stepmode=True))
        VU_steps.append(VU(canvasFiled, pb[0], pb[1], pe[0], pe[1], stepmode=True))

        pe[0], pe[1] = turn_point(radians(step), pe[0], pe[1], pb[0], pb[1])
        angles.append(angle)
        angle += step

    plt.figure("Исследование ступенчатости алгоритмов построение.", figsize=(18, 10))

    plt.subplot(2, 3, 1)
    plt.plot(angles, DDA_steps, label="ЦДА")
    plt.plot(angles, BrezenhemInteger_steps, '--', label="Брензенхем с целыми или\nдействительными коэффицентами")
    plt.plot(angles, BrezenhemInteger_steps, '.', label="Брензенхем с устр\nступенчатости")
    plt.plot(angles, VU_steps, '-.', label="By")
    plt.title("Исследование ступенчатости.\n{0} - длина отрезка".format(length))
    plt.xticks(np.arange(91, step=5))
    plt.legend()
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 2)
    plt.title("ЦДА")
    plt.plot(angles, DDA_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 3)
    plt.title("BУ")
    plt.plot(angles, VU_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 4)
    plt.title("Брензенхем с действительными коэффицентами")
    plt.plot(angles, BrezenhemFloat_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 5)
    plt.title("Брензенхем с целыми коэффицентами")
    plt.plot(angles, BrezenhemInteger_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 6)
    plt.title("Брензенхем с устр. ступенчатости")
    plt.plot(angles, BrezenhemSmooth_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.show()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INPUT DATA FRAME


dataFrame = tk.Frame(root)
dataFrame["bg"] = MAIN_FRAME_COLOR

dataFrame.place(x=BORDERS_SPACE, y=BORDERS_SPACE,
                 width=DATA_FRAME_WIGHT,
                 height=DATA_FRAME_HEIGHT)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Кнопки для выбора алгоритма

algorithmsLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="АЛГОРИТМЫ ПОСТРОЕНИЯ",
                     font=("Consolas", 16),
                     fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

algorithmsArr = [("Цифровой дифференциальный анализатор", 0),
                 ("Брензенхем (float)", 1),
                 ("Брензенхем (integer)", 2),
                 ("Брензенхем (c устр. ступенчатости)", 3),
                 ("By", 4),
                 ("Библиотечная функция", 5)]
algorithmsRB = tk.IntVar()

for value in range(len(algorithmsArr)):
    tk.Radiobutton(dataFrame, variable=algorithmsRB, text=algorithmsArr[value][0], value=value, bg="lightblue",
                   indicatoron=False, font=("Consolas", 16), justify=tk.LEFT, highlightbackground="black",
                   ).place(x=10, y=(value + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 2 * BORDERS_SPACE, height=DATA_FRAME_HEIGHT // COLUMNS)

algorithmsLabel .place(x=0, y=0, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ВЫБОР цвета
chooseColourMainLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ВЫБОР ЦВЕТА",
                     font=("Consolas", 16),
                     fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

size = (DATA_FRAME_WIGHT // 1.5) // 8
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Выбор цвета фона

bgColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет фона:",
                     font=("Consolas", 16),
                     fg=MAIN_COLOUR_LABEL_TEXT)


def get_color_bg():
    color_code = colorchooser.askcolor(title="Choose colour background canvas")
    set_bgcolour(color_code[-1])


def set_bgcolour(color):
    global CANVAS_COLOUR
    CANVAS_COLOUR = color
    canvasFiled.configure(bg=CANVAS_COLOUR)


whiteBg = tk.Button(dataFrame, bg="white", activebackground="white",
                    command=lambda: set_bgcolour("white"))
yellowBg = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                     command=lambda: set_bgcolour("yellow"))
orangeBg = tk.Button(dataFrame, bg="orange", activebackground="orange",
                     command=lambda: set_bgcolour("orange"))
redBg = tk.Button(dataFrame, bg="red", activebackground="red",
                  command=lambda: set_bgcolour("red"))
purpleBg = tk.Button(dataFrame, bg="purple", activebackground="purple",
                     command=lambda: set_bgcolour("purple"))
greenBg = tk.Button(dataFrame, bg="green", activebackground="green",
                    command=lambda: set_bgcolour("green"))
darkGreenBg = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                        command=lambda: set_bgcolour("darkgreen"))
lightBlueBg = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                        command=lambda: set_bgcolour("lightblue"))

bgColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать другой цвет фона', font=("Consolas", 14), command=get_color_bg)

chooseColourMainLabel.place(x=0, y=8 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
bgColourLabel.place(x=10, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 3, height=DATA_FRAME_HEIGHT // COLUMNS)
bgColourBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=10 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)


whiteBg.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
yellowBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + size, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
orangeBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 2 * size, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
redBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 3 * size, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
purpleBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 4 * size, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
greenBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 5 * size, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
darkGreenBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 6 * size, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
lightBlueBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 7 * size, y=9 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# выбор цвета линии

lineColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет линии:",
                     font=("Consolas", 16),
                     fg=MAIN_COLOUR_LABEL_TEXT)

lineCurColourTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет линии:",
                     font=("Consolas", 16),
                     fg=MAIN_COLOUR_LABEL_TEXT)

lineCurColourLabel = tk.Label(dataFrame, bg="black")


def get_colour_line():
    color_code = colorchooser.askcolor(title="Choose colour line")
    set_linecolour(color_code[-1])


def set_linecolour(color):
    global LINE_COLOUR
    LINE_COLOUR = color
    lineCurColourLabel.configure(bg=LINE_COLOUR)


whiteLine = tk.Button(dataFrame, bg="white", activebackground="white",
                    command=lambda: set_linecolour("white"))
yellowLine = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                     command=lambda: set_linecolour("yellow"))
orangeLine = tk.Button(dataFrame, bg="orange", activebackground="orange",
                     command=lambda: set_linecolour("orange"))
redLine = tk.Button(dataFrame, bg="red", activebackground="red",
                  command=lambda: set_linecolour("red"))
purpleLine = tk.Button(dataFrame, bg="purple", activebackground="purple",
                     command=lambda: set_linecolour("purple"))
greenLine = tk.Button(dataFrame, bg="green", activebackground="green",
                    command=lambda: set_linecolour("green"))
darkGreenLine = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                        command=lambda: set_linecolour("darkgreen"))
lightBlueLine = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                        command=lambda: set_linecolour("lightblue"))

lineColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать другой цвет линии', font=("Consolas", 14), command=get_colour_line)

lineColourLabel.place(x=5, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 3, height=DATA_FRAME_HEIGHT // COLUMNS)
lineColourBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=12 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourTextLabel.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=13 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourLabel.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE + DATA_FRAME_WIGHT // 2, y=13 * DATA_FRAME_HEIGHT // COLUMNS + 5, width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)

whiteLine.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
yellowLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + size, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
orangeLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 2 * size, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
redLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 3 * size, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
purpleLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 4 * size, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
greenLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 5 * size, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
darkGreenLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 6 * size, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
lightBlueLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 7 * size, y=11 * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение линии

lineMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ ЛИНИИ",
                     font=("Consolas", 16),
                     fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

argumnetsLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Xн         Yн         Xк          Yк",
                     font=("Consolas", 14),
                     fg=MAIN_COLOUR_LABEL_TEXT)

xsEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
ysEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
xeEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
yeEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
drawLineBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить линию", font=("Consolas", 14),
                        command=drawLine)


lineMakeLabel.place(x=0, y=14 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
argumnetsLabel.place(x=0, y=15 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
xsEntry.place(x=0, y=16 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
ysEntry.place(x=DATA_FRAME_WIGHT // 4, y=16 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
xeEntry.place(x=2 * DATA_FRAME_WIGHT // 4, y=16 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
yeEntry.place(x=3 * DATA_FRAME_WIGHT // 4, y=16 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
drawLineBtn.place(x=DATA_FRAME_WIGHT // 2 / 2.5, y=18 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение спектра

lineColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Угол поворота (в градуссах):",
                     font=12,
                     fg=MAIN_COLOUR_LABEL_TEXT)
angleEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
drawSpnBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить спектр", font=("Consolas", 14),
                       command=drawSpecter)

lineColourLabel.place(x=0, y=17 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
angleEntry.place(x=DATA_FRAME_WIGHT // 2, y=17 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
drawSpnBtn.place(x=DATA_FRAME_WIGHT // 2 / 2.5, y=19 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Кнопки сравнения, очистки и справки


def show_info():
    messagebox.showinfo('Информация',
                        'С помощью данной программы можно построить отрезки 6 способами:\n'
                        '1) методом цифрового дифференциального анализатора;\n'
                        '2) методом Брезенхема с действитльными коэфициентами;\n'
                        '3) методом Брезенхема с целыми коэфициентами;\n'
                        '4) методом Брезенхема с устранением ступенчатости;\n'
                        '5) методом Ву;\n'
                        '6) стандартым методом.\n'
                        '\nДля построения отрезка необходимо задать его начало\n'
                        'и конец и выбрать метод построения из списка предложенных.\n'
                        '\nДля построения спектра (пучка отрезков)\n'
                        'необходимо задать начало и конец,\n'
                        'выбрать метод для построения,\n'
                        'а также угол поворота отрезка.\n'
                        '\nДля анализа ступенчатости достаточно нажать на кнопку "Сравнение ступенчатости".\n'
                        'Анализ ступенчатости и времени исполнения приводится\n'
                        'в виде графиков pyplot.\n'
                        'Введите длину отрезка, если хотите сделать анализ программы\n'
                        'при построении отрезков определенной длины.')


lineLengthLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Длина линии:",
                     font=12,
                     fg=MAIN_COLOUR_LABEL_TEXT)
lengthEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")

compareTimenBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Сравнения времени", font=("Consolas", 14),
                            command=lambda: timeInput(1))
compareGradationBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Сравнения ступенчатости", font=("Consolas", 14),
                                command=lambda: timeInput(2))
clearCanvasBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Очистить экран", font=("Consolas", 14), command=clearScreen)
infoBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Справка", font=("Consolas", 14),
                    command=show_info)

lineLengthLabel.place(x=0, y=22 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
lengthEntry .place(x=DATA_FRAME_WIGHT // 4, y=22 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
compareTimenBtn.place(x=20, y=23 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 40, height=DATA_FRAME_HEIGHT // COLUMNS)
compareGradationBtn.place(x=20, y=24 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 40, height=DATA_FRAME_HEIGHT // COLUMNS)
clearCanvasBtn.place(x=20, y=25 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 40, height=DATA_FRAME_HEIGHT // COLUMNS)
infoBtn.place(x=20, y=26 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 40, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CANVAS FILED FOR DRAWING lines and spectres by algorithms
canvasFiled = tk.Canvas(root, bg=CANVAS_COLOUR)
canvasFiled.place(x=WINDOW_WIDTH * DATA_SITUATION + BORDERS_SPACE, y=BORDERS_SPACE, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

angleEntry.insert(0, str(15))
lengthEntry.insert(0, str(100))

xsEntry.insert(0, str(545))
ysEntry.insert(0, str(350))

xeEntry.insert(0, str(695))
yeEntry.insert(0, str(500))

drawAxes()

root.mainloop()