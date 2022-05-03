from dataclasses import dataclass
import time
from config import *

@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

@dataclass
class Node:
    x: float
    dx: float
    dy: int

    def __init__(self, x=0, dx=0, dy=0):
        self.x = x
        self.dx = dx
        self.dy = dy


def draw_line(canvas, ps, pe, colour):
    x_beg = ps.x + 0.5
    x_end = pe.x + 0.5
    y = ps.y
    canvas.create_line(x_beg, y, x_end, y, fill=colour)


def draw_edges(canvas, edges):
    for i in range(len(edges)):
        canvas.create_line(edges[i][0].x, edges[i][0].y,
                           edges[i][1].x, edges[i][1].y, fill="black")


# figures - полигон фигур или массив всех замкнутых фигур
def make_edges_list(figures):
    edges = list()
    for fig in figures:
        amount_point = len(fig)
        for i in range(amount_point):
            if i + 1 > amount_point - 1:
                edges.append([fig[-1], fig[0]])
            else:
                edges.append([fig[i], fig[i + 1]])

    return edges


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def find_extrimum_Y_figures(figures):
    yMin = figures[0][0].y
    yMax = figures[0][0].y
    for fig in figures:
        for p in fig:
            if p.y > yMax:
                yMax = p.y
            if p.y < yMin:
                yMin = p.y
    return yMin, yMax

# first_method without y-group and CAP
# ------------------------------------------------


def bubble_sort_y(pointList):
    for i in range(len(pointList)):
        for j in range(i + 1, len(pointList)):
            if pointList[i].y < pointList[j].y:
                pointList[i], pointList[j] = pointList[j], pointList[i]


def sort_x_in_y(pointList):
    for i in range(len(pointList)):
        for j in range(i + 1, len(pointList)):
            if pointList[i].x > pointList[j].x and pointList[i].y == pointList[j].y:
                pointList[i], pointList[j] = pointList[j], pointList[i]


def simple_algorithm_with_ordered_list_of_edges(canvas, polygon, colour, delay=False):
    edges = make_edges_list(polygon)
    # print("Все рёбра всех фигур: ")
    # for edge in edges:
    #     print(edge)
    # print("----------------------")

    ins = dda_find_insertion(edges)
    ins.sort(key=lambda point: point.y, reverse=True)
    sort_x_in_y(ins)

    for i in range(0, len(ins), 2):
        draw_line(canvas, ins[i], ins[i + 1], colour)
        if delay:
            time.sleep(0.00001)
            canvas.update()
    draw_edges(canvas, edges)


def dda_find_insertion(edges):
    intersections = []
    for edge in edges:
        x1 = edge[0].x
        y1 = edge[0].y
        x2 = edge[1].x
        y2 = edge[1].y

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_y != 0:
            dx = ((x2 > x1) - (x2 < x1)) * len_x / len_y
            dy = ((y2 > y1) - (y2 < y1))

            x1 += dx / 2
            y1 += dy / 2

            for j in range(len_y):
                # print(i, x1, y1, end ='\n')
                intersections.append(Point(x1, y1))
                x1 += dx
                y1 += dy

    return intersections


# second_method with y-group
# ------------------------------------------------
def make_y_groups(Ymin=0, Ymax=CANVAS_HEIGHT):
    y_group = dict()
    for i in range(round(Ymax), round(Ymin), -1):
        y_group.update({i - 0.5: list()})
    return y_group


def dda_update_y_group(edges, y_groups):
    for edge in edges:
        x1 = edge[0].x
        y1 = edge[0].y
        x2 = edge[1].x
        y2 = edge[1].y

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_y != 0:
            dx = ((x2 > x1) - (x2 < x1)) * len_x / len_y
            dy = ((y2 > y1) - (y2 < y1))

            x1 += dx / 2
            y1 += dy / 2

            for j in range(len_y):
                # print(i, x1, y1, end ='\n')
                sotYdr = y_groups.get(y1)
                sotYdr.append(x1)
                x1 += dx
                y1 += dy


def draw_all_ygroups(canvas, y_groups, colour, delay=False):
    for yValue in y_groups:
        draw_Y_group(canvas, yValue, y_groups.get(yValue), colour)
        if delay:
            time.sleep(0.0001)
            canvas.update()


def draw_Y_group(canvas, y, y_group, colour):
    for i in range(0, len(y_group), 2):
        canvas.create_line(y_group[i] + 0.5, y, y_group[i + 1] + 0.5, y, fill=colour)


