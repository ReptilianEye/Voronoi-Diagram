from .dataStructures import Point


def distance(p1: Point, p2: Point):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5


def mat_det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def getIntersect(start1: Point, direction1: Point, start2: Point, direction2: Point):
    x1, y1 = start1.x, start1.y
    x2, y2 = direction1.x, direction1.y

    x3, y3 = start2.x, start2.y
    x4, y4 = direction2.x, direction2.y

    den = mat_det([(x1-x2), (x3-x4)], [(y1-y2), (y3-y4)])
    if den == 0:
        return None
    t = mat_det([(x1-x3), (x3-x4)], [(y1-y3), (y3-y4)]) / den
    u = -mat_det([(x1-x2), (x1-x3)], [(y1-y2), (y1-y3)]) / den

    if 0 <= t and 0 <= u:
        return Point(x1 + t*(x2-x1), y1 + t*(y2-y1))
    return None


def lineSegmentIntersect(start: Point, end: Point, line_start: Point, line_direction: Point):
    x1, y1 = start.x, start.y
    x2, y2 = end.x, end.y

    x3, y3 = line_start.x, line_start.y
    x4, y4 = line_direction.x, line_direction.y

    den = mat_det([(x1-x2), (x3-x4)], [(y1-y2), (y3-y4)])
    if den == 0:
        return None
    t = mat_det([(x1-x3), (x3-x4)], [(y1-y3), (y3-y4)]) / den
    u = -mat_det([(x1-x2), (x1-x3)], [(y1-y2), (y1-y3)]) / den

    if 0 <= t <= 1 and 0 <= u:
        return Point(x1 + t*(x2-x1), y1 + t*(y2-y1))
    return None
