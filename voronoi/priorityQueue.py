import heapq
from .dataStructures import Event


class PriorityQueue(object):
    def __init__(self, items=[]):
        self.heap = []
        self.events_to_nodes = {}
        for i in items:
            self.add(i)

    def add(self, event: Event):

        if event.node != None and self.events_to_nodes.get(event.node) != None:
            self.delete(self.events_to_nodes.get(event.node))

        entry = [-event.point.y, event]
        if event.node != None:
            self.events_to_nodes[event.node] = event
        heapq.heappush(self.heap, entry)

    def pop(self):
        while self.heap:
            temp: Event = heapq.heappop(self.heap)[1]
            if not temp.false_alarm:
                if temp.node != None:
                    del self.events_to_nodes[temp.node]
                return temp
        return None

    def delete(self, item: Event):
        entry = self.events_to_nodes.pop(item.node)
        entry.false_alarm = True

    def __bool__(self):
        return len(self.heap) > 0
