from algrorithm import *
from brezenhem import bresenhem_int

import tkinter as tk
from tkinter import colorchooser, messagebox
from config import *
import time

root = tk.Tk()
root.title("КГ Лабораторная работа №6")
root["bg"] = MAIN_COLOUR

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(height=False, width=False)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clearScreen():
    allFigures.clear()
    currentFigure.clear()
    listPoint_scroll.delete(0, tk.END)
    canvasField.delete("all")
    canvasImg.put(CANVAS_COLOUR, to=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
    canvasField.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=canvasImg, state="normal")

def fill_all_figures():
    if not allFigures and not currentFigure:
        messagebox.showwarning("Предупреждение!", "Фигура не введена для закраски!")
    elif not allFigures and  currentFigure:
        messagebox.showwarning("Предупреждение!", "Фигура не замкнута для закраски!")
    else:

        if not seed_pixels:
            messagebox.showwarning("Предупреждение!", "Затравочный пиксел не установлен!")
            return
        if BORDER_COLOUR == FILL_COLOUR:
            messagebox.showwarning("Предупреждение!", "Цвет границы и цвет закраски не должны совпадать!")
            return
        if BORDER_COLOUR == CANVAS_COLOUR:
            messagebox.showwarning("Предупреждение!", "Цвет границы и цвет фона не должны совпадать!")
            return
        if CANVAS_COLOUR == FILL_COLOUR:
            messagebox.showwarning("Предупреждение!", "Цвет фона и цвет закраски не должны совпадать!")
            return

        delay = False
        if methodDraw.get() == 0:
            delay = True
        print(seed_pixels)
        time_start = time.time()
        line_by_line_filling_algorithm_with_seed(canvasField, canvasImg, BORDER_COLOUR,
                                  FILL_COLOUR, seed_pixels[-1], delay=delay)
        time_end = time.time() - time_start
        if round(time_end * 1000, 2) < 1000:
            timeLabel["text"] = "Время закраски: " + str(round(time_end * 1000, 2)) + " mc."
        else:
            timeLabel["text"] = "Время закраски: " + str(round(time_end, 2)) + " c."
def get_point():
    x = xEntry.get()
    y = yEntry.get()
    if not x or not y:
        messagebox.showinfo("Предупреждение!", "Координаты точек не введены!")
    else:
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            messagebox.showinfo("Предупреждение!", "Координаты точек должны быть только целые!")
            return
        add_point(x, y)


def close_figure():
    global currentFigure
    if len(currentFigure) > 2:
        draw_line_on_img(canvasImg, currentFigure[-1], currentFigure[0], BORDER_COLOUR)

        index = findIndexForListPointScroll(allFigures, currentFigure)
        listPoint_scroll.insert(index, "------------Closed------------")

        allFigures.append(currentFigure)
        currentFigure = []
    elif len(currentFigure) == 0:
        messagebox.showwarning("Предупреждение!", "Точки фигуры не введены!")
    else:
        messagebox.showwarning("Предупреждение!", "Такую фигуру нельзя замкнуть!\nНеобходимо как минимум, чтобы у фигуры было 3 точки!")


def findIndexForListPointScroll(allArraysFigure, currentArray):
    index = 0

    for pointFigure in allArraysFigure:
         index += len(pointFigure) + 1

    index += len(currentArray)
    return index


def draw_line_on_img(img, ps, pe, colour="#000000"):
    points = bresenhem_int(ps, pe)
    for p in points:
        draw_pixel(img, p.x, p.y, colour)

def add_point(x, y, colour="#000000"):
    if Point(x, y) not in currentFigure:
        # canvasField.create_text(x, y - 10, text=(str(x) + " " + str(y)))
        if currentFigure:
            draw_line_on_img(canvasImg, currentFigure[-1], Point(x, y), colour)
        index = findIndexForListPointScroll(allFigures, currentFigure)
        listPoint_scroll.insert(index,  "{:3d}) X = {:4d}; Y = {:4d}".format(index + 1, x, y))
        currentFigure.append(Point(x, y))
    else:
        messagebox.showwarning("Предупреждение!", "Точка с такими координатами фигуры уже введена!")


def add_seed(event):
    x, y = event.x, event.y

    canvasField.create_oval(x, y, x, y, outline="orange", width=3)

    seed_pixels.append(Point(x, y))

def add_point_figure_onClick(event):
    x, y = event.x,  event.y
    add_point(x, y, BORDER_COLOUR)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INPUT DATA FRAME


dataFrame = tk.Frame(root, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT)
dataFrame["bg"] = MAIN_FRAME_COLOR

