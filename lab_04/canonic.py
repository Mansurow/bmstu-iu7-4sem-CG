from draw_pixel import draw_simetric_pixels, set_pixel
import math as m


# (x - xc) ** 2 + (y - yc) ** 2 = R**2
# f(x, y) = (x - xc) ** 2 + (y - yc) ** 2 - R**2
# y = yc + sqrt(R**2 - (x - xc)**2)
# x = xc + sqrt(R**2 - (y - yc)**2)
def canonical_сircle(canvas, xc, yc, r, colour, draw):
    sqr_r = r ** 2

    border = round(xc + r / m.sqrt(2))

    for x in range(xc, border + 1):
        y = yc + m.sqrt(sqr_r - (x - xc) ** 2)
        if draw:
            # print(x, y, y - yc)
            # set_pixel(canvas, x, y, color)
            draw_simetric_pixels(canvas, [x, y, colour], xc, yc, circle=True)


def canonical_ellipse(canvas, xc, yc, ra, rb, colour, draw):
    sqr_ra = ra * ra
    sqr_rb = rb * rb

    border_x = round(xc + ra / m.sqrt(1 + sqr_rb / sqr_ra))
    border_y = round(yc + rb / m.sqrt(1 + sqr_ra / sqr_rb))

    for x in range(round(xc), border_x + 1):
        y = yc + m.sqrt(sqr_ra * sqr_rb - (x - xc) ** 2 * sqr_rb) / ra

        if draw:
            # set_pixel(canvas, x, y, color)
            draw_simetric_pixels(canvas, [x, y, colour], xc, yc, circle=False)

    for y in range(border_y, round(yc) - 1, -1):
        x = xc + m.sqrt(sqr_ra * sqr_rb - (y - yc) ** 2 * sqr_ra) / rb

        if draw:
            # set_pixel(canvas, x, y, color)
            draw_simetric_pixels(canvas, [x, y, colour], xc, yc, circle=False)