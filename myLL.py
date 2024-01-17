from TInterface import T
from dataStructures import *
from util import *


class myLL(T):
    def __init__(self):
        self.head = Node()

    def find_node(self, p):
        r = self.head.next
        while r.next is not None and r.next.parabolaIntersectX() < p.x:
            r = r.next.next
        return r

    def replace(self, arc_node: Arc, new_arc: Arc):
        arc = arc_node.arc
        old_arc_l = Arc(arc.focus)
        old_arc_r = Arc(arc.focus)
        new_arc.setLeftEdge(old_arc_l)
        new_arc.setRightEdge(old_arc_r)
        old_arc_l.edgeGoingLeft = arc.edgeGoingLeft
        old_arc_r.edgeGoingRight = arc.edgeGoingRight

        #   old_arc_l -> old_new -> new_arc -> new_old -> old_arc_r

        old_new_node = Node()
        old_new_node.arc_pair = Pair(old_arc_l, new_arc)

        old_arc_leaf_l = Node()
        old_arc_leaf_l.arc = old_arc_l

        new_old_node = Node()
        new_old_node.arc_pair = Pair(new_arc, old_arc_r)

        new_arc_leaf = Node()
        new_arc_leaf.arc = new_arc

        old_arc_leaf_r = Node()
        old_arc_leaf_r.arc = old_arc_r

        # relations
        if arc_node.prev != None:
            arc_node.prev.next = old_arc_leaf_l
            old_arc_leaf_l.prev = arc_node.prev

        old_arc_leaf_l.next = old_new_node
        old_new_node.prev = old_arc_leaf_l

        old_new_node.next = new_arc_leaf
        new_arc_leaf.prev = old_new_node

        new_arc_leaf.next = new_old_node
        new_old_node.prev = new_arc_leaf

        new_old_node.next = old_arc_leaf_r
        old_arc_leaf_r.prev = new_old_node

        if arc_node.next != None:
            arc_node.next.prev = old_arc_leaf_r
            old_arc_leaf_r.next = arc_node.next

        return old_arc_leaf_l, old_arc_leaf_r

    def insert(self, p):
        arc = Arc(p)
        if self.head.next == None:
            new = Node()
            new.arc = arc
            self.head.next = new
            new.prev = self.head
            return None, None, None
        node_to_replace = self.find_node(p)

        left_arc_node, right_arc_node = self.replace(node_to_replace, arc)

        left_circle_event = self.checkForCircleEvent(left_arc_node)
        right_circle_event = self.checkForCircleEvent(right_arc_node)

        return node_to_replace, left_circle_event, right_circle_event

    def checkForCircleEvent(self, node):
        circle_center_point, circle_event_point = self.isCirleEvent(node)
        circle_event = None
        if circle_event_point != None:
            circle_event = Event(
                CIRCLE_EVENT, point=circle_event_point, cirle_center_point=circle_center_point, node=node)
            node.arc.circle_event = circle_event

        return circle_event

    def isCirleEvent(self, arc_node: Node):
        leftEdge = arc_node.arc.edgeGoingLeft
        rightEdge = arc_node.arc.edgeGoingRight
        if leftEdge == None or rightEdge == None:
            return None, None
        cirle_center = getIntersect(leftEdge.start, leftEdge.direction,
                                    rightEdge.start, rightEdge.direction)
        if cirle_center == None:
            return None, None
        circle_event_point = Point(
            cirle_center[0], cirle_center[1] - distance(cirle_center, self.rightNbour(arc_node).arc.focus))
        return cirle_center, circle_event_point

    def handleSquize(self, arc_node):
        al = self.leftNbour(arc_node)
        ar = self.rightNbour(arc_node)

        al.next.arc_pair.right = ar.arc
        ar.prev.arc_pair.left = al.arc

        intersect = Node()
        intersect.arc_pair = Pair(al.arc, ar.arc)

        self.__replaceRemove(arc_node, intersect)

        left_circle_event = self.checkForCircleEvent(al)
        right_circle_event = self.checkForCircleEvent(ar)

        return left_circle_event, right_circle_event

    def __replaceRemove(self, node, newPair):
        newPair.prev = node.prev.prev
        newPair.next = node.next.next
        node.prev.prev.next = newPair
        node.next.next.prev = newPair

    def leftNbour(self, node):
        return node.prev.prev

    def rightNbour(self, node):
        return node.next.next

    def print(self):
        r = self.head.next
        while r is not None:
            if r.arc_pair is None:
                print(r.arc.focus, end="->")
            r = r.next
        print()