dataFrame.pack(side=tk.LEFT, padx=BORDERS_SPACE, fill=tk.Y)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ВЫБОР цвета

chooseColourMainLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ВЫБОР ЦВЕТА ЗАКРАСКИ",
                     font=("Consolas", 16), fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

size = (DATA_FRAME_WIGHT // 1.6) // 8
chooseColourMainLabel.place(x=0, y=0, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# выбор цвета закраски

borderColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет границы:",
                     font=("Consolas", 14),
                     fg=MAIN_COLOUR_LABEL_TEXT)
fillColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет закраски:",
                     font=("Consolas", 13),
                     fg=MAIN_COLOUR_LABEL_TEXT)
bgColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет фона:",
                     font=("Consolas", 14),
                     fg=MAIN_COLOUR_LABEL_TEXT)

borderCurColourLabel = tk.Label(dataFrame, bg=BORDER_COLOUR)
fillCurColourLabel = tk.Label(dataFrame, bg=FILL_COLOUR)
bgCurColourLabel = tk.Label(dataFrame, bg=CANVAS_COLOUR)

def get_colour(mode):
    global BORDER_COLOUR, FILL_COLOUR, CANVAS_COLOUR
    if mode == "border":
        colour_code = colorchooser.askcolor(title="Выбрать цвет границы!")
        colour = colour_code[-1]
        BORDER_COLOUR = colour
        borderCurColourLabel.configure(bg=colour)
    if mode == "fill":
        colour_code = colorchooser.askcolor(title="Выбрать цвет закраски!")
        colour = colour_code[-1]
        FILL_COLOUR = colour
        fillCurColourLabel.configure(bg=colour)
    if mode == "bg":
        colour_code = colorchooser.askcolor(title="Выбрать цвет границы!")
        colour = colour_code[-1]
        CANVAS_COLOUR = colour
        canvasImg.put(colour, to=(0,0, CANVAS_WIDTH, CANVAS_HEIGHT))
        bgCurColourLabel.configure(bg=colour)



borderColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать цвет гр-цы', font=("Consolas", 13), command=lambda: get_colour("border"))
fillColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать цвет закр-ки', font=("Consolas", 13), command=lambda: get_colour("fill"))
bgColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать цвет фона', font=("Consolas", 13), command=lambda: get_colour("bg"))

