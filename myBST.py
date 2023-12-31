from datatypes import *
from TInterface import T


class MyBST(T):
    def __init__(self) -> None:
        self.root: Node = None

    def find_node(self, p: Point) -> Node:
        r = self.root
        while r.left or r.right:
            i = r.parabolaIntersectX()
            if i > p.x:
                r = r.left
            else:
                r = r.right
        return r

    def replace(self, arc_node: Arc, new_arc: Arc):
        arc = arc_node.arc
        # new_arc.setEdgesWithHigher(arc)
        old_arc_l = Arc(arc.focus)
        old_arc_r = Arc(arc.focus)  # deepcopy(arc)
        new_arc.setLeftEdge(old_arc_l)
        new_arc.setRightEdge(old_arc_r)
        old_arc_l.edgeGoingLeft = arc.edgeGoingLeft
        old_arc_r.edgeGoingRight = arc.edgeGoingRight
        #       old_new
        #      /       \
        # old_arc_l   new_old
        #             /  \
        #        new_arc  old_arc_r
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
        old_new_node.left = old_arc_leaf_l
        old_new_node.right = new_old_node
        old_arc_leaf_l.parent = old_new_node
        new_old_node.parent = old_new_node

        new_old_node.left = new_arc_leaf
        new_old_node.right = old_arc_leaf_r
        new_arc_leaf.parent = new_old_node
        old_arc_leaf_r.parent = new_old_node

        # old_arc_leaf_l.prev = arc_node.prev
        # old_arc_leaf_l.next = new_arc_leaf

        # new_arc_leaf.prev = old_arc_leaf_l
        # new_arc_leaf.next = old_arc_leaf_r

        # old_arc_leaf_r.prev = new_arc_leaf
        # old_arc_leaf_r.next = arc_node.next
        # connect to tree
        old_new_node.parent = arc_node.parent
        if arc_node.parent == None:
            self.root = old_new_node
        elif arc_node.parent.left == arc_node:
            arc_node.parent.left = old_new_node
        else:
            arc_node.parent.right = old_new_node
        self.update_next_prev()
        self.print()
        return old_arc_leaf_l, old_arc_leaf_r

    def insert(self, p):
        pass

    def update_next_prev(self):
        pass

    def print(self):
        pass
