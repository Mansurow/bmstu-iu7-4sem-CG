def set_pixel(canvas, x, y, color):
    canvas.create_line(x, y, x + 1, y, fill=color, width=1)
    # canvas.create_oval(x, y, x, y, outline=color, width=1)


def draw_pixels(canvas, dot, xc, yc, circle=True):
    if circle:
        set_pixel(canvas,  dot[1] - yc + xc,  dot[0] - xc + yc, dot[2])
        set_pixel(canvas, -dot[1] + yc + xc,  dot[0] - xc + yc, dot[2])
        set_pixel(canvas,  dot[1] - yc + xc, -dot[0] + xc + yc, dot[2])
        set_pixel(canvas, -dot[1] + yc + xc, -dot[0] + xc + yc, dot[2])

    set_pixel(canvas,  dot[0],           dot[1],          dot[2])
    set_pixel(canvas, -dot[0] + 2 * xc,  dot[1],          dot[2])
    set_pixel(canvas,  dot[0],          -dot[1] + 2 * yc, dot[2])
    set_pixel(canvas, -dot[0] + 2 * xc, -dot[1] + 2 * yc, dot[2])