yColourLine = 1.2
borderColourLabel.place(x=0, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5, height=DATA_FRAME_HEIGHT // COLUMNS)
fillColourLabel.place(x=0, y=(yColourLine + 1.1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5, height=DATA_FRAME_HEIGHT // COLUMNS)
bgColourLabel.place(x=0, y=(yColourLine + 2.2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5, height=DATA_FRAME_HEIGHT // COLUMNS)


borderColourBtn.place(x=1.5 * DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
fillColourBtn.place(x=1.5 * DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourLine + 1.1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
bgColourBtn.place(x=1.5 * DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourLine + 2.2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)


borderCurColourLabel.place(x=DATA_FRAME_WIGHT // 3 + BORDERS_SPACE, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS + 5, width=DATA_FRAME_WIGHT // 9, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
fillCurColourLabel.place(x=DATA_FRAME_WIGHT // 3 + BORDERS_SPACE, y=(yColourLine + 1.1) * DATA_FRAME_HEIGHT // COLUMNS + 5, width=DATA_FRAME_WIGHT // 9, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
bgCurColourLabel.place(x=DATA_FRAME_WIGHT // 3 + BORDERS_SPACE, y=(yColourLine + 2.2) * DATA_FRAME_HEIGHT // COLUMNS + 5, width=DATA_FRAME_WIGHT // 9, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Режим закраски

modeMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="РЕЖИМ ЗАКРАСКИ",
                         font=("Consolas", 16),
                         fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

modeDraw = yColourLine + 3.1
methodDraw = tk.IntVar()
methodDraw.set(1)
modeMakeLabel.place(x=0, y=modeDraw * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
tk.Radiobutton(dataFrame, variable=methodDraw, text="С задержкой", value=0, bg=MAIN_FRAME_COLOR,
                font=("Consolas", 16), justify=tk.LEFT, fg=MAIN_COLOUR_LABEL_TEXT, selectcolor="purple",
                activebackground=MAIN_FRAME_COLOR, activeforeground=MAIN_COLOUR_LABEL_TEXT,
               ).place(x=10, y=(modeDraw + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 2 * BORDERS_SPACE,
                       height=DATA_FRAME_HEIGHT // COLUMNS)
tk.Radiobutton(dataFrame, variable=methodDraw, text="Без задержки", value=1, bg=MAIN_FRAME_COLOR,
                font=("Consolas", 16), justify=tk.LEFT, fg=MAIN_COLOUR_LABEL_TEXT, selectcolor="purple",
                activebackground=MAIN_FRAME_COLOR, activeforeground=MAIN_COLOUR_LABEL_TEXT,
               ).place(x=DATA_FRAME_WIGHT // 2, y=(modeDraw + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 2 * BORDERS_SPACE,
                       height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение точки

pointMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ точки",
                          font=("Consolas", 16),
                          fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

msgAboutPoint = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="X       Y",
                         font=("Consolas", 16),
                         fg=MAIN_COLOUR_LABEL_TEXT)

xEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")
yEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 14), fg=MAIN_FRAME_COLOR, justify="center")

drawPointBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить точку", font=("Consolas", 14),
                         command=get_point)
drawCloseBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Замкнуть фигуру", font=("Consolas", 14),
                         command=close_figure)

makePoint = modeDraw + 2.1
pointMakeLabel.place(x=0, y=makePoint * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutPoint.place(x=0, y=(makePoint + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)

xEntry.place(x=DATA_FRAME_WIGHT // 4, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
yEntry.place(x=2 * DATA_FRAME_WIGHT // 4, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)

makePoint += 0.2
drawPointBtn.place(x=10, y=(makePoint + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
drawCloseBtn.place(x=DATA_FRAME_WIGHT // 2, y=(makePoint + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)

listPoint_scroll = tk.Listbox(font=("Consolas", 14))
makePoint += 0.4
listPoint_scroll.place(x=40, y=(makePoint + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 60, height=6 * DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

modeByMouse = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ с помощью мыши",
                             font=("Consolas", 16),
                             fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)
labelTextInfo_1 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Левая кнопка - добавить точку",
                             font=("Consolas", 14),
                             fg=MAIN_COLOUR_LABEL_TEXT)
labelTextInfo_2 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Правая кнопка - замкнуть фигуру",
                             font=("Consolas", 14),
                             fg=MAIN_COLOUR_LABEL_TEXT)
modeMouse = makePoint + 10 + 0.2
modeByMouse.place(x=0, y=modeMouse * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
labelTextInfo_1.place(x=0, y=(modeMouse + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
labelTextInfo_2.place(x=0, y=(modeMouse + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Кнопки сравнения, очистки и справки


def show_info():
    messagebox.showinfo('Информация',
                        'С помощью данной программы можно построить фигуру и закрасить ее:\n'
                        '\nДля построения закраски фигуры используется алгоритм с упорядоченным списоком ребер \n'
                        'и его реализация САР(список активных ребер).\n')


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CANVAS FILED FOR DRAWING lines and spectres by algorithms
currentFigure = []
allFigures = []
seed_pixels = []

canvasField = tk.Canvas(root, bg=CANVAS_COLOUR)
canvasField.place(x=WINDOW_WIDTH * DATA_SITUATION + BORDERS_SPACE, y=BORDERS_SPACE, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

canvasImg = tk.PhotoImage(width=CANVAS_WIDTH + 1, height=CANVAS_HEIGHT + 1)
canvasField.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=canvasImg, state="normal")
canvasImg.put(CANVAS_COLOUR, to=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))

canvasField.bind("<Button-1>", add_point_figure_onClick)
canvasField.bind("<Button-2>", add_seed)
canvasField.bind("<Button-3>", lambda event: close_figure())
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

timeLabel = tk.Label(root, bg="gray", text="Время закраски: ",
                             font=("Consolas", 16),
                             fg=MAIN_COLOUR_LABEL_TEXT)
fillingBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Выполнить закраску", font=("Consolas", 14), command=fill_all_figures)
clearCanvasBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Очистить экран", font=("Consolas", 14), command=clearScreen)
infoBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Справка", font=("Consolas", 14),
                    command=show_info)

timeLabel.place(x=DATA_FRAME_WIGHT + 2 * BORDERS_SPACE, y=CANVAS_HEIGHT + BORDERS_SPACE - DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 60, height=DATA_FRAME_HEIGHT // COLUMNS)
fillingBtn.place(x=40, y=(modeMouse + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80, height=DATA_FRAME_HEIGHT // COLUMNS)
clearCanvasBtn.place(x=40, y=(modeMouse + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80, height=DATA_FRAME_HEIGHT // COLUMNS)
infoBtn.place(x=40, y=(modeMouse + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80, height=DATA_FRAME_HEIGHT // COLUMNS)


# # drawAxes()

root.mainloop()