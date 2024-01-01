from priorityqueue import PriorityQueue
from beachline import Beachline
from datatypes import *
from util import *
from matplotlib import pyplot as plt
from myLL import myLL
from visualizer.main import Visualizer
# beachline
# insert, delete, find arc by x coordinate
# Na razie może być linkedlita


class Voronoi:
    def __init__(self, points):
        self.points = list(map(lambda p: Point(*p), points))

        self.box = []
        self.init_box()
        # self.vis = Visualizer()

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
        self.edges_segments = [(bottom_left, Point(bottom_left.x, top_right.y)),
                               (Point(bottom_left.x, top_right.y), top_right),
                               (Point(top_right.x, bottom_left.y), top_right),
                               (bottom_left, Point(top_right.x, bottom_left.y))]
        self.box = [bottom_left, top_right]

    def drawBox(self):
        box = self.box
        x_box = list(
            map(lambda x: x.x, [box[0], box[0], box[1], box[1], box[0]]))
        y_box = list(
            map(lambda x: x.y, [box[0], box[1], box[1], box[0], box[0]]))

        self.vis.add_polygon([(x_box[i], y_box[i])
                             for i in range(len(x_box))], fill=False, color="black")
        self.vis.add_point([(p.x, p.y) for p in self.points])
        # plt.plot(x_box, y_box, color="black")
        # plt.scatter([p.x for p in self.points], [p.y for p in self.points])

    def init_data(self):
        self.Q = PriorityQueue()
        # self.T = Beachline()
        self.T = myLL()
        self.D = []

    def get_voronoi(self):
        self.init_data()
        Q = self.Q
        T = self.T
        D = self.D
        # self.drawBox(plt)

        for p in self.points:
            Q.add(Event(SITE_EVENT, point=p))
        # print(Q.heap)
        while Q:
            event = Q.pop()
            if event is None:
                break
            if event.type == CIRCLE_EVENT and event.cirle_center_point.y < self.box[0].y:
                break
            Arc.setDirectrix(event.point.y)
            if event.type == SITE_EVENT:
                self.handleSiteEvent(event.point)
            else:
                self.handleCircleEvent(event)

        # T.print()
        self.finishEdges()
        self.cropEdges()
        voronoi_edges = [(start.x, start.y, end.x, end.y)
                         for start, end in self.D]
        # return voronoi_edges, self.box
        for start, end in self.D:
            plt.plot([start.x, end.x], [start.y, end.y])
        return plt

    def get_voronoi_visualised(self):
        self.init_data()
        Q = self.Q
        T = self.T
        D = self.D
        self.vis = Visualizer()
        vis = self.vis
        self.drawBox()
        # self.vis.show_gif()
        # self.vis.show()
        for p in self.points:
            Q.add(Event(SITE_EVENT, point=p))
        # print(Q.heap)
        min_x = self.box[0].x
        max_x = self.box[1].x
        broom = vis.add_line(
            [(min_x, self.box[1].y), (max_x, self.box[1].y)], color="red")
        parabolas = []
        circles = []
        while Q:
            event = Q.pop()
            if event is None:
                break
            if event.type == CIRCLE_EVENT:
                # if event.cirle_center_point.y > self.box[1].y:
                #     continue
                if event.cirle_center_point.y < self.box[0].y:
                    break
            y = event.point.y
            Arc.setDirectrix(y)
            self.clear_last_vis(broom, parabolas, circles)
            broom = vis.add_line(
                [(min_x, y), (max_x, y)], color="red")
            parabolas = self.drawParabolas()
            if event.type == SITE_EVENT:
                self.handleSiteEvent(event.point)
            else:
                circle = vis.add_circle(
                    (event.cirle_center_point.x, event.cirle_center_point.y, event.cirle_center_point.y - y), fill=False)
                circles.append(circle)
                self.handleCircleEvent(event)
        self.clear_last_vis(broom, parabolas, circles)
        # T.print()
        self.finishEdges()
        self.cropEdges()
        for start, end in self.D:
            vis.add_line_segment(((start.x, start.y), (end.x, end.y)))
            # plt.plot([start.x, end.x], [start.y, end.y])
        return vis

    def clear_last_vis(self, broom, parabolas, circles):
        self.vis.remove_figure(broom)
        for parabola in parabolas:
            self.vis.remove_figure(parabola)
        for circle in circles:
            self.vis.remove_figure(circle)

    def drawParabolas(self):
        drawnParabolas = []
        drawn = set()
        T = self.T
        vis = self.vis
        r = T.head.next
        while r is not None:
            arc = r.arc
            if arc.focus not in drawn:
                parabola = arc.draw(vis, self.box)
                drawnParabolas.append(parabola)
                drawn.add(arc.focus)
            if r.next is None:
                break
            r = T.rightNbour(r)
        return drawnParabolas

    def isPointInBox(self, point: Point):
        return self.box[0].x <= point.x <= self.box[1].x and self.box[0].y <= point.y <= self.box[1].y

    def cropEdges(self):
        for i in range(len(self.D)):
            for j in range(2):
                if not self.isPointInBox(self.D[i][j]) and not self.isPointInBox(self.D[i][1-j]):
                    self.D[i] = None
                    break
                if not self.isPointInBox(self.D[i][j]):
                    self.D[i] = self.finishEdgeWithBox(
                        # Edge(*self.D[i])
                        Edge(self.D[i][1-j], self.D[i][j])
                    )
                    if self.D[i] is None:
                        # self.D.pop(i)
                        break
        self.D = list(filter(lambda x: x is not None, self.D))
        # if not self.isPointInBox(self.D[i][0]):
        #     self.D[i] = self.finishEdgeWithBox(
        #         # Edge(*self.D[i])
        #         Edge(self.D[i][1], self.D[i][0])
        #     )
        # self.D[i] = self.finishEdgeWithBox(
        #     # Edge(*self.D[i])
        #     Edge(self.D[i][1], self.D[i][0])
        # )

    def finishEdges(self):
        r = self.T.head.next
        while r is not None:
            if r.arc.edgeGoingLeft is not None and r.arc.edgeGoingLeft.end is None:
                e = self.finishEdgeWithBox(r.arc.edgeGoingLeft)
                if e:
                    self.D.append(e)
            if r.arc.edgeGoingRight is not None and r.arc.edgeGoingRight.end is None:
                e = self.finishEdgeWithBox(r.arc.edgeGoingRight)
                if e:
                    self.D.append(e)
            if r.next is None:
                break
            r = self.T.rightNbour(r)

    # def finishEdgesTree(self):
    #     r = self.T.root
    #     while r.left != None:
    #         r = r.left
    #     while r is not None:
    #         if r.arc.edgeGoingLeft is not None and r.arc.edgeGoingLeft.end is None:
    #             e = self.finishEdgeWithBox(r.arc.edgeGoingLeft)
    #             if e:
    #                 self.D.append(e)
    #         if r.arc.edgeGoingRight is not None and r.arc.edgeGoingRight.end is None:
    #             e = self.finishEdgeWithBox(r.arc.edgeGoingRight)
    #             if e:
    #                 self.D.append(e)
    #         r = r.next

    def finishEdgeWithBox(self, edge: Edge):
        line_start = edge.start
        direction = edge.direction
        for start, end in self.edges_segments:
            intersect = lineSegmentIntersect(start, end, line_start, direction)
            if intersect:
                edge.end = intersect
                return (edge.start, edge.end)
                # self.D.append((edge.start, edge.end))
                # return

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

        # if leaf.arc.circle_event != None:
        #     Q.delete(leaf.arc.circle_event)

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
