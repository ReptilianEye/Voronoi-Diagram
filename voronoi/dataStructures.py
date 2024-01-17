from dataclasses import dataclass
from numpy import sqrt, linspace

SITE_EVENT = 'site'
CIRCLE_EVENT = 'circle'


class Node:
    def __init__(self):
        self.arc = None
        self.arc_pair: Pair = None
        self.parent = None
        self.left = None
        self.right = None
        self.prev = None
        self.next = None

    def parabolaIntersectX(self):
        return self.arc_pair.parabolaIntersect()


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y

    def __repr__(self):
        return f"Point({self.x:.3f}, {self.y:.3f})"


@dataclass
class Edge:
    def __init__(self, start: Point, direction: Point):
        self.start = start
        self.direction = direction
        self.twin = None
        self.end = None

    def close_edge(self, end: Point):
        self.end = end

    def __repr__(self):
        return f"Edge(start={self.start}, dir=({self.direction.x:.3f}, {self.direction.y:.3f}))"


class Arc:
    directrix: float

    objects = []

    def __init__(self, focus):
        self.focus = focus
        self.circle_event = None
        self.edgeGoingLeft = None
        self.edgeGoingRight = None
        self.a = None
        self.b = None
        self.c = None
        if self.directrix is not None:
            self.updateABC()
        self.__class__.objects.append(self)

    @classmethod
    def setDirectrix(cls, directrix, all=True):
        cls.directrix = directrix
        if all:
            for obj in cls.objects:
                obj.updateABC()

    def setLeftEdge(self, side_arc, start=None):
        if start is None:
            start_x = self.focus.x
            start = Point(start_x, side_arc.__unit_val(start_x))

        left_intersection = side_arc.lookupForIntersectionBetween(self)
        leftEdge = Edge(start, left_intersection)
        side_arc.edgeGoingRight = leftEdge
        self.edgeGoingLeft = leftEdge

    def setRightEdge(self, side_arc, start=None):
        if start is None:
            start_x = self.focus.x
            start = Point(start_x, side_arc.__unit_val(start_x))
        right_intersection = self.lookupForIntersectionBetween(side_arc)
        rightEdge = Edge(start, right_intersection)
        side_arc.edgeGoingLeft = rightEdge
        self.edgeGoingRight = rightEdge

    def updateABC(self):
        if self.focus.y == self.directrix:
            return
        f = abs(self.focus.y - self.directrix)/2.0
        vertex = Point(self.focus.x, self.focus.y - f)
        self.a = 1.0 / (4*f)
        self.b = -vertex.x / (2*f)
        self.c = vertex.x**2 / (4*f) + vertex.y

    def __unit_val(self, x):
        return self.a*x**2 + self.b*x + self.c

    def value(self,  x, directrix=None):
        if directrix is not None:
            self.setDirectrix(directrix)
        return [self.__unit_val(x) for x in x]

    def draw(self, vis, box):
        x = linspace(box[0].x, box[1].x, 1000)
        parabolasPoints = list(filter(
            lambda point: point[1] < box[1].y, list(zip(x, self.value(x)))))
        return vis.add_point(parabolasPoints, s=0.1)

    def lookupForIntersectionBetween(self, right_arc):
        prevDirectrix = self.directrix
        self.setDirectrix(prevDirectrix-1, False)
        self.updateABC()
        right_arc.updateABC()
        found_intersect = self.intersect(right_arc)
        self.setDirectrix(prevDirectrix, False)
        self.updateABC()
        right_arc.updateABC()
        return found_intersect

    def lookupIntersectionsWithHigher(self, higher):
        return higher.lookForIntersectionBetween(self), self.lookupForIntersectionBetween(higher)

    def intersect(self, arc) -> Point:
        a = self.a - arc.a
        b = self.b - arc.b
        c = self.c - arc.c
        x = (-b + sqrt(b**2 - 4*a*c))/(2*a)
        return Point(x, self.__unit_val(x))


@dataclass
class Event:
    type: str
    point: Point = None

    # cirle event needed
    node: Node = None
    cirle_center_point: Point = None
    false_alarm: bool = False


class Pair:

    def __init__(self, left: Arc, right: Arc):
        self.left = left
        self.right = right

    def parabolaIntersect(self):
        return self.left.intersect(self.right).x
