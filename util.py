
from datatypes import Point


def distance(p1: Point, p2: Point):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5


def mat_det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def getIntersect(start1: Point, direction1: Point, start2: Point, direction2: Point):
    x1, y1 = start1.x, start1.y
    x2, y2 = direction1.x, direction1.y

    x3, y3 = start2.x, start2.y
    x4, y4 = direction2.x, direction2.y
    # Wyznaczenie równań prostych
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
    # Wyznaczenie równań prostych
    den = mat_det([(x1-x2), (x3-x4)], [(y1-y2), (y3-y4)])
    if den == 0:
        return None
    t = mat_det([(x1-x3), (x3-x4)], [(y1-y3), (y3-y4)]) / den
    u = -mat_det([(x1-x2), (x1-x3)], [(y1-y2), (y1-y3)]) / den

    if 0 <= t <= 1 and 0 <= u:
        return Point(x1 + t*(x2-x1), y1 + t*(y2-y1))
    return None


# def pointBeetwenPoints(toBeBetween: Point, p1: Point, p2: Point):
#     # is p0 between p1 and p2?
#     bot_left = min(p1, p2, key=lambda x: (x.x, x.y))
#     up_right = max(p1, p2, key=lambda x: (x.x, x.y))
#     return bot_left.x <= toBeBetween.x <= up_right.x and bot_left.y <= toBeBetween.y <= up_right.y
# def leftParent(node):
#     if node.parent == None:
#         return None
#     if node.parent.right == node:
#         return node.parent
#     return leftParent(node.parent)


# def rightParent(node):
#     if node.parent == None:
#         return None
#     if node.parent.left == node:
#         return node.parent
#     return rightParent(node.parent)


# def replaceRemove(node, replacement):
#     rParent = rightParent(node)
#     lParent = leftParent(node)
#     if rParent == None:
#         lParent.arc = replacement
#         lParent.right = None
#         return
#     if lParent == None:
#         rParent.arc = replacement
#         rParent.left = None
#         return
#     higherParent = lParent if node.parent == rParent else rParent
#     if higherParent == lParent:
#         __replaceOnRight(node, replacement)
#     else:
#         __replaceOnLeft(node, replacement)


# def __replaceOnRight(node, replacement):
#     lParent = leftParent(node)
#     rParent = rightParent(node)
#     lParent.arc = replacement.arc
#     if rParent.parent == lParent:
#         lParent.right = rParent.right
#     else:
#         rParent.parent.left = rParent.right


# def __replaceOnLeft(node, replacement):
#     rParent = rightParent(node)
#     lParent = leftParent(node)
#     rParent.arc = replacement.arc
#     if lParent.parent == rParent:
#         rParent.left = lParent.left
#     else:
#         lParent.parent.right = lParent.left
