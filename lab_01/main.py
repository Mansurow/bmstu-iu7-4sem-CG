"""
На плоскости дано множество точек.
Найти такой треугольник с вершинами в этих точках,
у которого угол, образованный медианой и биссектрисой
исходящими из одно вершины, минимален
"""
from tkinter import Tk, Canvas, Label, Entry, Button, messagebox, LAST, Listbox
from triangle import *

window = Tk()
WINDOW_WIDTH = window.winfo_screenwidth()
WINDOW_HEIGHT = window.winfo_screenheight() - 70
AXIS_SPACE = 10

CANVAS_X = WINDOW_WIDTH
CANVAS_Y = WINDOW_HEIGHT - 120

numb_points = 0

point_list = []


def translate_to_normal_system(x, y):
    return transform_origin_x(x), transform_origin_y(y)


def transform_origin_x(x):
    return x * (x_max - x_min) / CANVAS_X + x_min


def transform_origin_y(y):
    return -(y * (y_max - y_min) / CANVAS_Y - y_max)


def translate_to_own_system(x, y):
    return transform_x(x), transform_y(y)


def transform_x(x):
    return (x - x_min) / (x_max - x_min) * CANVAS_X


def transform_y(y):
    return (y_max - y) / (y_max - y_min) * CANVAS_Y


def point_not_enter():
    messagebox.showwarning("Предупреждение!",
                           "Координаты точки не введены!")


def number_not_enter():
    messagebox.showwarning("Предупреждение!",
                           "Введите номер удаляемой точки!")


def point_not_exist():
    messagebox.showwarning("Предупреждение!",
                           "Под такой нумерации точки нет!")


def point_exist():
    messagebox.showwarning("Предупреждение!",
                           "Такая точка уже введена!")


def task():
    messagebox.showinfo("Условие задачи",
                        " На плоскости дано множество точек.\n"
                        " Найти такой треугольник с вершинами в этих точках,\n"
                        " у которого угол, образованный медианой и биссектрисой\n"
                        " исходящими из одно вершины, минимален.")


def clear_canvas_field():
    global numb_points
    global flag_find_triangle, corner_bisector_median

    canvas.delete("all")
    clear_fields(del_point_txt)
    clear_fields(x_point_txt)
    clear_fields(y_point_txt)
    draw_axis()
    point_list.clear()
    numb_points = 0
    scroll_menu.delete(0, scroll_menu.size() - 1)
    flag_find_triangle = False
    corner_bisector_median = 400.0


def clear_fields(field):
    string = field.get()
    len_str = len(string)

    while len_str >= 1:
        field.delete(len_str - 1)
        len_str -= 1


def draw_axis():
    for i in range(0, CANVAS_Y, 50):
        canvas.create_line(7, CANVAS_Y - i - AXIS_SPACE, 13, CANVAS_Y - i - AXIS_SPACE, width=2)
        if i != 0:
            canvas.create_text(25, CANVAS_Y - i - AXIS_SPACE, text=str(round(transform_origin_y(CANVAS_Y - i - AXIS_SPACE), 2)))

    for i in range(0, CANVAS_X, 50):
        canvas.create_line(i + AXIS_SPACE, CANVAS_Y - 13, i + AXIS_SPACE, CANVAS_Y - 7, width=2)
        if i != 0:
            canvas.create_text(i + AXIS_SPACE, CANVAS_Y - AXIS_SPACE - 10, text=round(transform_origin_x(i + AXIS_SPACE), 2))

    canvas.create_line(0, CANVAS_Y - AXIS_SPACE, CANVAS_X, CANVAS_Y - AXIS_SPACE, width=2, arrow=LAST)
    canvas.create_line(AXIS_SPACE, CANVAS_Y, AXIS_SPACE, 0, width=2, arrow=LAST)


def add_point():
    global numb_points

    x_text = x_point_txt.get()
    y_text = y_point_txt.get()

    if x_text == "" or y_text == "":
        point_not_enter()
    else:
        try:
            x, y = float(x_text), float(y_text)
            flag = False
            for p in point_list:
                flag = p.equalpoint(x, y)
                if flag:
                    break

            if point_list == [] or (not flag):
                point_list.append(Point(x, y))

                scroll_menu.insert(numb_points, str(numb_points + 1) + ".(" + str(round(x, 2)) + ";" + str(round(y, 2)) + ")")

                numb_points += 1

                draw_point(x, y, numb_points, color_points_add)

                clear_fields(del_point_txt)

                del_point_txt.insert(0, numb_points)
            else:
                point_exist()
        except:
            messagebox.showwarning("Предупреждение!",
                                   "Введены недопустимые символы")
        clear_fields(x_point_txt)
        clear_fields(y_point_txt)


