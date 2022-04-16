import time
from math import radians
from methodfunctions import turn_point


def drawLineBy_StandartAlgorithm(canvas, x1, y1, x2, y2, colour):
    canvas.create_line(x1, y1, x2, y2, fill=colour)


def drawLineBy_algorithm(canvas, pointList):
    for point in pointList:
        canvas.create_line(point[0], point[1], point[0] + 1, point[1], fill=point[2])
        # canvas.create_oval(point[0], point[1], point[0], point[1], outline=point[2], width=1)


def drawSpecterBy_Method(canvas, method, x1, y1, x2, y2, angle, colour, draw=True, intensive=False):
    total = 0
    steps = int(360 // angle)
    for i in range(steps):
        if intensive:
            cur1 = time.time()
            pointsList = method(canvas, x1, y1, x2, y2, colour)
            cur2 = time.time()
        else:
            cur1 = time.time()
            pointsList = method(x1, y1, x2, y2, colour)
            cur2 = time.time()

        if draw:
            #print(pointsList)
            drawLineBy_algorithm(canvas, pointsList)

        x2, y2 = turn_point(radians(angle), x2, y2, x1, y1)
        total += cur2 - cur1

    return total / (steps - 2)


def drawSpecterBy_StardartMethod(canvas, x1, y1, x2, y2, angle, colour):
    steps = int(360 // angle)
    for i in range(steps):
        drawLineBy_StandartAlgorithm(canvas, x1, y1, x2, y2, colour)
        x2, y2 = turn_point(radians(angle), x2, y2, x1, y1)