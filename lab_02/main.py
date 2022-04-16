import tkinter as tk
import config as cfg
import tkinter.messagebox as mb
import buttonFunction as bf
from math import pi, cos, sin

root = tk.Tk()
root.title("КГ Лабораторная работа 2")
root["bg"] = cfg.MAIN_COLOUR

root.geometry(str(cfg.WINDOW_WIDTH) + "x" + str(cfg.WINDOW_HEIGHT))
root.resizable(height=False, width=False)

dataFrame = tk.Frame(root)
dataFrame["bg"] = cfg.MAIN_FRAME_COLOR

dataFrame.place(x=int(cfg.BORDERS_SPACE), y=int(cfg.BORDERS_SPACE),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT)

### -----------------------------------------------------
### Сбор фигуры на начальное значение
def throwFigure():
    if bf.forwardList or bf.backList:
        field.delete("all")
        bf.backList.clear()
        bf.forwardList.clear()
        bf.fillFigureList()
        bf.drawAxis(field)
        bf.drawFigure(field)
###------------------------------------------------------

###------------------------------------------------------
### Изменение параметров фигуры
def changeParams():
    try:
        bf.A = float(aEntry.get())
        bf.B = float(bEntry.get())
        bf.C = float(cEntry.get())
        bf.R = float(rEntry.get())
    except ValueError:
        mb.showerror("Некорректные данные", "Ожидались действительные числа! (При этом R != 0)")
    else:
        bf.backList.clear()
        bf.forwardList.clear()
        bf.fillFigureList()
        field.delete("all")
        bf.drawAxis(field)
        bf.drawFigure(field)
###-------------------------------------------------------

###-------------------------------------------------------
### Перенос фигуры используя матрицы переноса
def moveFigure():
    try:
        x = float(dxEntry.get())
        y = float(dyEntry.get())
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")

    else:
        move_matrix = [[1, 0, x], [0, 1, y], [0, 0, 1]]
        bf.apply_command(move_matrix)

        if bf.forwardList:
            bf.forwardList.clear()

        bf.backList.append(bf.find_reversed_matrix(move_matrix))

    # dxEntry.delete(0, tk.END)
    # dyEntry.delete(0, tk.END)
    field.delete("all")
    bf.drawAxis(field)
    bf.drawFigure(field)
###-------------------------------------------------------

###-------------------------------------------------------
### Поворот фигуры (сначала перемещение в центр поворота, затем поворот и затем обратный перенос)
def rotateFigure():
    try:
        x = (-1) * float(rxEntry.get())
        y = (-1) * float(ryEntry.get())
        angle = float(angleEntry.get()) * pi / 180
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")

    else:
        move_matrix = [[1, 0, -x], [0, 1, -y], [0, 0, 1]] # Матрица переноса
        rotate_matrix = [[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]] # Матрица поворота
        unmove_matrix = [[1, 0, x], [0, 1, y], [0, 0, 1]] # Матрица обратного переноса

        result_matrix = bf.mul_matrices(move_matrix, rotate_matrix)
        result_matrix = bf.mul_matrices(result_matrix, unmove_matrix)

        bf.apply_command(result_matrix)

        if bf.forwardList:
            bf.forwardList.clear()
        bf.backList.append(bf.find_reversed_matrix(result_matrix))

    # rxEntry.delete(0, tk.END)
    # ryEntry.delete(0, tk.END)
    # angleEntry.delete(0, tk.END)
    field.delete("all")
    bf.drawAxis(field)
    bf.drawFigure(field)
###-------------------------------------------------------

