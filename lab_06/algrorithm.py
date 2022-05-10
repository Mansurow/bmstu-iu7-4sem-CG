from dataclasses import dataclass
from config import *

@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def draw_pixel(img, x, y, colour):
    img.put(colour, (x, y))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def rgb(color):
    return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))

def line_by_line_filling_algorithm_with_seed \
    (canvas, img, border_colour, fill_colour, seed_point, delay=False):

    fill_colour_rgb = rgb(fill_colour)
    border_colour_rgb = rgb(border_colour)

    print("fill_c = ", fill_colour, fill_colour_rgb)
    print("border_c = ", border_colour, border_colour_rgb)

    stack = [seed_point]
    while stack:

        seed_pixel = stack.pop()
        x = seed_pixel.x
        y = seed_pixel.y

        draw_pixel(img, x, y, fill_colour)
        tx = x
        ty = y

        # заполняем интервал справа от затравки

        x += 1

        while img.get(x, y) != fill_colour_rgb and \
              img.get(x, y) != border_colour_rgb and x < CANVAS_WIDTH:
            draw_pixel(img, x, y, fill_colour)
            x += 1

        xr = x - 1

        # заполняем интервал слева от затравки

        x = tx - 1
        while img.get(x, y) != fill_colour_rgb and \
              img.get(x, y) != border_colour_rgb and x > 0:
            draw_pixel(img, x, y, fill_colour)
            x -= 1

        xl = x + 1

        # Проход по верхней строке

        x = xl
        if ty < CANVAS_HEIGHT:
            y = ty + 1

            while x <= xr:
                flag = False

                while img.get(x, y) != fill_colour_rgb and \
                      img.get(x, y) != border_colour_rgb and x <= xr:
                    flag = True
                    x += 1

                # Помещаем в стек крайний справа пиксель

                if flag:
                    if x == xr and img.get(x, y) != fill_colour_rgb and \
                                   img.get(x, y) != border_colour_rgb:
                        if y < CANVAS_HEIGHT:
                            stack.append(Point(x, y))
                    else:
                        if y < CANVAS_HEIGHT:
                            stack.append(Point(x - 1, y))

                    flag = False

                # Продолжаем проверку, если интервал был прерван

                x_in = x
                while (img.get(x, y) == fill_colour_rgb or
                       img.get(x, y) == border_colour_rgb) and x < xr:
                    x = x + 1

                if x == x_in:
                    x += 1

        # Проход по нижней строке

        x = xl
        y = ty - 1

        while x <= xr:
            flag = False

            while img.get(x, y) != fill_colour_rgb and \
                  img.get(x, y) != border_colour_rgb and x <= xr:
                flag = True
                x += 1

            # Помещаем в стек крайний справа пиксель

            if flag:

                if x == xr and img.get(x, y) != fill_colour_rgb and \
                        img.get(x, y) != border_colour_rgb:
                    if y > 0:
                        stack.append(Point(x, y))
                else:
                    if y > 0:
                        stack.append(Point(x - 1, y))

                flag = False

            # Продолжаем проверку, если интервал был прерван

            x_in = x
            while (img.get(x, y) == fill_colour_rgb or
                   img.get(x, y) == border_colour_rgb) and x < xr:
                x = x + 1

            if x == x_in:
                x += 1

        if delay:
            canvas.update()