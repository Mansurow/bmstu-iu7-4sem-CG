from draw import draw_pixels, set_pixel


# 1/4 часть
def bresenham_circle_quadrant(xc, yc, r, color, canvas, draw):
    x = 0
    y = r

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)

    delta = 2 * (1 - r)

    while y >= 0:
        if delta < 0:
            d1 = 2 * delta + 2 * y - 1
            if d1 <= 0:
                x += 1
                delta += 2 * x + 1
            elif d1 > 0:
                x += 1
                y -= 1
                delta += 2 * (x - y + 1)
        elif delta > 0:
            d2 = 2 * delta - 2 * x - 1
            if d2 <= 0:
                x += 1
                y -= 1
                delta += 2 * (x - y + 1)
            elif d2 > 0:
                y -= 1
                delta -= 2 * y + 1
        else:
            x += 1
            y -= 1
            delta += 2 * (x - y + 1)

        if draw:
            # set_pixel(canvas, x + xc, y + yc, color)
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle = True)


# 1/8
def bresenham_circle_octant(xc, yc, r, color, canvas, draw):
    x = 0
    y = r

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)

    delta = 2 * (1 - r)

    while y >= x:
        d1 = 2 * (delta + y) - 1

        x += 1                        # так у обоих шагов увеличивается x, то можно вынести
        if d1 >= 0:
            y -= 1
            delta += 2 * (x - y + 1)  # диагональный шаг
        else:
            delta += 2 * x + 1        # горизонтальный шаг

        if draw:
            # set_pixel(canvas, x + xc, y + yc, color)
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)


def bresenham_ellipse(xc, yc, ra, rb, color, canvas, draw):
    x = 0
    y = rb

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)

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

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle = False)