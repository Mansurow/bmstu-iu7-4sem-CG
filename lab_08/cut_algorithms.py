def scalar_mul(fvector, svector):
    return fvector[0] * svector[0] + fvector[1] * svector[1]

def get_vect(dot_start, dot_end):
    return [dot_end[0] - dot_start[0], dot_end[1] - dot_start[1]]

def get_vect_mul(fvector, svector):
    return fvector[0] * svector[1] - fvector[1] * svector[0]

def check_convexity_polygon(cutter):
    if len(cutter) < 3:
        return False

    vect1 = get_vect(cutter[0], cutter[1])
    vect2 = get_vect(cutter[1], cutter[2])

    sign = None
    if get_vect_mul(vect1, vect2) > 0:
        sign = 1
    else:
        sign = -1

    for i in range(len(cutter)):
        vecti = get_vect(cutter[i-2], cutter[i-1])
        vectj = get_vect(cutter[i-1], cutter[i])

        if sign * get_vect_mul(vecti, vectj) < 0:
            return False

    if sign < 0:
        cutter.reverse()

    return True

def get_normal(dot1, dot2, dot3):
    vector = get_vect(dot1, dot2)

    if vector[1]:
        normal = [1, - vector[0] / vector[1]]
    else:
        normal = [0, 1]

    if scalar_mul(get_vect(dot2, dot3), normal) < 0:
        normal[0] = - normal[0]
        normal[1] = - normal[1]

    return normal

def cyrus_beck_alg(canvas, clipper_figure, line, res_color):
    t_beg = 0
    t_end = 1

    dot1 = line[0]
    dot2 = line[1]

    d = [dot2[0] - dot1[0], dot2[1] - dot1[1]]  # директриса

    for i in range(-2, len(clipper_figure) - 2):
        normal = get_normal(clipper_figure[i], clipper_figure[i + 1], clipper_figure[i + 2])

        w = [dot1[0] - clipper_figure[i][0],
             dot1[1] - clipper_figure[i][1]]

        d_scalar = scalar_mul(d, normal)
        w_scalar = scalar_mul(w, normal)

        if d_scalar == 0:
            if w_scalar < 0:
                return
            else:
                continue

        t = - w_scalar / d_scalar

        if d_scalar > 0:
            if t <= 1:
                t_beg = max(t_beg, t)
            else:
                return

        elif d_scalar < 0:
            if t >= 0:
                t_end = min(t_end, t)
            else:
                return

        if t_beg > t_end:
            break

    if t_beg <= t_end:
        dot1_res = [round(dot1[0] + d[0] * t_beg), round(dot1[1] + d[1] * t_beg)]
        dot2_res = [round(dot1[0] + d[0] * t_end), round(dot1[1] + d[1] * t_end)]

        canvas.create_line(dot1_res, dot2_res, fill=res_color)