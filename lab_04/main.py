import time
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import colorchooser, messagebox

from config import *
from bresenham import bresenham_circle_octant, bresenham_ellipse
from canonic import canonical_сircle, canonical_ellipse
from parametric import parameter_circle, parameter_ellipse
from midpoint import midpoint_circle, midpoint_ellipse
from draw import set_pixel, draw_pixels

root = tk.Tk()
root.title("КГ Лабораторная работа 4")
root["bg"] = MAIN_COLOUR

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(height=False, width=False)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clearScreen():
    canvasFiled.delete("all")


def standart_oval(canvas, xc, yc, ra, rb, color):
    canvas.create_oval(xc - ra, yc - rb, xc + ra, yc + rb, outline=color)


def spectrumBy_standart(canvas, xc, yc, ra, rb, step, count, colour):
    for e in range(0, count):
        standart_oval(canvas, xc, yc, ra, rb, colour)
        ra += step
        rb += step


def draw_circle():

    xc = xcEntry.get()
    yc = ycEntry.get()
    r = rEntry.get()

    if not xc or not yc:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты центра фигуры!')
    elif not r:
        messagebox.showwarning('Ошибка ввода',
                               'Не задан радиус окружности!')
    else:
        try:
            xc = round(float(xc))
            yc = round(float(yc))
            r = round(float(r))

            value_alg = algorithmsRB.get()

            if value_alg == 0:
                canonical_сircle(xc, yc, r, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 1:
                parameter_circle(xc, yc, r, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 2:
                midpoint_circle(xc, yc, r, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 3:
                bresenham_circle_octant(xc, yc, r, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 4:
                standart_oval(canvasFiled, xc, yc, r, r, LINE_COLOUR)
        except:
            messagebox.showwarning('Ошибка ввода',
                                   'В данных для построения окружности введенно(ы) некорректный(ые) символ(ы)!')


def draw_ellipse():

    xc = xcEntry.get()
    yc = ycEntry.get()
    ra = rxEntry.get()
    rb = ryEntry.get()

    if not xc or not yc:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты центра фигуры!')
    elif not ra or not rb:
        messagebox.showwarning('Ошибка ввода',
                                'Не заданы радиусы эллипса для построения эллипса!')
    else:
        try:
            xc = round(float(xc))
            yc = round(float(yc))
            ra = round(float(ra))
            rb = round(float(rb))
            value_alg = algorithmsRB.get()

            if value_alg == 0:
                canonical_ellipse(xc, yc, ra, rb, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 1:
                parameter_ellipse(xc, yc, ra, rb, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 2:
                midpoint_ellipse(xc, yc, ra, rb, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 3:
                bresenham_ellipse(xc, yc, ra, rb, LINE_COLOUR, canvasFiled, True)
            elif value_alg == 4:
                standart_oval(canvasFiled, xc, yc, ra, rb, LINE_COLOUR)
        except:
            messagebox.showwarning('Ошибка ввода',
                                   'В данных для построения эллипса введенно(ы) некорректный(ые) символ(ы)!')


def spectrumCircleBy_algorith(canvas, alg, xc, yc, rs, step, count, colour):
    for e in range(0, count):
        alg(xc, yc, rs, colour, canvas, True)
        rs += step


def spectrumEllipseBy_algorith(canvas, alg, xc, yc, ra, rb, step, count, colour):
    for e in range(0, count):
        alg(xc, yc, ra, rb, colour, canvas, True)
        ra += step
        rb += step


NUMBER_OF_RUNS = 5
MAX_RADIUS = 10000
STEP = 1000


def time_ellipse(canvas, alg, xc, yc, ra, rb):
    alg(xc, yc, ra, rb, LINE_COLOUR, canvas, False)


def time_comparison(figure):



    if figure == "ellipse":
        figure = "эллипса"
    else:
        figure = "окружности"

    plt.figure(figsize=(10, 6))
    plt.rcParams['font.size'] = '12'
    plt.title("Замеры времени для построения %s различными методами.\n" %(figure))

    # plt.plot(radius_arr, time_list[0], label='Каноническое уравнение')
    # plt.plot(radius_arr, time_list[1], label='Параметрическое уравнение')
    # plt.plot(radius_arr, time_list[2], label='Алгоритм средней точки')
    # plt.plot(radius_arr, time_list[3], label='Алгоритм Брезенхема')
    # plt.plot(radius_arr, time_list[4], label='Библиотечная функция')

    plt.xticks(np.arange(STEP, MAX_RADIUS + STEP, STEP))
    plt.legend()
    plt.xlabel("Длина радиуса")
    plt.ylabel("Время")

    plt.show()

def draw_spectrum(mode):

    xc = xcEntry.get()
    yc = ycEntry.get()

    if not xc or not yc:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты центра фигуры!')
    else:
        xc = round(float(yc))
        yc = round(float(yc))

        step = stepEntry.get()
        count = countEntry.get()
        if not step:
            messagebox.showwarning('Ошибка ввода',
                                   'Не задан шаг изменения!')
        elif not count:
            messagebox.showwarning('Ошибка ввода',
                                   'Не заданo количество фигур!')
        else:

            step = round(float(step))
            count = int(count)

            if mode == "circle":

                rs = spnREntry.get()
                if not rs:
                    messagebox.showwarning('Ошибка ввода',
                                           'Не заданo начальный радиус окружности для построения спектра!')
                else:
                    rs = round(float(rs))
                    value_alg = algorithmsRB.get()
                    if value_alg == 0:
                        spectrumCircleBy_algorith(canvasFiled, canonical_сircle, xc, yc, rs, step, count, LINE_COLOUR)
                    elif value_alg == 1:
                        spectrumCircleBy_algorith(canvasFiled, parameter_circle, xc, yc, rs, step, count, LINE_COLOUR)
                    elif value_alg == 2:
                        spectrumCircleBy_algorith(canvasFiled, midpoint_circle, xc, yc, rs, step, count, LINE_COLOUR)
                    elif value_alg == 3:
                        spectrumCircleBy_algorith(canvasFiled, bresenham_circle_octant, xc, yc, rs, step, count, LINE_COLOUR)
                    elif value_alg == 4:
                        spectrumBy_standart(canvasFiled, xc, yc, rs, rs, step, count, LINE_COLOUR)
            elif mode == "ellipse":
                ra = spnRxEntry.get()
                rb = spnRyEntry.get()
                if not ra or not rb:
                    messagebox.showwarning('Ошибка ввода',
                                           'Не заданo начальные радиусы эллипса для построения спектра!')
                else:
                    ra = round(float(ra))
                    rb = round(float(rb))

                    value_alg = algorithmsRB.get()
                    if value_alg == 0:
                        spectrumEllipseBy_algorith(canvasFiled, canonical_ellipse, xc, yc, ra, rb, step, count, LINE_COLOUR)
                    elif value_alg == 1:
                        spectrumEllipseBy_algorith(canvasFiled, parameter_ellipse, xc, yc, ra, rb, step, count, LINE_COLOUR)
                    elif value_alg == 2:
                        spectrumEllipseBy_algorith(canvasFiled, midpoint_ellipse, xc, yc, ra, rb, step, count, LINE_COLOUR)
                    elif value_alg == 3:
                        spectrumEllipseBy_algorith(canvasFiled, bresenham_ellipse, xc, yc, ra, rb, step, count, LINE_COLOUR)
                    elif value_alg == 4:
                        spectrumBy_standart(canvasFiled, xc, yc, ra, rb, step, count, LINE_COLOUR)
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

algorithmsArr = [("Канонического уравнения", 0),
                 ("Параметрического уравнения", 1),
                 ("Алгоритм средней точки", 2),
                 ("Алгоритм Брезенхема", 3),
                 ("Библиотечная функция", 4)]
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

yColourBG = 7.1
chooseColourMainLabel.place(x=0, y=6.1 * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
bgColourLabel.place(x=10, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 3, height=DATA_FRAME_HEIGHT // COLUMNS)

whiteBg.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
yellowBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + size, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
orangeBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 2 * size, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
redBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 3 * size, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
purpleBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 4 * size, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
greenBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 5 * size, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
darkGreenBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 6 * size, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
lightBlueBg.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 7 * size, y=yColourBG * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)

bgColourBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourBG + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
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

yColourLine = 9.1
lineColourLabel.place(x=5, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 3, height=DATA_FRAME_HEIGHT // COLUMNS)

whiteLine.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
yellowLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
orangeLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 2 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
redLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 3 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
purpleLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 4 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
greenLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 5 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
darkGreenLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 6 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)
lightBlueLine.place(x=(DATA_FRAME_WIGHT // 3 - BORDERS_SPACE) + 7 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS)

lineColourBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourLine + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourTextLabel.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourLabel.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE + DATA_FRAME_WIGHT // 2, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5, width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение окружности и эллипса

lineMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ ОКРУЖНОСТИ или ЭЛЛИПСА",
                             font=("Consolas", 16),
                             fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

lineMakeCircle = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="ОКРУЖНОСТЬ",
                     font=("Consolas", 14),
                     fg=MAIN_COLOUR_LABEL_TEXT)

lineMakeEllipse = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="ЭЛЛИПС",
                     font=("Consolas", 14),
                     fg=MAIN_COLOUR_LABEL_TEXT)

argumnetsCenterLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Коорд. центра:     Xс         Yс                  ",
                     font=("Consolas", 14),  justify="right",
                     fg=MAIN_COLOUR_LABEL_TEXT)

radiusCircleLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Радиус (R):",
                     font=("Consolas", 14),  justify="center",
                     fg=MAIN_COLOUR_LABEL_TEXT)
widthEllipseLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Высота (Ry):",
                     font=("Consolas", 14),  justify="center",
                     fg=MAIN_COLOUR_LABEL_TEXT)

heightEllipseLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Ширина (Rx):",
                     font=("Consolas", 14),  justify="center",
                     fg=MAIN_COLOUR_LABEL_TEXT)

xcEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
ycEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
rEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
rxEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
ryEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
drawCircleBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить окружность", font=("Consolas", 14),
                          command=draw_circle)
drawEllipseBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить эллипс", font=("Consolas", 14),
                          command=draw_ellipse)

makeCircleOREllipse = 12.2
lineMakeLabel.place(x=0, y=makeCircleOREllipse * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
argumnetsCenterLabel.place(x=0, y=(makeCircleOREllipse + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
xcEntry.place(x=DATA_FRAME_WIGHT // 4, y=(makeCircleOREllipse + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
ycEntry.place(x=2 * DATA_FRAME_WIGHT // 4, y=(makeCircleOREllipse + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)

lineMakeCircle.place(x=0, y=(makeCircleOREllipse + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
lineMakeEllipse.place(x=DATA_FRAME_WIGHT // 2, y=(makeCircleOREllipse + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)

radiusCircleLabel.place(x=0, y=(makeCircleOREllipse + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
rEntry.place(x=DATA_FRAME_WIGHT // 4, y=(makeCircleOREllipse + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 20, height=DATA_FRAME_HEIGHT // COLUMNS)
drawCircleBtn.place(x=10, y=(makeCircleOREllipse + 6) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 30, height=DATA_FRAME_HEIGHT // COLUMNS)

heightEllipseLabel.place(x=10 + 2 * DATA_FRAME_WIGHT // 4, y=(makeCircleOREllipse + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)
widthEllipseLabel.place(x=10 + 2 * DATA_FRAME_WIGHT // 4, y=(makeCircleOREllipse + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)
rxEntry.place(x=10 + 3 * DATA_FRAME_WIGHT // 4, y=(makeCircleOREllipse + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 20, height=DATA_FRAME_HEIGHT // COLUMNS)
ryEntry.place(x=10 + 3 * DATA_FRAME_WIGHT // 4, y=(makeCircleOREllipse + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 20, height=DATA_FRAME_HEIGHT // COLUMNS)
drawEllipseBtn.place(x=10 + DATA_FRAME_WIGHT // 2, y=(makeCircleOREllipse + 6) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 20, height=DATA_FRAME_HEIGHT // COLUMNS)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение спектра

specterMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ СПЕКТРА ОКРУЖНОСТИ или ЭЛЛИПСА",
                             font=("Consolas", 16),
                             fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

msgAboutCenterPoint = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Координаты центра выше",
                             font=("Consolas", 14),
                             fg=MAIN_COLOUR_LABEL_TEXT)

specterMakeCircle = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="ОКРУЖНОСТЬ",
                     font=("Consolas", 14),
                     fg=MAIN_COLOUR_LABEL_TEXT)

specterMakeEllipse = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="ЭЛЛИПС",
                     font=("Consolas", 14),
                     fg=MAIN_COLOUR_LABEL_TEXT)

spnRadiusCircleLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Нач. Радиус:",
                     font=("Consolas", 14),  justify="center",
                     fg=MAIN_COLOUR_LABEL_TEXT)
spnWidthEllipseLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Нач. Высота:",
                     font=("Consolas", 14),  justify="center",
                     fg=MAIN_COLOUR_LABEL_TEXT)

spnHeightEllipseLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Нач. Ширина:",
                     font=("Consolas", 14),  justify="center",
                     fg=MAIN_COLOUR_LABEL_TEXT)

stepSpecterLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Шаг изменения:",
                     font=("Consolas", 14),  justify="left",
                     fg=MAIN_COLOUR_LABEL_TEXT)

countSpecterLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Количество фигур:",
                     font=("Consolas", 14),  justify="left",
                     fg=MAIN_COLOUR_LABEL_TEXT)

spnREntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
spnRxEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
spnRyEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
stepEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
countEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")

drawSpnCircleBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить спектор\nокружностей", font=("Consolas", 14),
                             command=lambda: draw_spectrum("circle"))
drawSpnEllipseBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить спектор\n эллипсов", font=("Consolas", 14),
                              command=lambda: draw_spectrum("ellipse"))

makeSpecter = 19.3
specterMakeLabel.place(x=0, y=makeSpecter * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutCenterPoint.place(x=0, y=(makeSpecter + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)

specterMakeCircle.place(x=0, y=(makeSpecter + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
specterMakeEllipse.place(x=DATA_FRAME_WIGHT // 2, y=(makeSpecter + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)

spnRadiusCircleLabel.place(x=0, y=(makeSpecter + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
spnREntry.place(x=DATA_FRAME_WIGHT // 4, y=(makeSpecter + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 20, height=DATA_FRAME_HEIGHT // COLUMNS)


spnHeightEllipseLabel.place(x=10 + 2 * DATA_FRAME_WIGHT // 4, y=(makeSpecter + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)
spnWidthEllipseLabel.place(x=10 + 2 * DATA_FRAME_WIGHT // 4, y=(makeSpecter + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)
spnRxEntry.place(x=10 + 3 * DATA_FRAME_WIGHT // 4, y=(makeSpecter + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 20, height=DATA_FRAME_HEIGHT // COLUMNS)
spnRyEntry.place(x=10 + 3 * DATA_FRAME_WIGHT // 4, y=(makeSpecter + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4 - 20, height=DATA_FRAME_HEIGHT // COLUMNS)

stepSpecterLabel.place(x=0, y=(makeSpecter + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 3, height=DATA_FRAME_HEIGHT // COLUMNS)
stepEntry.place(x=DATA_FRAME_WIGHT // 3, y=(makeSpecter + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)

countSpecterLabel .place(x=0, y=(makeSpecter + 6) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 3, height=DATA_FRAME_HEIGHT // COLUMNS)
countEntry.place(x=DATA_FRAME_WIGHT // 3, y=(makeSpecter + 6) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)

drawSpnCircleBtn.place(x=10, y=(makeSpecter + 7) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 30, height=2 * DATA_FRAME_HEIGHT // COLUMNS)
drawSpnEllipseBtn.place(x=10 + DATA_FRAME_WIGHT // 2, y=(makeSpecter + 7) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 20, height=2 * DATA_FRAME_HEIGHT // COLUMNS)
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


TimeBarSpnCircleBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Сравнение времени\n построение окружности", font=("Consolas", 14))
TimeBarEllipseBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Сравнение времени\n построение эллипса", font=("Consolas", 14),
                              command=lambda: time_comparison("ellipse"))

clearCanvasBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Очистить экран", font=("Consolas", 14), command=clearScreen)
infoBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Справка", font=("Consolas", 14),
                    command=show_info)

TimeBarSpnCircleBtn.place(x=10, y=(makeSpecter + 9) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 30, height=2 * DATA_FRAME_HEIGHT // COLUMNS)
TimeBarEllipseBtn.place(x=10 + DATA_FRAME_WIGHT // 2, y=(makeSpecter + 9) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 20, height=2 * DATA_FRAME_HEIGHT // COLUMNS)
clearCanvasBtn.place(x=40, y=(makeSpecter + 12) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80, height=DATA_FRAME_HEIGHT // COLUMNS)
infoBtn.place(x=40, y=(makeSpecter + 13) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CANVAS FILED FOR DRAWING lines and spectres by algorithms
canvasFiled = tk.Canvas(root, bg=CANVAS_COLOUR)
canvasFiled.place(x=WINDOW_WIDTH * DATA_SITUATION + BORDERS_SPACE, y=BORDERS_SPACE, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

xcEntry.insert(0, str(545))
ycEntry.insert(0, str(350))

#drawAxes()

root.mainloop()