def del_point():
    global numb_points, corner_bisector_median, flag_find_triangle, corner_bisector_median

    del_text = del_point_txt.get()
    if del_text == '':
        number_not_enter()
    else:
        index_del = int(del_text) - 1
        if index_del >= len(point_list) or index_del < 0:
            point_not_exist()
        elif numb_points != 0:
            canvas.delete("all")
            draw_axis()

            point_list.pop(index_del)

            for i in range(0, len(point_list)):
                draw_point(point_list[i].x, point_list[i].y, i + 1, color_points_add)

            scroll_menu.delete(index_del)
            clear_fields(del_point_txt)
            numb_points -= 1
            if numb_points != 0:
                del_point_txt.insert(0, numb_points)

            if index_del == numb_points:
                scroll_menu.delete(index_del)
            else:
                scroll_menu.delete(index_del, scroll_menu.size() - 1)
                for i in range(index_del, len(point_list)):
                    x, y = point_list[i].x, point_list[i].y
                    scroll_menu.insert(i, str(i + 1) + ".(" + str(round(x, 3)) + ";" + str(round(y, 3)) + ")")

            flag_find_triangle = False
            corner_bisector_median = 400.0


def draw_point(x, y, name, color):
    xp, yp = transform_x(x), transform_y(y)
    coor = str(name) + ".(" + str(round(x, 2)) + ";" + str(round(y, 2)) + ")"
    canvas.create_oval(xp - 2, yp - 2, xp + 2, yp + 2, fill=color, outline=color, width=2)
    canvas.create_text(xp + 5, yp - 10, text=coor, fill=color, font=("Courier New", 10))


def draw_line(x1, y1, x2, y2, color):
    x1, y1 = translate_to_own_system(x1, y1)
    x2, y2 = translate_to_own_system(x2, y2)
    canvas.create_line(x1, y1, x2, y2, width=2, fill=color)


def draw_triangle(pa, pb, pc):
    draw_line(pa.x, pa.y, pb.x, pb.y, colour_triangle)
    draw_line(pc.x, pc.y, pb.x, pb.y, colour_triangle)
    draw_line(pc.x, pc.y, pa.x, pa.y, colour_triangle)


def check_one_line():
    amount = len(point_list)
    for i in range(amount - 2):
        for j in range(i + 1, amount - 1):
            for k in range(j + 1, amount):
                if abs((point_list[k].x - point_list[i].x) * (point_list[j].y - point_list[i].y) - \
                       (point_list[j].x - point_list[i].x) * (point_list[k].y - point_list[i].y)) > EPS:
                    return CORRECT
    return MISTAKE


