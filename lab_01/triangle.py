from math import sqrt, acos, pi

from class_point import *

EPS = 1e-6


# вершина проведения с
def length_bisector(side_a, side_b, side_c):
    return sqrt(side_a * side_b * (side_a + side_b + side_c) * (side_a + side_b - side_c)) / (side_a + side_b)


def length_side_triangle(pa, pb):
    return sqrt((pb.x - pa.x) * (pb.x - pa.x) + (pb.y - pa.y) * (pb.y - pa.y))


def displacement_factor(side_a, side_b):
    if abs(side_a) < EPS or abs(side_b) < EPS:
        return 0.0
    if side_a >= side_b:
        k = side_a / side_b
    else:
        k = side_b / side_a

    return k


def is_triangle(side_a, side_b, side_c):
    if abs(side_a + side_b - side_c) < EPS or abs(side_b + side_c - side_a) < EPS or abs(side_a + side_c - side_b) < EPS:
        return False
    else:
        return True


def find_coordinate(x1, x2, k):
    return (x1 + k * x2) / (1 + k)


def find_middle_coordinate(x1, x2):
    return (x1 + x2) / 2


def find_point_bisector_on_front_side(pa, pb, pc):
    pm = Point(0, 0)

    ab = length_side_triangle(pa, pb)
    ac = length_side_triangle(pa, pc)

    k = displacement_factor(ab, ac)

    if ab >= ac:
        pm.x = find_coordinate(pc.x, pb.x, k)
        pm.y = find_coordinate(pc.y, pb.y, k)
    else:
        pm.x = find_coordinate(pb.x, pc.x, k)
        pm.y = find_coordinate(pb.y, pc.y, k)

    return pm


def find_point_median_on_front_side(pb, pc):
    pn = Point(0, 0)

    pn.x = find_middle_coordinate(pb.x, pc.x)
    pn.y = find_middle_coordinate(pb.y, pc.y)

    return pn


# от с
def find_corner(side_a, side_b, side_c):
    return acos((side_a * side_a + side_b * side_b - side_c * side_c) / (2 * side_a * side_b)) * (180 / pi)


def find_corner_between_bisector_median(pa, pb, pc):
    pbisector = find_point_bisector_on_front_side(pa, pb, pc)
    pmedian = find_point_median_on_front_side(pb, pc)

    am = length_side_triangle(pa, pbisector)
    an = length_side_triangle(pa, pmedian)
    mn = length_side_triangle(pbisector, pmedian)

    print("----- The bisector and median----------")
    print("am = ", am)
    print("an = ", an)
    print("mn = ", mn)

    return pbisector, pmedian, find_corner(am, an, mn)
