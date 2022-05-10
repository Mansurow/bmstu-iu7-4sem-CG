from algrorithm import Point

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