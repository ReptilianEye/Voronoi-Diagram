from priorityqueue import PriorityQueue
from beachline import Beachline
from datatypes import *
from util import *
from matplotlib import pyplot as plt
# beachline
# insert, delete, find arc by x coordinate
# Na razie może być linkedlita


class Voronoi:
    def __init__(self, points):
        self.points = list(map(lambda p: Point(*p), points))
        self.Q = PriorityQueue()
        self.T = Beachline()
        self.D = []
        self.box = []
        self.init_box()

    def init_box(self):
        points = self.points
        min_x = min(points, key=lambda p: p.x).x
        max_x = max(points, key=lambda p: p.x).x
        min_y = min(points, key=lambda p: p.y).y
        max_y = max(points, key=lambda p: p.y).y
        margin_x = (max_x - min_x) * 0.1
        margin_y = (max_y - min_y) * 0.1
        bottom_left = Point(min_x - margin_x, min_y - margin_y)
        top_right = Point(max_x + margin_x, max_y + margin_y)
        self.box = [bottom_left, top_right]

    def drawBox(self, plt):
        box = self.box
        x_box = list(
            map(lambda x: x.x, [box[0], box[0], box[1], box[1], box[0]]))
        y_box = list(
            map(lambda x: x.y, [box[0], box[1], box[1], box[0], box[0]]))
        plt.plot(x_box, y_box, color="black")
        plt.scatter([p.x for p in self.points], [p.y for p in self.points])

    def get_voronoi(self):
        Q = self.Q
        T = self.T
        D = self.D
        self.drawBox(plt)
        plt.show()

        for p in self.points:
            Q.add(Event(SITE_EVENT, point=p))
        # print(Q.heap)
        while Q:
            event = Q.pop()
            Arc.setDirectrix(event.point.y)
            if event.type == SITE_EVENT:
                self.handleSiteEvent(event.point)
            else:
                self.handleCircleEvent(event)
        T.print()
        for start, end in D:
            print(start, end)

    def handleSiteEvent(self, p):
        T = self.T
        Q = self.Q
        D = self.D

        arc_above_node, left_circle_event, right_circle_event = T.insert(p)
        if arc_above_node is None:
            return
        # arc = Arc(p)
        # if not T:
        #     T.insert(arc)
        #     return

        # # Find arc above p
        # arcAbove = T.find_node(p)

        if arc_above_node.arc.circle_event != None:
            Q.delete(arc_above_node.arc.circle_event)

        # afl, afr = T.replace(arcAbove, arc)

        if left_circle_event != None:
            Q.add(left_circle_event)
        if right_circle_event != None:
            Q.add(right_circle_event)

    def handleCircleEvent(self, event):
        T = self.T
        Q = self.Q
        leaf: Node = event.node
        lnode: Node = T.leftNbour(leaf)
        rnode: Node = T.rightNbour(leaf)
        al: Arc = lnode.arc
        ar: Arc = rnode.arc

        point: Point = event.cirle_center_point

        closedLeft = leaf.arc.edgeGoingLeft
        closedRight = leaf.arc.edgeGoingRight

        closedLeft.end = point
        closedRight.end = point
        self.D.append((closedLeft.start, closedLeft.end))
        self.D.append((closedRight.start, closedRight.end))

        al.setRightEdge(ar, point)
        # ar.setLeftEdge(al, point) # not needed because setRightEdge does it

        # leftEdge = al.edgeGoingLeft
        # rightEdge = ar.edgeGoingRight
        # leftEdge.end = point
        # rightEdge.end = point

        left_circle_event, right_circle_event = T.handleSquize(leaf)
        if left_circle_event != None:
            Q.add(left_circle_event)
        if right_circle_event != None:
            Q.add(right_circle_event)
