from priorityQueue import PriorityQueue
from dataStructures import *
from util import *
from myLL import myLL
from visualizer.main import Visualizer


class Voronoi:
    def __init__(self, points):
        self.points = list(map(lambda p: Point(*p), points))

        self.box = []
        self.__init_box()

    def __init_box(self):
        points = self.points
        min_x = min(points, key=lambda p: p.x).x
        max_x = max(points, key=lambda p: p.x).x
        min_y = min(points, key=lambda p: p.y).y
        max_y = max(points, key=lambda p: p.y).y
        margin_x = max(1, (max_x - min_x) * 0.1)
        margin_y = max(1, (max_y - min_y) * 0.1)
        bottom_left = Point(min_x - margin_x, min_y - margin_y)
        top_right = Point(max_x + margin_x, max_y + margin_y)
        self.edges_segments = [(bottom_left, Point(bottom_left.x, top_right.y)),
                               (Point(bottom_left.x, top_right.y), top_right),
                               (Point(top_right.x, bottom_left.y), top_right),
                               (bottom_left, Point(top_right.x, bottom_left.y))]
        self.box = [bottom_left, top_right]

    def __drawBox(self):
        box = self.box
        x_box = list(
            map(lambda x: x.x, [box[0], box[0], box[1], box[1], box[0]]))
        y_box = list(
            map(lambda x: x.y, [box[0], box[1], box[1], box[0], box[0]]))

        self.vis.add_polygon([(x_box[i], y_box[i])
                             for i in range(len(x_box))], fill=False, color="black")
        self.vis.add_point([(p.x, p.y) for p in self.points])

    def __init_data(self):
        self.Q = PriorityQueue()
        # self.T = Beachline()
        self.T = myLL()
        self.D = []
        self.starts = {}

    def get_voronoi(self):
        self.withVisualisation = False
        voronoi_edges, box, _ = self.get_voronoi_visualised()
        return voronoi_edges, box

    def get_voronoi_visualised(self):
        self.withVisualisation = True
        self.__init_data()
        Q = self.Q
        if self.withVisualisation:
            self.vis = Visualizer()
            vis = self.vis
            self.__drawBox()
        else:
            self.vis = None
        allVertical = len(set(map(lambda p: p.x, self.points))) == 1
        if allVertical:
            self.__handleVerticalPoints()
            return self.D, self.box, self.vis

        for p in self.points:
            Q.add(Event(SITE_EVENT, point=p))

        if self.withVisualisation:
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

                if event.cirle_center_point.y < self.box[0].y:
                    break
                if event.cirle_center_point.x < self.box[0].x or event.cirle_center_point.x > self.box[1].x:
                    continue

            y = event.point.y
            Arc.setDirectrix(y)
            if self.withVisualisation:
                self.__clear_last_vis(broom, parabolas, circles)
                broom = vis.add_line(
                    [(min_x, y), (max_x, y)], color="red")
                parabolas = self.__drawParabolas()
            if event.type == SITE_EVENT:
                self.__handleSiteEvent(event.point)
            else:
                if self.withVisualisation:
                    circle = vis.add_circle(
                        (event.cirle_center_point.x, event.cirle_center_point.y, event.cirle_center_point.y - y), fill=False)
                    circles.append(circle)

                self.__handleCircleEvent(event)

        if self.withVisualisation:
            self.__clear_last_vis(broom, parabolas, circles)
        for e in self.starts.values():
            self.D.append(e)
        self.__finishEdges()
        self.__cropEdges()
        voronoi_edges = [((start.x, start.y), (end.x, end.y))
                         for start, end in self.D]
        if self.withVisualisation:
            for start, end in voronoi_edges:
                vis.add_line_segment((start, end))
        return voronoi_edges, self.box, vis

    def __handleSiteEvent(self, p):
        T = self.T
        Q = self.Q
        D = self.D

        arc_above_node, left_circle_event, right_circle_event = T.insert(p)
        if arc_above_node is None:
            return

        if arc_above_node.arc.circle_event != None:
            Q.delete(arc_above_node.arc.circle_event)

        if left_circle_event != None:
            Q.add(left_circle_event)
        if right_circle_event != None:
            Q.add(right_circle_event)

    def __handleCircleEvent(self, event):
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
        self.__addToDiagram(closedLeft.start, closedLeft.end)
        self.__addToDiagram(closedRight.start, closedRight.end)

        al.setRightEdge(ar, point)

        left_circle_event, right_circle_event = T.handleSquize(leaf)
        if left_circle_event != None:
            Q.add(left_circle_event)
        if right_circle_event != None:
            Q.add(right_circle_event)

    def __clear_last_vis(self, broom, parabolas, circles):
        self.vis.remove_figure(broom)
        for parabola in parabolas:
            self.vis.remove_figure(parabola)
        for circle in circles:
            self.vis.remove_figure(circle)
        parabolas.clear()
        circles.clear()

    def __drawParabolas(self):
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

    def __isPointInBox(self, point: Point):
        return self.box[0].x <= point.x <= self.box[1].x and self.box[0].y <= point.y <= self.box[1].y

    def __cropEdges(self):
        for i in range(len(self.D)):
            for j in range(2):
                if not self.__isPointInBox(self.D[i][j]) and not self.__isPointInBox(self.D[i][1-j]):
                    self.D[i] = None
                    break
                if not self.__isPointInBox(self.D[i][j]):
                    self.D[i] = self.__finishEdgeWithBox(
                        # Edge(*self.D[i])
                        Edge(self.D[i][1-j], self.D[i][j])
                    )
                    if self.D[i] is None:
                        # self.D.pop(i)
                        break
        self.D = list(filter(lambda x: x is not None, self.D))

    def __handleVerticalPoints(self):
        points = sorted(self.points, key=lambda p: p.y)
        for i in range(len(points)-1):
            y = (points[i].y + points[i+1].y) / 2
            edge = ((self.box[0].x, y), (self.box[1].x, y))
            self.D.append(edge)
            if self.withVisualisation:
                self.vis.add_line_segment(edge)

    def __finishEdges(self):
        r = self.T.head.next
        while r is not None:
            if r.arc.edgeGoingLeft is not None and r.arc.edgeGoingLeft.end is None:
                e = self.__finishEdgeWithBox(r.arc.edgeGoingLeft)
                if e:
                    self.D.append(e)
            if r.arc.edgeGoingRight is not None and r.arc.edgeGoingRight.end is None:
                e = self.__finishEdgeWithBox(r.arc.edgeGoingRight)
                if e:
                    self.D.append(e)
            if r.next is None:
                break
            r = self.T.rightNbour(r)

    def __finishEdgeWithBox(self, edge: Edge):
        line_start = edge.start
        direction = edge.direction
        for start, end in self.edges_segments:
            intersect = lineSegmentIntersect(start, end, line_start, direction)
            if intersect:
                edge.end = intersect
                return (edge.start, edge.end)
                # self.D.append((edge.start, edge.end))
                # return

    def __addToDiagram(self, start, end):
        if start in self.starts:
            e = self.starts[start]
            self.D.append((e[1], end))
            del self.starts[start]
        else:
            self.starts[start] = (start, end)