def find_triangle():
    global flag_find_triangle
    global coor_triangle, coor_start, coor_bisector, coor_median, coor_median, corner_bisector_median
    global x_min, x_max, y_min, y_max, x_c, y_c

    amount = len(point_list)
    if not point_list or numb_points < 3:
        messagebox.showwarning('Ошибка', 'Треугольник невозможно построить'
                                         '\nВведите три точки')
        return
    if check_one_line() == MISTAKE:
        messagebox.showwarning("Ошибка", "Все точки лежат на одной прямой\n(нельзя построить треугольник)")
        return

    if flag_find_triangle:

        canvas.delete("all")
        draw_axis()
        if point_list:
            for i in range(amount):
                draw_point(point_list[i].x, point_list[i].y, i + 1, color_points_add)
        flag_find_triangle = False

    for i in range(amount - 2):
        for j in range(i + 1, amount - 1):
            for k in range(j + 1, amount):

                pa = point_list[i]
                pb = point_list[j]
                pc = point_list[k]

                print("\n \n ------ Check Triangle ---------\n"
                      "pa = ", pa.x, pa.y,
                      "pb = ", pb.x, pb.y,
                      "pc = ", pc.x, pc.y, "\n")

                ab = length_side_triangle(pa, pb)
                ac = length_side_triangle(pa, pc)
                bc = length_side_triangle(pb, pc)

                print("----------Len Sides --------")
                print("ab = ", ab)
                print("bc = ", bc)
                print("ac = ", ac)

                if is_triangle(ab, ac, bc):
                    # corner_i = find_corner(ab, ac, bc)
                    # corner_j = find_corner(bc, ab, ac)
                    # corner_k = find_corner(ac, bc, ab)
                    # min_corner = min(corner_i, corner_j, corner_k)
                    print("------Vector - pa:")
                    pm_i, pn_i, angle_i = find_corner_between_bisector_median(pa, pb, pc)
                    print("angle_pa: ", angle_i)
                    print("------Vector - pb:")
                    pm_j, pn_j, angle_j = find_corner_between_bisector_median(pb, pa, pc)
                    print("angle_pb: ", angle_j)
                    print("------Vector - pc:")
                    pm_k, pn_k, angle_k = find_corner_between_bisector_median(pc, pb, pa)
                    print("angle_pc: ", angle_k)
                    min_angle = min(angle_i, angle_j, angle_k)

                    if corner_bisector_median > min_angle:
                        coor_triangle[0] = pa
                        coor_triangle[1] = pb
                        coor_triangle[2] = pc
                        corner_bisector_median = min_angle

                        if abs(angle_i - min_angle) < EPS:
                            coor_start = pa
                            coor_bisector = pm_i
                            coor_median = pn_i
                        if abs(angle_j - min_angle) < EPS:
                            coor_start = pb
                            coor_bisector = pm_j
                            coor_median = pn_j
                        if abs(angle_k - min_angle) < EPS:
                            coor_start = pc
                            coor_bisector = pm_k
                            coor_median = pn_k

                    print("min_angle in this triangle: ", corner_bisector_median)
    print(coor_triangle)
    print(coor_bisector, coor_median)

    x_max = max(coor_triangle[0].x, coor_triangle[1].x, coor_triangle[2].x, coor_bisector.x, coor_median.x)
    y_max = max(coor_triangle[0].y, coor_triangle[1].y, coor_triangle[2].y, coor_bisector.y, coor_median.y)

    x_min = min(coor_triangle[0].x, coor_triangle[1].x, coor_triangle[2].x, coor_bisector.x, coor_median.x)
    y_min = min(coor_triangle[0].y, coor_triangle[1].y, coor_triangle[2].y, coor_bisector.y, coor_median.y)

    # Отступ от краеё поля графика
    x_c = (x_min + x_max) / 2
    x_min = x_c - (x_c - x_min) * (kx_space + x_max / CANVAS_X + 0.1)
    x_max = x_c + (x_max - x_c) * (kx_space + x_max / CANVAS_X + 0.1)

    y_c = (y_min + y_max) / 2
    y_min = y_c - (y_c - y_min) * (ky_space + y_max / CANVAS_Y + 0.1)
    y_max = y_c + (y_max - y_c) * (ky_space + y_max / CANVAS_Y + 0.1)

    # Коэффициенты доли в экране
    kx = (x_max - x_min) / CANVAS_X
    ky = (y_max - y_min) / CANVAS_Y

    if kx < ky:
        # Координаты центра растяжения
        x_c = (x_min + x_max) / 2
        x_min = x_c - (x_c - x_min) * (ky / kx)
        x_max = x_c + (x_max - x_c) * (ky / kx)
    else:
        # Координаты центра растяжения
        y_c = (y_min + y_max) / 2
        y_min = y_c - (y_c - y_min) * (kx / ky)
        y_max = y_c + (y_max - y_c) * (kx / ky)

    canvas.delete("all")
    draw_axis()
    for i in range(amount):
        draw_point(point_list[i].x, point_list[i].y, str(i + 1), color_points_add)

    draw_result()

    if not flag_find_triangle:
        flag_find_triangle = True


