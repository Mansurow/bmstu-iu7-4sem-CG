import tkinter as tk
import tkinter.messagebox as mb
import config as cfg
from math import pi, cos, sin

INFORMATION = '''\
Данная программа предоставляет следующие возможности работы с фигурой, образованной окружностью и \
гипербалом: перемещение, вращение, масштабирование, изменение параметров фигур, а также возврат на \
неограниченное кол-во состояний вперед и назад.\n\n\
Уравнения прямых:
(x - a) ^ 2 + (y - b) ^ 2 = r ^ 2
x = с / x
a, b, c - постоянные коэффициенты
r - радиус окружности
'''
## Параметры уравнения фигуры
A, B, C, R = 0, 0, 0.1, 1
## список функция и заштрихованной части
figureList = [list(), list(), list()]
backList = list()
forwardList = list()


def showInfoParams():
    mb.showinfo("Информация", INFORMATION)


def showInfoMove():
    mb.showinfo("Информация про перенос",
                "(Ввод dx, dy,\nгде dx, dy - перемещение\nпо х и по у соответственно)")


def showInfoRotate():
    mb.showinfo("Информация про поворот",
                "(Ввод x, y, angle,\nгде x, y - координаты центра поворота, \nangle - угол поворота в радианах)")


def showInfoScale():
    mb.showinfo("Информация про масштабирование",
                "(Ввод kx, ky, cx, cy, где \nC(x, y) - центр масштабирования,\n kx, ky - коэффициенты масштабирования)")


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x:g}".strip() + "; " + f"{self.y:g}".strip()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def translate_to_computer_system(pointVector):
    x = (pointVector[0] - cfg.MIN_LIMIT_X) / (cfg.MAX_LIMIT_X - cfg.MIN_LIMIT_X) * cfg.FIELD_WIDTH
    y = (1 - (pointVector[1] - cfg.MIN_LIMIT_Y) / (cfg.MAX_LIMIT_Y - cfg.MIN_LIMIT_Y)) * cfg.FIELD_HEIGHT
    return Point(x, y)


def findPointStrokes():
    pointListStrokes = list()
    for pList in figureList:
        pointListStrokes.extend(
            list(filter(lambda point: (point[0] - A) ** 2 + (point[1] - B) ** 2 <= R * R
                        and point[1] >= C / point[0] and (
                                          (point[0] > 0 and point[1] > 0 and C > 0) or
                                          (point[0] < 0 and point[1] > 0 and C < 0)
                                            )
                                          , pList)))

    return pointListStrokes


def fillFigureList():
    print(A, B, C, R)
    # очищение списка
    for i in range(len(figureList)):
        figureList[i].clear()

    # (x + A)**2 + (y + B)**2 = R**2 - круг
    # A + cos(degrees) * R = x
    # B + sin(degrees) * R = y
    # [x, y, r], r - радиус
    degrees = 0
    while degrees <= 2 * pi:
        figureList[0].append([A + cos(degrees) * R, B + sin(degrees) * R, 1])
        degrees += 1 / (R * cfg.SCALE)

    # y = C / x - гипербало
    # x = C / y
    # [x, y]
    x = cfg.MAX_LIMIT_X * 4
    while x > 0:
        if x != 0:
            figureList[1].append([x, C / x, 1])
            x -= 1 / cfg.SCALE / 10

    figureList[2] = findPointStrokes()


def draw_lines(field):
    step = cfg.STEP
    zone_points = figureList[2]
    min_b, max_b = None, None

    for pts in zone_points:
        b = pts[1] - cfg.INCLINE * pts[0]

        if not min_b or b < min_b:
            min_pts = pts
            min_b = b

        if not max_b or b > max_b:
            max_b = b
            max_pts = pts

    c = (max_pts[1] - min_pts[1]) / (max_pts[0] - min_pts[0])

    half_b = max_pts[1] - c * max_pts[0]
    # p1 = translate_to_comp([-1000, c * -1000 + half_b, 1])
    # p2 = translate_to_comp([1000, c * 1000 + half_b, 1])
    # field.create_line(p1.x, p1.y, p2.x, p2.y, fill="blue")

    z1, z2 = list(), list()
    for pts in zone_points:
        if pts[1] - c * pts[0] < half_b:
            z1.append(pts)
        else:
            z2.append(pts)

    z1.sort(key=lambda x: x[1] - cfg.INCLINE * x[0])
    z2.sort(key=lambda x: x[1] - cfg.INCLINE * x[0])

    cur_b = min_b

    while cur_b < max_b:
        draw_line(field, cur_b, z1, z2, cfg.INCLINE)
        cur_b += step