def y_group_algorithm_with_ordered_list_of_edges(canvas, polygon, colour="black", delay=False):
    edges = make_edges_list(polygon)
    print("Все рёбра всех фигур: ")
    for edge in edges:
        print(edge)

    ymin, ymax = find_extrimum_Y_figures(polygon)
    y_groups = make_y_groups(ymin, ymax)
    dda_update_y_group(edges, y_groups)

    for yValue in y_groups:
        y_group = y_groups.get(yValue)
        y_group.sort()

    print(y_groups)

    draw_all_ygroups(canvas, y_groups, colour, delay)
    draw_edges(canvas, edges)


# third_method with CAP - more fast than 1st and 2d
# ------------------------------------------------
def make_link_list(Ymin=0, Ymax=CANVAS_WIDTH):
    link_list = dict()
    for i in range(round(Ymax), round(Ymin), -1):
        link_list.update({i: list()})
    return link_list


def make_insert_thm(edges, link_list):
    for edge in edges:
        x1 = edge[0].x
        y1 = edge[0].y
        x2 = edge[1].x
        y2 = edge[1].y

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_y != 0:
            dx = ((x2 > x1) - (x2 < x1)) * len_x / len_y
            dy = ((y2 > y1) - (y2 < y1))

            nmax = max(y1, y2)

            x = x1 + dx / 2
            y = y2 + dy / 2

            for j in range(len_y):
                # print(i, x1, y1, end ='\n')
                sotYdr = link_list.get(nmax)
                sotYdr.append(Node(x1))
                x += dx
                y += dy


def update_y_group(y_groups, x_start, y_start, x_end, y_end):
        if y_start > y_end:
            x_end, x_start = x_start, x_end
            y_end, y_start = y_start, y_end

        # if y_end > y_max:
        #     self.y_max = y_end
        #
        # if y_start < y_min:
        #     self.y_min = y_start

        # y_proj = y_end - y_start if y_end - y_start else 1 // учитывает горизонтали
        y_proj = abs(y_end - y_start)
        if y_proj != 0:
            x_step = -(x_end - x_start) / y_proj
            if y_end not in y_groups:
                y_groups[y_end] = [Node(x_end, x_step, y_proj)]
            else:
                y_groups[y_end].append(Node(x_end, x_step, y_proj))
                # y_groups[y_end].extend([[x_end, x_step, y_proj]])


def iterator_active_edges(active_edges):
    i = 0
    while i < len(active_edges):
        active_edges[i].x += active_edges[i].dx
        active_edges[i].dy -= 1
        if active_edges[i].dy < 1:
            active_edges.pop(i) # удаляем как в стеке LIFO - размерность списка n x 4, бывают случаи когда нечетное в этом случае не учитвается
        else:
            i += 1


def add_active_edges(y_groups, active_edges, y):
    if y in y_groups:
        for y_group in y_groups.get(y):
            active_edges.append(y_group)
    active_edges.sort(key=lambda edge: edge.x)


def draw_act(canvas, active_edges, y, colour):
    len_edge = len(active_edges)
    #if len_edge % 2 != 0:
    #    len_edge -= 1
    for i in range(0, len_edge, 2):
        try:
            canvas.create_line(active_edges[i].x, y, active_edges[i + 1].x, y, fill=colour)
        except:
            canvas.create_line(active_edges[i].x, y, active_edges[i - 1].x, y, fill=colour)


