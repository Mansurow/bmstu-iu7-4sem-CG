def DDA(x1, y1, x2, y2, colour='black', stepmode=False):
    pointsList = []
    steps = 0
    if x1 == x2 and y1 == y2:
        pointsList.append([round(x1), round(y1), colour])
    else:
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # steep - max growth
        if dx >= dy:
            length = dx
        else:
            length = dy
        dx = (x2 - x1) / length  # step of x
        dy = (y2 - y1) / length  # step of y

        # set line to start
        x = x1
        y = y1


        # i <= lenght i = 0
        # while abs(x - x2) > 1 or abs(y - y2) > 1:
        for i in range(0, int(length) + 1):
            if not stepmode:
                pointsList.append([round(x), round(y), colour])
            elif round(x + dx) != round(x) and round(y + dy) != round(y):
                steps += 1
            x += dx
            y += dy
    if stepmode:
        return steps
    return pointsList