def draw_line(field, b, z1, z2, incline):
    points = list()

    i = 0
    while i < len(z1) - 1 and z1[i][1] - incline * z1[i][0] < b:
        i += 1
    points.append(translate_to_computer_system(z1[i]))

    i = 0
    while i < len(z2) - 1 and z2[i][1] - incline * z2[i][0] < b:
        i += 1
    points.append(translate_to_computer_system(z2[i]))

    field.create_line(points[0].x, points[0].y, points[1].x, points[1].y, width=cfg.LINE_WIDTH,
                      fill="red")


def drawFigure(field):
    for k in range(len(figureList) - 1):
        p1 = translate_to_computer_system(figureList[k][0])

        # # "Дорисовка" окружности
        # if k == 0:
        #     p2 = translate_to_computer_system(figureList[k][-1])
        #     field.create_line(p1.x, p1.y, p2.x, p2.y, fill="green", width=cfg.LINE_WIDTH)

        for i in range(1, len(figureList[k])):
            p2 = translate_to_computer_system(figureList[k][i])
            field.create_line(p1.x, p1.y, p2.x, p2.y, fill="green", width=2.5)
            p1 = p2

        if figureList[2]:
            draw_lines(field)


def drawAxis(field):
    p1 = translate_to_computer_system([cfg.MIN_LIMIT_X, 0])
    p2 = translate_to_computer_system([cfg.MAX_LIMIT_X, 0])
    field.create_line(p1.x, p1.y, p2.x, p2.y, fill="black", arrow=tk.LAST, width=cfg.LINE_WIDTH)
    p1 = translate_to_computer_system([0, cfg.MIN_LIMIT_Y])
    p2 = translate_to_computer_system([0, cfg.MAX_LIMIT_Y])
    field.create_line(p1.x, p1.y, p2.x, p2.y, fill="black", arrow=tk.LAST, width=cfg.LINE_WIDTH)
    for i in range(int(cfg.MIN_LIMIT_Y * 3), int(cfg.MAX_LIMIT_Y * 3)):
        p1 = translate_to_computer_system([cfg.MIN_LIMIT_X, i / 3])
        p2 = translate_to_computer_system([cfg.MAX_LIMIT_X, i / 3])
        if i % 1 == 0:
            field.create_text(cfg.FIELD_WIDTH // 2 - 15, p1.y + 10, text=str(round(i / 3, 2)))
        field.create_line(p1.x, p1.y, p2.x, p2.y, fill="blue", width=1)

    for i in range(int(cfg.MIN_LIMIT_X * 3), int(cfg.MAX_LIMIT_X * 3) ):
        if i != 0:
            p1 = translate_to_computer_system([i / 3, cfg.MIN_LIMIT_Y])
            p2 = translate_to_computer_system([i / 3, cfg.MAX_LIMIT_Y])
            field.create_text(p1.x - 15, cfg.FIELD_HEIGHT // 2 + 10, text=str(round(i / 3, 2)))
            field.create_line(p1.x, p1.y, p2.x, p2.y, fill="blue", width=1)


def apply_command(matrix):
    for q in range(len(figureList)):
        for i in range(len(figureList[q])):
            new_point = [0, 0, 0]
            for j in range(3):
                for k in range(3):
                    new_point[j] += figureList[q][i][k] * matrix[j][k]
            figureList[q][i] = new_point


def find_reversed_matrix(matrix):
    det = 0
    for i in range(3):
        det += matrix[0][i] * (matrix[1][(i + 1) % 3] * matrix[2][(i + 2) % 3] -
                               matrix[1][(i + 2) % 3] * matrix[2][(i + 1) % 3])

    new_matrix = [[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            new_matrix[j][i] = (matrix[(i + 1) % 3][(j + 1) % 3] *
                                  matrix[(i + 2) % 3][(j + 2) % 3] -
                                  matrix[(i + 2) % 3][(j + 1) % 3] *
                                  matrix[(i + 1) % 3][(j + 2) % 3]) / det
    return new_matrix


def mul_matrices(matrix1, matrix2):
    result_matrix = [[0 for i in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
    return result_matrix