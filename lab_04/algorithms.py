from bresenham import bresenham_circle_octant, bresenham_ellipse
from canonic import canonical_сircle, canonical_ellipse
from parametric import parameter_circle, parameter_ellipse
from midpoint import midpoint_circle, midpoint_ellipse


def standart_oval(canvas, xc, yc, ra, rb, colour):
    canvas.create_oval(xc - ra, yc - rb, xc + ra, yc + rb, outline=colour)


def spectrumBy_standart(canvas, xc, yc, ra, rb, step, count, colour):
    for e in range(0, count):
        standart_oval(canvas, xc, yc, ra, rb, colour)
        ra += step
        rb += step


def spectrumCircleBy_algorith(canvas, alg, xc, yc, rs, step, count, colour):
    for e in range(0, count):
        alg(canvas, xc, yc, rs, colour, True)
        rs += step


def spectrumEllipseBy_algorith(canvas, alg, xc, yc, ra, rb, step, count, colour):
    constant = ra / rb
    for e in range(0, count):
        alg(canvas, xc, yc, ra, rb, colour, True)
        ra += step
        rb = round(ra / constant)


def add_ellipse(canvas, algorithm, xc, yc, ra, rb, color, drawMode=True):
    try:
        alg = algorithm.get()
    except AttributeError:
        alg = algorithm

    if alg == 0:
        canonical_ellipse(canvas, xc, yc, ra, rb, color, drawMode)
    elif alg == 1:
        parameter_ellipse(canvas, xc, yc, ra, rb, color, drawMode)
    elif alg == 2:
        midpoint_ellipse(canvas, xc, yc, ra, rb, color, drawMode)
    elif alg == 3:
        bresenham_ellipse(canvas, xc, yc, ra, rb, color, drawMode)
    else:
        standart_oval(canvas, xc, yc, ra, rb, color)
        return


def add_circle(canvas, algorithm, xc, yc, r, color, drawMode=True):
    try:
        alg = algorithm.get()
    except AttributeError:
        alg = algorithm

    if alg == 0:
        canonical_сircle(canvas, xc, yc, r, color, drawMode)
    elif alg == 1:
        parameter_circle(canvas, xc, yc, r, color, drawMode)
    elif alg == 2:
        midpoint_circle(canvas, xc, yc, r, color, drawMode)
    elif alg == 3:
        bresenham_circle_octant(canvas, xc, yc, r, color, drawMode)
    else:
        standart_oval(canvas, xc, yc, r, r, color)
        return