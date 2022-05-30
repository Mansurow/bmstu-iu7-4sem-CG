
def get_bit_cod_point(rectange, point):
    bit = 0b0000
    #   x < x_лев
    if point[0] < rectange[0]:
        bit += 0b0001
    # x > x_прав
    if point[0] > rectange[1]:
        bit += 0b0010
    # y < y_низ
    if point[1] < rectange[2]:
        bit += 0b0100
    # y > y_верх
    if point[1] > rectange[3]:
        bit += 0b1000
    return bit

def T_arr(rect, point):
    x = point[0]
    y = point[1]
    xl = rect[0]
    xr = rect[1]
    yd = rect[2]
    yu = rect[3]

    T = [0, 0, 0, 0]
    T[0] = 1 if x < xl else 0
    T[1] = 1 if x > xr else 0
    T[2] = 1 if y < yd else 0
    T[3] = 1 if y > yu else 0

    return T

def count_S(T):
    return sum(T)

def logic_multy(T1, T2):
    mul = 0
    for i in range(4):
        mul += T1[i] * T2[i]
    return mul

def sutherland_cohen_algorithm(rectangle, line):
    p1 = [line[0][0], line[0][1]]
    p2 = [line[1][0], line[1][1]]

    Fl = 0

    if p1[0] == p2[0]:
        Fl = -1
    else:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])

        if m == 0:
            Fl = 1
    for i in range(4):
        T1 = T_arr(rectangle, p1)
        T2 = T_arr(rectangle, p2)

        pr = find_visibility(T1, T2)
        if pr == -1:
            return pr, [p1, p2]
        if pr == 1:
            return pr, [p1, p2]

        if T1[i] == T2[i]:
            continue

        if T1[i] == 0:
            p1, p2 = p2, p1

        if Fl == -1:
            p1[1] = rectangle[i]
        else:
            if i < 2:
                p1[1] = m*(rectangle[i] - p1[0]) + p1[1]
                p1[0] = rectangle[i]
            else:
                p1[0] = (1 / m) * (rectangle[i] - p1[1]) + p1[0]
                p1[1] = rectangle[i]


    return pr, [p1, p2]

def find_visibility(T1, T2):
    S1 = count_S(T1)
    S2 = count_S(T2)

    if S1 == 0 and S2 == 0:
        pr = 1
    else:
        Pl = logic_multy(T1, T2)
        if Pl == 1:
            pr = -1
        else:
            pr = 0
    return pr