def draw_result():
    draw_triangle(coor_triangle[0], coor_triangle[1], coor_triangle[2])
    draw_line(coor_start.x, coor_start.y, coor_bisector.x, coor_bisector.y, colour_bisector)
    draw_line(coor_start.x, coor_start.y, coor_median.x, coor_median.y, colour_median)

    if abs(coor_bisector.x - coor_median.x) < 0.001 and abs(coor_bisector.y - coor_median.y) < 0.001:
        draw_point(coor_bisector.x, coor_bisector.y, "BM", "Crimson")
    else:
        draw_point(coor_bisector.x, coor_bisector.y, "B", colour_bisector)
        draw_point(coor_median.x, coor_median.y, "M", colour_median)


def get_result():
    if flag_find_triangle:
        messagebox.showinfo("Результат!",
                            "Треугольник состоит из точек с координатами:\n"
                            "1.( " + str(round(coor_triangle[0].x, 2)) + " ; " + str(round(coor_triangle[0].y, 2)) + " )\n"
                            "2.( " + str(round(coor_triangle[1].x, 2)) + " ; " + str(round(coor_triangle[1].y, 2)) + " )\n"
                            "3.( " + str(round(coor_triangle[2].x, 2)) + " ; " + str(round(coor_triangle[2].y, 2)) + " )\n"
                            "Наименьший угол между биссектрисой(синий) и медианы(красный): " + str(round(corner_bisector_median, 6)) + " градусов")
    else:
        messagebox.showinfo("Результатов нет!",
                            "Треугольник не построен!")


if __name__ == "__main__":
    CORRECT = 1
    MISTAKE = 0
    colour_triangle = "green"
    colour_bisector = "blue"
    colour_median = "red"
    color_points_add = "purple"
    kx_space = 1.01
    ky_space = 1.02

    x_max = 20
    x_min = 0
    y_max = 10
    y_min = 0

    x_c = (x_min + x_max) / 2
    x_min = x_c - (x_c - x_min) * kx_space
    x_max = x_c + (x_max - x_c) * kx_space

    y_c = (y_min + y_max) / 2
    y_min = y_c - (y_c - y_min) * ky_space
    y_max = y_c + (y_max - y_c) * ky_space

    coor_triangle = [Point(0, 0), Point(0, 0), Point(0, 0)]
    coor_start = Point(0, 0)
    coor_bisector = Point(0, 0)
    coor_median = Point(0, 0)
    corner_bisector_median = 400.0
    flag_find_triangle = False

    window.title("Лабораторная работа №1")
    window.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.resizable(False, False)

    canvas = Canvas(window, width=CANVAS_X, height=CANVAS_Y, bg="lightblue")
    canvas.place(x=0, y=120)

    draw_axis()

    Label(window, text="X: ", font=("Courier New", 18)). \
        place(width=60, height=40, x=10, y=15)

    x_point_txt = Entry(window, font=("Courier New", 15))
    x_point_txt.place(width=50, height=40, x=50, y=15)

    Label(window, text="Y: ", font=("Courier New", 18)). \
        place(width=60, height=40, x=100, y=15)

    y_point_txt = Entry(window, font=("Courier New", 15))
    y_point_txt.place(width=50, height=40, x=140, y=15)

    Button(text="Добавить точку", font=("Courier New", 12), command=add_point). \
        place(width=180, height=40, x=10, y=60)

    Label(window, text="№:", font=("Courier New", 15)). \
        place(height=50, x=200, y=15)

    del_point_txt = Entry(window, font=("Courier New", 15))
    del_point_txt.place(width=150, height=40, x=230, y=15)

    Button(text="Удалить точку", font=("Courier New", 12), command=del_point). \
        place(width=180, height=40, x=200, y=60)

    Button(text="Условие задачи", font=("Courier New", 12), command=task). \
        place(width=180, height=40, x=390, y=15)

    Button(text="Очистить все поля", font=("Courier New", 12), command=clear_canvas_field). \
        place(width=180, height=40, x=580, y=15)

    Button(text="Построить треуг-к", font=("Courier New", 12), command=find_triangle). \
        place(width=180, height=40, x=390, y=60)

    Button(text="Вывести результаты", font=("Courier New", 11), command=get_result). \
        place(width=180, height=40, x=580, y=60)

    Label(window, text="Cписок всех точек:", font=("Courier New", 12)). \
        place(width=180, height=50, x=800, y=35)
    scroll_menu = Listbox()
    scroll_menu.place(width=180, height=100, x=1000, y=15)

    window.mainloop()
