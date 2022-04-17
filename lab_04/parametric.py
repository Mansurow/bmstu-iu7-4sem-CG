from draw_pixel import draw_simetric_pixels, set_pixel
import math as m


# 1/8 часть
# { x = xc + r * cos(t)
# { y = yc + r * sin(t)
# f = (x - xc)**2 + (y - yc)**2 + r**2
# f = (r * cos(t)) ** 2 + (r ** sin(t))**2 + r**2
def parameter_circle(canvas, xc, yc, r, colour, draw):
    step = 1 / r

    i = 0
    while i <= m.pi / 4 + step:
        x = xc + r * m.cos(i)
        y = yc + r * m.sin(i)

        if draw:
            # set_pixel(canvas, x, y, color)
            draw_simetric_pixels(canvas, [x, y, colour], xc, yc, circle=True)

        i += step


# 1/4 часть
# { x = xc + ra * cos(t)
# { y = yc + rb * sin(t)
# f = (x - xc)**2 * ra**2 + (y - yc)**2 ** rb**2 + ra**2 * rb**2
def parameter_ellipse(canvas, xc, yc, ra, rb, colour, draw):
    if ra > rb:
        step = 1 / ra
    else:
        step = 1 / rb

    i = 0
    while i <= m.pi / 2 + step:
        x = xc + round(ra * m.cos(i))
        y = yc + round(rb * m.sin(i))

        if draw:
            draw_simetric_pixels(canvas, [x, y, colour], xc, yc, circle=False)

        i += step