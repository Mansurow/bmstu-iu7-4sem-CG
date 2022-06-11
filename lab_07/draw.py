def draw_lines(canvas, lines):
    for line in lines:
        if len(line) == 3:
            canvas.create_line(line[0], line[1], fill = line[2])

def set_pixel(canvas, x, y, color):
    canvas.create_line(x, y, x + 1, y, fill = color)

def add_line(canvas, lines, xb, yb, xe, ye, linecolour):
    canvas.create_line([xb, yb], [xe, ye], fill=linecolour)

    lines.append([])
    lines[-1].append([xb, yb])
    lines[-1].append([xe, ye])
    lines[-1].append(linecolour)

def draw_rectangle(canvas, rectangle, lines, clippercolour):
    canvas.delete("all")
    draw_lines(canvas, lines)
    canvas.create_rectangle(rectangle[0], rectangle[1], rectangle[2], rectangle[3], outline=clippercolour)


def click_right(event, lines, canvas, linecolour):
    x = event.x
    y = event.y

    if len(lines) == 0 or len(lines[-1]) > 2:
        lines.append([])

    set_pixel(canvas, x, y, linecolour)

    lines[-1].append([x, y])

    if len(lines[-1]) == 2:
        canvas.create_line(lines[-1][0], lines[-1][1], fill=linecolour)

        lines[-1].append(linecolour)

def draw_rectangle_by_Button(event, rectangle, lines, canvas, clippercolour, flag):
    if flag == False:
        rectangle[0] = event.x
        rectangle[1] = event.y

        flag = True
    else:
        x = event.x
        y = event.y

        canvas.delete("all")
        draw_lines(canvas, lines)
        canvas.create_rectangle(rectangle[0], rectangle[1], x, y, outline=clippercolour)

        rectangle[2] = x
        rectangle[3] = y
    return flag
