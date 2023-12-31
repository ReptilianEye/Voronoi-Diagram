import heapq
from datatypes import Event, Point
# import itertools


class PriorityQueue(object):
    '''
    Creates Priority queue to use with Fortunes's algorithm
    item is a tuple of ((x,y), pointer_to_leaf)
    '''
    # heap = []

    def __init__(self, items=[]):
        self.heap = []
        self.events_to_nodes = {}
        # self.counter = itertools.count(0,-1)
        for i in items:
            self.add(i)

    def add(self, event: Event):
        # Check for duplicate

        if event.node != None and self.events_to_nodes.get(event.node) != None:
            self.delete(self.events_to_nodes.get(event.node))

        # count = next(self.counter)
        # use negative y-coordinate as a primary key
        # heapq in python is min-heap and we need max-heap
        # print("heapAdd: " + str(item[0]))
        entry = [-event.point.y, event]
        # entry = [item[0][1]*-1, count, item]
        if event.node != None:
            self.events_to_nodes[event.node] = event
        heapq.heappush(self.heap, entry)

    def pop(self):
        while self.heap:
            temp: Event = heapq.heappop(self.heap)[1]
            # print "pop" + str(temp[2][0])
            if not temp.false_alarm:
                if temp.node != None:
                    del self.events_to_nodes[temp.node]
                return temp
        raise KeyError('pop from an empty priority queue')

    def delete(self, item: Event):
        # print ("delete: " + str(item[0]))
        entry = self.events_to_nodes.pop(item.node)
        entry.false_alarm = True

    def __bool__(self):
        return bool(self.heap)
