from config import CANVAS_COLOUR
from methodfunctions import sign, get_rgb_intensity


def BrezenhemFloat(x1, y1, x2, y2, colour='black', stepmode=False):
    pointsList = []

    if x1 == x2 and y1 == y2:
        pointsList.append([x1, y1, colour])
    else:
        dx = x2 - x1
        dy = y2 - y1

        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        if dy > dx:
            dx, dy = dy, dx
            exchange = 1
        else:
            exchange = 0

        tg = dy / dx
        e = tg - 0.5
        x = x1
        y = y1

        xb = x1
        yb = y1
        steps = 0

        # i <= dx i = 0
        # for i in range(0, dx + 1):
        # i = 0
        # while i <= dx:
        while x != x2 or y != y2:

            if not stepmode:
                pointsList.append([x, y, colour])

            if e >= 0:
                if exchange == 1:
                    x += sx
                else:
                    y += sy
                e -= 1

            if e <= 0:
                if exchange == 0:
                    x += sx
                else:
                    y += sy
                e += tg

            if stepmode:
                if xb != x and yb != y:
                    steps += 1
                xb = x
                yb = y

        if stepmode:
            return steps
    return pointsList


def BrezenhemInteger(x1, y1, x2, y2, colour='black', stepmode=False):
    pointsList = []
    if x1 == x2 and y1 == y2:
        pointsList.append([x1, y1, colour])
    else:
        dx = x2 - x1
        dy = y2 - y1

        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        if dy > dx:
            dx, dy = dy, dx
            exchange = 1
        else:
            exchange = 0

        e = 2 * dy - dx
        x = x1
        y = y1

        xb = x
        yb = y
        steps = 0

        # i <= dx i = 0
        # for i in range(0, dx + 1):
        # i = 0
        # while i <= dx:
        while x != x2 or y != y2:
            if stepmode == False:
                pointsList.append([x, y, colour])

            if e >= 0:
                if exchange == 1:
                    x += sx
                else:
                    y += sy
                e -= 2 * dx  # отличие от вещественного (e -= 1)
            if e <= 0:
                if exchange == 0:
                    x += sx
                else:
                    y += sy
                e += 2 * dy  # difference (e += tg)

            if stepmode:
                if xb != x and yb != y:
                    steps += 1
                xb = x
                yb = y

        if stepmode:
            return steps
    return pointsList


def BrezenhemSmooth(canvas, x1, y1, x2, y2, fill='black', stepmode=False):
    pointsList = []
    I = 100
    fill = get_rgb_intensity(canvas, fill, CANVAS_COLOUR, I)
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        steep = 1  #
    else:
        steep = 0  #
    tg = dy / dx * I  # тангенс угла наклона (умножаем на инт., чтобы не приходилось умножать внутри цикла
    e = I / 2  # интенсивность для высвечивания начального пикселя
    w = I - tg  # пороговое значение
    x = x1
    y = y1

    xb = x
    yb = y
    steps = 0

    # i <= dx i = 0
    # for i in range(0, dx + 1):
    # i = 0
    # while i <= dx:
    while x != x2 or y != y2:
        if not stepmode:
            pointsList.append([x, y, fill[round(e) - 1]])
        # canvas.create_oval(x, y, x, y, outline=fill[round(e) - 1])
        if e < w:
            if steep == 0:  # dy < dx
                x += sx     # -1 if dx < 0, 0 if dx = 0, 1 if dx > 0
            else:           # dy >= dx
                y += sy     # -1 if dy < 0, 0 if dy = 0, 1 if dy > 0
            e += tg
        elif e >= w:
            x += sx
            y += sy
            e -= w

        if stepmode:
            if xb != x and yb != y:
                steps += 1
            xb = x
            yb = y

    if stepmode:
        return steps
    return pointsList