###-------------------------------------------------------
### Масштабирование фигуры
def scaleFigure():
    try:
        x = (-1) * float(scxEntry.get())
        y = (-1) * float(scyEntry.get())
        kx = float(sxEntry.get())
        ky = float(syEntry.get())
        if not kx or not ky:
            raise ZeroDivisionError
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")

    except ZeroDivisionError:
        mb.showerror("Плохие данные.", "При данных значениях масштабирования фигура "
                                       "превратится либо в точку, либо в прямую. Не допускаю!")

    else:
        move_matrix = [[1, 0, -x], [0, 1, -y], [0, 0, 1]] # Матрица переноса
        scale_matrix = [[kx, 0, 0], [0, ky, 0], [0, 0, 1]] # матрица масштабирования
        unmove_matrix = [[1, 0, x], [0, 1, y], [0, 0, 1]] # матрица обратного поворота

        result_matrix = bf.mul_matrices(move_matrix, scale_matrix)
        result_matrix = bf.mul_matrices(result_matrix, unmove_matrix)

        bf.apply_command(result_matrix)

        if bf.forwardList:
            bf.forwardList.clear()
        bf.backList.append(bf.find_reversed_matrix(result_matrix))

    # scxEntry.delete(0, tk.END)
    # scyEntry.delete(0, tk.END)
    # sxEntry.delete(0, tk.END)
    # syEntry.delete(0, tk.END)
    field.delete("all")
    bf.drawAxis(field)
    bf.drawFigure(field)
##-------------------------------------------------------------------------

##-------------------------------------------------------------------------
## Шаг назад
def backFigure():
    if bf.backList:
        matrix = bf.backList.pop()
        bf.apply_command(matrix)
        bf.forwardList.append(bf.find_reversed_matrix(matrix))
        field.delete("all")
        bf.drawAxis(field)
        bf.drawFigure(field)
##-------------------------------------------------------------------------

##-------------------------------------------------------------------------
## Шаг вперед
def forwardFigure():
    if bf.forwardList:
        matrix = bf.forwardList.pop()
        bf.apply_command(matrix)
        bf.backList.append(bf.find_reversed_matrix(matrix))
        field.delete("all")
        bf.drawAxis(field)
        bf.drawFigure(field)
##-------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------
# For move command.
# ----------------------------------------------------------------------------------------------------------------
moveInfButton = tk.Button(dataFrame, text="i", font=("Consolas", 20), bg=cfg.ADD_COLOUR, fg=cfg.TEXT_ENTRY_COLOUR,
                          activebackground=cfg.ADD_COLOUR, command=bf.showInfoMove,
                          activeforeground=cfg.MAIN_COLOUR)

moveLabel = tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="ПЕРЕМЕЩЕНИЕ",
                     font=("Consolas", 16),
                     fg=cfg.TEXT_ENTRY_COLOUR, relief=tk.GROOVE)

dxEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 14),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
dyEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 15),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
moveBtn = tk.Button(dataFrame, text="Переместить", font=("Consolas", 14),
                    bg=cfg.MAIN_FRAME_COLOR, fg=cfg.TEXT_ENTRY_COLOUR, command=moveFigure,
                    activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_FRAME_COLOR)

