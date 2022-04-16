from config import CANVAS_COLOUR
from methodfunctions import get_rgb_intensity
from math import floor


def VU(canvas, x1, y1, x2, y2, fill='black', stepmode=False):
    pointsList = []
    I = 100
    # stairs = []
    fills = get_rgb_intensity(canvas, fill, CANVAS_COLOUR, I)
    if x1 == x2 and y1 == y2:
        pointsList.append([x1, y1, fills[100]])
        # canvas.create_oval(x1, y1, x1, y1, outline=fills[100])

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        tg = 1
    else:
        tg = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + tg * (xend - x1)
    xpx1 = xend
    y = yend + tg

    # second endpoint
    xend = int(x2 + 0.5)
    xpx2 = xend

    steps = 0

    # main loop
    if steep:
        for x in range(xpx1, xpx2):
            try:
                pointsList.append([int(y), x + 1, fills[int((I - 1) * (abs(1 - y + int(y))))]])
            except:
                pointsList.append([int(y), x + 1, fill])
            pointsList.append([int(y) + 1, x + 1, fills[int((I - 1) * (abs(y - int(y))))]])
            # canvas.create_oval(int(y), x + 1, int(y), x + 1, outline=fills[int((I - 1) * (abs(1 - y + int(y))))])
            # canvas.create_oval(int(y) + 1, x + 1, int(y) + 1, x + 1, outline=fills[int((I - 1) * (abs(y - int(y))))])

            if x < round(x2) and int(y) != int(y + tg):
                steps += 1

            y += tg
    else:
        for x in range(xpx1, xpx2):
            pointsList.append([x + 1, int(y), fills[round((I - 1) * (abs(1 - y + floor(y))))]])
            pointsList.append([x + 1, int(y) + 1, fills[round((I - 1) * (abs(1 - y + floor(y))))]])
            # canvas.create_oval(x + 1, int(y), x + 1, int(y), outline=fills[round((I - 1) * (abs(1 - y + floor(y))))])
            # canvas.create_oval(x + 1, int(y) + 1, x + 1, int(y) + 1,
            #                    outline=fills[round((I - 1) * (abs(y - floor(y))))])

            if x < round(x2) and int(y) != int(y + tg):
                steps += 1

            y += tg
    if stepmode:
        return steps

    return pointsList