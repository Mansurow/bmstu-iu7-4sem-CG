from algrorithm import Point

def add_simetric_pixels(points, dot, xc, yc, circle=True):
    if circle:
        points.append(Point( dot[1] - yc + xc,  dot[0] - xc + yc))
        points.append(Point(-dot[1] + yc + xc,  dot[0] - xc + yc))
        points.append(Point( dot[1] - yc + xc, -dot[0] + xc + yc))
        points.append(Point(-dot[1] + yc + xc, -dot[0] + xc + yc))

    points.append(Point( dot[0],           dot[1]))
    points.append(Point(-dot[0] + 2 * xc,  dot[1]))
    points.append(Point( dot[0],          -dot[1] + 2 * yc))
    points.append(Point(-dot[0] + 2 * xc, -dot[1] + 2 * yc))

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def bresenhem_int(beg_point, end_point):
    dx = end_point.x - beg_point.x
    dy = end_point.y - beg_point.y

    if dx == 0 and dy == 0:
        return [Point(beg_point.x, beg_point.y)]

    x_sign = sign(dx)
    y_sign = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        exchange = 1
    else:
        exchange = 0

    two_dy = 2 * dy
    two_dx = 2 * dx

    e = two_dy - dx

    x = beg_point.x
    y = beg_point.y
    points = []

    i = 0
    while i <= dx:
        points.append(Point(x, y))

        if e >= 0:
            if exchange == 1:
                x += x_sign
            else:
                y += y_sign

            e -= two_dx

        if exchange == 1:
            y += y_sign
        else:
            x += x_sign

        e += two_dy
        i += 1

    return points

def bresenham_circle(xc, yc, r):
    x = 0
    y = r

    points = list()
    add_simetric_pixels(points, [x + xc, y + yc], xc, yc, circle=True)

    delta = 2 * (1 - r)

    while y >= x:
        d = 2 * (delta + y) - 1
        x += 1

        if d >= 0:
            y -= 1
            delta += 2 * (x - y + 1)
        else:
            delta += x + x + 1

        add_simetric_pixels(points, [x + xc, y + yc], xc, yc, circle=True)

    return points

def bresenham_ellipse(xc, yc, ra, rb):
    x = 0
    y = rb

    points = list()

    add_simetric_pixels(points, [x + xc, y + yc], xc, yc, circle=False)

    sqr_ra = ra * ra
    sqr_rb = rb * rb
    delta = sqr_rb - sqr_ra * (2 * rb + 1)

    while y >= 0:

        if delta < 0:
            d1 = 2 * delta + sqr_ra * (2 * y + 2)

            x += 1
            if d1 < 0:
                delta += sqr_rb * (2 * x + 1)
            else:
                y -= 1
                delta += sqr_rb * (2 * x + 1) + sqr_ra * (1 - 2 * y)
        elif delta > 0:
            d2 = 2 * delta + sqr_rb * (2 - 2 * x)

            y -= 1
            if d2 > 0:
                delta += sqr_ra * (1 - 2 * y)
            else:
                x += 1
                delta += sqr_rb * (2 * x + 1) + sqr_ra * (1 - 2 * y)
        else:
            y -= 1
            x += 1
            delta += sqr_rb * (2 * x + 1) + sqr_ra * (1 - 2 * y)

        add_simetric_pixels(points, [x + xc, y + yc], xc, yc, circle=False)

    return points