def CAP_algorithm_with_ordered_list_of_edges(canvas, polygon, colour="black", delay=False):
    edges = make_edges_list(polygon)
    print("Все рёбра всех фигур: ")
    for edge in edges:
        print(edge)

    ymin, ymax = find_extrimum_Y_figures(polygon)
    y_groups = make_link_list(ymin, ymax)

    # hard test
    # edges = [[Point(x=205, y=356), Point(x=376, y=28)],
    #         [Point(x=376, y=28), Point(x=266, y=325)],
    #         [Point(x=266, y=325), Point(x=440, y=39)],
    #         [Point(x=440, y=39), Point(x=306, y=335)],
    #         [Point(x=306, y=335), Point(x=512, y=57)],
    #         [Point(x=512, y=57), Point(x=353, y=342)],
    #         [Point(x=353, y=342), Point(x=569, y=75)],
    #         [Point(x=569, y=75), Point(x=398, y=372)],
    #         [Point(x=398, y=372), Point(x=640, y=97)],
    #         [Point(x=640, y=97), Point(x=386, y=422)],
    #         [Point(x=386, y=422), Point(x=652, y=145)],
    #         [Point(x=652, y=145), Point(x=434, y=437)],
    #         [Point(x=434, y=437), Point(x=671, y=198)],
    #         [Point(x=671, y=198), Point(x=459, y=486)],
    #         [Point(x=459, y=486), Point(x=709, y=305)],
    #         [Point(x=709, y=305), Point(x=498, y=510)],
    #         [Point(x=498, y=510), Point(x=730, y=381)],
    #         [Point(x=730, y=381), Point(x=520, y=547)],
    #         [Point(x=520, y=547), Point(x=566, y=607)],
    #         [Point(x=566, y=607), Point(x=527, y=652)],
    #         [Point(x=527, y=652), Point(x=489, y=685)],
    #         [Point(x=489, y=685), Point(x=465, y=697)],
    #         [Point(x=465, y=697), Point(x=399, y=718)],
    #         [Point(x=399, y=718), Point(x=388, y=721)],
    #         [Point(x=388, y=721), Point(x=317, y=738)],
    #         [Point(x=317, y=738), Point(x=272, y=746)],
    #         [Point(x=272, y=746), Point(x=244, y=751)],
    #         [Point(x=244, y=751), Point(x=237, y=751)],
    #         [Point(x=237, y=751), Point(x=148, y=709)],
    #         [Point(x=148, y=709), Point(x=147, y=703)],
    #         [Point(x=147, y=703), Point(x=149, y=683)],
    #         [Point(x=149, y=683), Point(x=152, y=675)],
    #         [Point(x=152, y=675), Point(x=156, y=667)],
    #         [Point(x=156, y=667), Point(x=173, y=665)],
    #         [Point(x=173, y=665), Point(x=183, y=677)],
    #         [Point(x=183, y=677), Point(x=202, y=667)],
    #         [Point(x=202, y=667), Point(x=224, y=638)],
    #         [Point(x=224, y=638), Point(x=234, y=621)],
    #         [Point(x=234, y=621), Point(x=238, y=607)],
    #         [Point(x=238, y=607), Point(x=241, y=586)],
    #         [Point(x=241, y=586), Point(x=241, y=557)],
    #         [Point(x=241, y=557), Point(x=241, y=523)],
    #         [Point(x=241, y=523), Point(x=239, y=510)],
    #         [Point(x=239, y=510), Point(x=230, y=504)],
    #         [Point(x=230, y=504), Point(x=221, y=505)],
    #         [Point(x=221, y=505), Point(x=205, y=508)],
    #         [Point(x=205, y=508), Point(x=186, y=544)],
    #         [Point(x=186, y=544), Point(x=182, y=552)],
    #         [Point(x=182, y=552), Point(x=168, y=553)],
    #         [Point(x=168, y=553), Point(x=163, y=542)],
    #         [Point(x=163, y=542), Point(x=168, y=528)],
    #         [Point(x=168, y=528), Point(x=176, y=516)],
    #         [Point(x=176, y=516), Point(x=191, y=504)],
    #         [Point(x=191, y=504), Point(x=198, y=500)],
    #         [Point(x=198, y=500), Point(x=199, y=489)],
    #         [Point(x=199, y=489), Point(x=187, y=483)],
    #         [Point(x=187, y=483), Point(x=166, y=484)],
    #         [Point(x=166, y=484), Point(x=155, y=475)],
    #         [Point(x=155, y=475), Point(x=147, y=447)],
    #         [Point(x=147, y=447), Point(x=147, y=419)],
    #         [Point(x=147, y=419), Point(x=163, y=395)],
    #         [Point(x=163, y=395), Point(x=179, y=371)],
    #         [Point(x=179, y=371), Point(x=198, y=355)],
    #         [Point(x=198, y=355), Point(x=205, y=356)],
    #         [Point(x=161, y=90), Point(x=724, y=30)],
    #         [Point(x=724, y=30), Point(x=1135, y=226)],
    #         [Point(x=1135, y=226), Point(x=1286, y=344)],
    #         [Point(x=1286, y=344), Point(x=1193, y=549)],
    #         [Point(x=1193, y=549), Point(x=402, y=873)],
    #         [Point(x=402, y=873), Point(x=747, y=463)],
    #         [Point(x=747, y=463), Point(x=751, y=226)],
    #         [Point(x=751, y=226), Point(x=681, y=122)],
    #         [Point(x=681, y=122), Point(x=161, y=90)],
    #         [Point(x=64, y=119), Point(x=92, y=856)],
    #         [Point(x=92, y=856), Point(x=331, y=835)],
    #         [Point(x=331, y=835), Point(x=64, y=119)]]
    print("Все рёбра всех фигур: ")
    for edge in edges:
         print(edge)
        
    for edge in edges:
        update_y_group(y_groups, edge[0].x, edge[0].y, edge[1].x, edge[1].y)

    print(y_groups)

    y_end = ymax
    y_start = ymin
    active_edges = []
    while y_end > y_start:
        iterator_active_edges(active_edges)
        add_active_edges(y_groups, active_edges, y_end)

        print("Len egde:", len(active_edges))
        e = 1
        for i in active_edges:
            print("   ", e, ")", i)
            e += 1
        draw_act(canvas, active_edges, y_end, colour)
        y_end -= 1
        if delay:
            time.sleep(0.00001)
            canvas.update()
    draw_edges(canvas, edges)