moveLabel.place(x=0, y=0, width=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
moveInfButton.place(x=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, y=0, width=cfg.DATA_WIDTH * (1 - cfg.DATA_K_LABEL), height=cfg.DATA_HEIGHT // cfg.COLUMNS)

tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="dx         dy",
                     font=("Consolas", 18),
                     fg=cfg.TEXT_ENTRY_COLOUR).\
                    place(x=0, y=cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

dxEntry.place(x=0, y=2 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH // 2,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
dyEntry.place(x=cfg.DATA_WIDTH // 2, y=2 * cfg.DATA_HEIGHT // cfg.COLUMNS,
               width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
moveBtn.place(x=0, y=3 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------
# For rotate command.
# ----------------------------------------------------------------------------------------------------------------
rotateInfButton = tk.Button(dataFrame, text="i", font=("Consolas", 20),
                        bg=cfg.ADD_COLOUR, fg=cfg.TEXT_ENTRY_COLOUR, command=bf.showInfoRotate,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

rotateLabel = tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="ПОВЕРНУТЬ",
                     font=("Consolas", 16),
                     fg=cfg.TEXT_ENTRY_COLOUR, relief=tk.GROOVE)

rxEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
ryEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
angleEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                       fg=cfg.MAIN_FRAME_COLOR, justify="center")

rotateBtn = tk.Button(dataFrame, text="Повернуть", font=("Consolas", 14),
                    bg=cfg.MAIN_FRAME_COLOR, fg=cfg.TEXT_ENTRY_COLOUR, command=rotateFigure,
                    activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_FRAME_COLOR)

rotateLabel.place(x=0, y=cfg.DATA_HEIGHT * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 10, width=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
rotateInfButton.place(x=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, y=cfg.DATA_HEIGHT * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 10, width=cfg.DATA_WIDTH * (1 - cfg.DATA_K_LABEL), height=cfg.DATA_HEIGHT // cfg.COLUMNS)

tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="rx      ry    angle",
                     font=("Consolas", 18),
                     fg=cfg.TEXT_ENTRY_COLOUR).\
                    place(x=0, y=cfg.DATA_HEIGHT * cfg.COLUMNS_DATA_BORDERS_HEIGHT + cfg.DATA_HEIGHT // cfg.COLUMNS + 10, width=cfg.DATA_WIDTH, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

rxEntry.place(x=0, y=cfg.DATA_HEIGHT * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 10, width=cfg.DATA_WIDTH // 3,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)

ryEntry.place(x=cfg.DATA_WIDTH // 3, y=cfg.DATA_HEIGHT * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 10,
               width=cfg.DATA_WIDTH // 3, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

angleEntry.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.DATA_HEIGHT * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 10,
               width=cfg.DATA_WIDTH // 3, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

rotateBtn.place(x=0, y=cfg.DATA_HEIGHT * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 3 * cfg.DATA_HEIGHT // cfg.COLUMNS + 10, width=cfg.DATA_WIDTH,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------
# For scale command.
# ----------------------------------------------------------------------------------------------------------------
scaleInfButton = tk.Button(dataFrame, text="i", font=("Consolas", 20),
                        bg=cfg.ADD_COLOUR, fg=cfg.TEXT_ENTRY_COLOUR, command=bf.showInfoScale,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

scaleLabel = tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="МАСШТАБИРОВАНИЕ",
                     font=("Consolas", 16),
                     fg=cfg.TEXT_ENTRY_COLOUR, relief=tk.GROOVE)

sxEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
syEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
scxEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                       fg=cfg.MAIN_FRAME_COLOR, justify="center")
scyEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                       fg=cfg.MAIN_FRAME_COLOR, justify="center")

scaleBtn = tk.Button(dataFrame, text="Масштабировать", font=("Consolas", 14),
                    bg=cfg.MAIN_FRAME_COLOR, fg=cfg.TEXT_ENTRY_COLOUR, command=scaleFigure,
                    activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_FRAME_COLOR)

scaleLabel.place(x=0, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 20, width=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
scaleInfButton.place(x=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 20, width=cfg.DATA_WIDTH * (1 - cfg.DATA_K_LABEL), height=cfg.DATA_HEIGHT // cfg.COLUMNS)

tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="kx    ky    cx    cy",
                     font=("Consolas", 18),
                     fg=cfg.TEXT_ENTRY_COLOUR).\
                    place(x=0, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + cfg.DATA_HEIGHT // cfg.COLUMNS + 20, width=cfg.DATA_WIDTH, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

sxEntry.place(x=0, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 20, width=cfg.DATA_WIDTH // 3,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)

syEntry.place(x=cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 20,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

scxEntry.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 20,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

scyEntry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 20,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

scaleBtn.place(x=0, y=cfg.DATA_HEIGHT * 2 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 3 * cfg.DATA_HEIGHT // cfg.COLUMNS + 20, width=cfg.DATA_WIDTH,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------
# For const command.
# ----------------------------------------------------------------------------------------------------------------
constInfButton = tk.Button(dataFrame, text="i", font=("Consolas", 20),
                        bg=cfg.ADD_COLOUR, fg=cfg.TEXT_ENTRY_COLOUR, command=bf.showInfoParams,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

constLabel = tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="Параметры",
                     font=("Consolas", 16),
                     fg=cfg.TEXT_ENTRY_COLOUR, relief=tk.GROOVE)

aEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
bEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_FRAME_COLOR, justify="center")
cEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                       fg=cfg.MAIN_FRAME_COLOR, justify="center")
rEntry = tk.Entry(dataFrame, bg=cfg.TEXT_ENTRY_COLOUR, font=("Consolas", 13),
                       fg=cfg.MAIN_FRAME_COLOR, justify="center")

constBtn = tk.Button(dataFrame, text="Построить", font=("Consolas", 14),
                    bg=cfg.MAIN_FRAME_COLOR, fg=cfg.TEXT_ENTRY_COLOUR, command=changeParams,
                    activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_FRAME_COLOR)

constLabel.place(x=0, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 30, width=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
constInfButton.place(x=cfg.DATA_WIDTH * cfg.DATA_K_LABEL, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 30, width=cfg.DATA_WIDTH * (1 - cfg.DATA_K_LABEL), height=cfg.DATA_HEIGHT // cfg.COLUMNS)

tk.Label(dataFrame, bg=cfg.ADD_COLOUR, text="a    b    c    r",
                     font=("Consolas", 18),
                     fg=cfg.TEXT_ENTRY_COLOUR).\
                    place(x=0, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + cfg.DATA_HEIGHT // cfg.COLUMNS + 30, width=cfg.DATA_WIDTH, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

aEntry.place(x=0, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 30, width=cfg.DATA_WIDTH // 3,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)

bEntry.place(x=cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 30,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

cEntry.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 30,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

rEntry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * cfg.DATA_HEIGHT // cfg.COLUMNS + 30,
             width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

constBtn.place(x=0, y=cfg.DATA_HEIGHT * 3 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 3 * cfg.DATA_HEIGHT // cfg.COLUMNS + 30, width=cfg.DATA_WIDTH,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------
# For steps.
# ----------------------------------------------------------------------------------------------------------------

backBtn = tk.Button(dataFrame, text="<--", font=("Consolas", 24),
                    bg=cfg.MAIN_COLOUR, fg=cfg.TEXT_ENTRY_COLOUR, command=backFigure,
                    activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

forwardBtn = tk.Button(dataFrame, text="-->", font=("Consolas", 24),
                       bg=cfg.MAIN_COLOUR, fg=cfg.TEXT_ENTRY_COLOUR, command=forwardFigure,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

throwBtn = tk.Button(dataFrame, text="Сбросить", font=("Consolas", 20),
                      bg=cfg.MAIN_COLOUR, fg=cfg.TEXT_ENTRY_COLOUR, command=throwFigure,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

backBtn.place(x=0, y=cfg.DATA_HEIGHT * 4 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 40, width=cfg.DATA_WIDTH // 2,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)

forwardBtn.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * 4 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 40,
                  width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.COLUMNS)

throwBtn.place(x=0, y=cfg.DATA_HEIGHT * 4 * cfg.COLUMNS_DATA_BORDERS_HEIGHT + 2 * 40,
                  width=cfg.DATA_WIDTH, height=cfg.DATA_HEIGHT // cfg.COLUMNS)


# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

field = tk.Canvas(root, bg="lightblue")
field.place(x=cfg.WINDOW_WIDTH * cfg.BORDERS_MAIN_MAKE + 2 * cfg.BORDERS_SPACE, y=cfg.BORDERS_SPACE, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)


bf.fillFigureList()
bf.drawAxis(field)
bf.drawFigure(field)

aEntry.insert(0, bf.A)
bEntry.insert(0, bf.B)
cEntry.insert(0, bf.C)
rEntry.insert(0, bf.R)

root.mainloop()
