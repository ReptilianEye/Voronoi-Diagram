from voronoi.delaunay.utils import Point, Triangle, mat_det_3x3


class Triangulation:
    def __init__(self, P):
        self.edges = {}
        self.triangles = set()
        self.data_frame, self.map_vertexes, self.central_point, self.central_triangle = self.get_triangulation_start(
            P)

    def get_triangulation_start(self, P):
        low_left = Point(float('inf'), float('inf'))
        up_right = Point(float('-inf'), float('-inf'))
        for p in P:
            if p.x < low_left.x:
                low_left.x = p.x
            if p.x > up_right.x:
                up_right.x = p.x
            if p.y < low_left.y:
                low_left.y = p.y
            if p.y > up_right.y:
                up_right.y = p.y
        data_frame = [Point(low_left.x, low_left.y),
                      Point(up_right.x, up_right.y)]
        central_point = Point((low_left.x + up_right.x)/2,
                              (low_left.y + up_right.y)/2 + 1e-2)
        low_left.x += -10**4
        low_left.y += -10**4
        up_right.x += 10**4
        up_right.y += 10**4
        map_vertexes = [low_left, Point(
            up_right.x, low_left.y), up_right, Point(low_left.x, up_right.y)]
        self.triangles.add(
            Triangle(low_left, Point(up_right.x, low_left.y), up_right))
        self.triangles.add(Triangle(low_left, up_right,
                           Point(low_left.x, up_right.y)))
        central_triangle = None
        for tri in self.triangles:
            if central_point in tri:
                central_triangle = tri
            # posortowane
            self.edges[(tri.p1, tri.p2)] = tri.p3
            self.edges[(tri.p2, tri.p3)] = tri.p1
            self.edges[(tri.p3, tri.p1)] = tri.p2
        return data_frame, map_vertexes, central_point, central_triangle

    # funkcja służy dostosowaniu prostokąta ograniczającego konstrukcję Voronoi
    def adjust_map_size(self, map_size=3):
        left = self.data_frame[0].x - map_size
        low = self.data_frame[0].y - map_size
        right = self.data_frame[1].x + map_size
        up = self.data_frame[1].y + map_size
        self.map_vertexes = [Point(left, low), Point(
            right, low), Point(right, up), Point(left, up)]

    def find_adjacent_tri(self, edge):
        if (edge[1], edge[0]) in self.edges:
            tri = Triangle(edge[1], edge[0], self.edges[(edge[1], edge[0])])
            tri.sort_tri_vertexes()
            return tri
        return None

    def find_all_adjacent_tri(self, triangle):
        tri_adjacent = set()
        tri = self.find_adjacent_tri((triangle.p1, triangle.p2))
        if tri:
            tri_adjacent.add(tri)
        tri = self.find_adjacent_tri((triangle.p2, triangle.p3))
        if tri:
            tri_adjacent.add(tri)
        tri = self.find_adjacent_tri((triangle.p3, triangle.p1))
        if tri:
            tri_adjacent.add(tri)
        return tri_adjacent

    def remove(self, triangle):
        triangle.sort_tri_vertexes()
        if (triangle.p1, triangle.p2) in self.edges:
            del self.edges[(triangle.p1, triangle.p2)]
        if (triangle.p2, triangle.p3) in self.edges:
            del self.edges[(triangle.p2, triangle.p3)]
        if (triangle.p3, triangle.p1) in self.edges:
            del self.edges[(triangle.p3, triangle.p1)]
        self.triangles.remove(triangle)

    def add(self, triangle):
        triangle.sort_tri_vertexes()
        self.edges[(triangle.p1, triangle.p2)] = triangle.p3
        self.edges[(triangle.p2, triangle.p3)] = triangle.p1
        self.edges[(triangle.p3, triangle.p1)] = triangle.p2
        self.triangles.add(triangle)

    def adjust_triangulation(self, tri_to_remove, p):
        for tri in tri_to_remove:
            tri.sort_tri_vertexes()
        outer_edges = set()

        for tri in tri_to_remove:
            tri_edges = tri.get_edges()  # set krawędzi trójkąta
            for edge in tri_edges:
                if not ((edge[1], edge[0]) in self.edges):
                    outer_edges.add(edge)
                elif not (self.find_adjacent_tri(edge) in tri_to_remove):
                    outer_edges.add(edge)

        for tri in tri_to_remove:
            self.remove(tri)

        added_tri = []
        for edge in outer_edges:
            tri = Triangle(edge[0], edge[1], p)
            tri.sort_tri_vertexes()
            added_tri.append(tri)
            self.add(tri)

        if self.central_triangle in tri_to_remove:
            for tri in added_tri:
                if self.central_point in tri:
                    self.central_triangle = tri

    def remove_map_vertexes(self):
        triangles = list(self.triangles)
        for tri in triangles:
            if tri.p1 in self.map_vertexes:
                self.remove(tri)
            elif tri.p2 in self.map_vertexes:
                self.remove(tri)
            elif tri.p3 in self.map_vertexes:
                self.remove(tri)


# funkcje pomocnicze funkcji Delaunay

def get_points(Points):
    P = []
    for point in Points:
        P.append(Point(point[0], point[1]))
    return P


def find_containing(T, p):
    curr_tri = T.central_triangle
    tri_visited = set()
    while True:
        tri_visited.add(curr_tri)
        p1 = curr_tri.p1
        p2 = curr_tri.p2
        p3 = curr_tri.p3
        if mat_det_3x3(p1, p2, p) < 0:
            curr_tri = T.find_adjacent_tri((p1, p2))
        elif mat_det_3x3(p2, p3, p) < 0:
            curr_tri = T.find_adjacent_tri((p2, p3))
        elif mat_det_3x3(p3, p1, p) < 0:
            curr_tri = T.find_adjacent_tri((p3, p1))
        else:
            return curr_tri


# Główna funkcja Delaunay

def delaunay(Points):
    P = get_points(Points)
    T = Triangulation(P)

    for p in P:
        containing_tri = find_containing(T, p)
        tri_to_remove = []  # trójkąty do usunięcia
        tri_visited = []  # odwiedzone trójkąty
        stack = [containing_tri]

        while len(stack) > 0:
            curr_tri = stack.pop()
            tri_visited.append(curr_tri)

            if curr_tri.in_circle(p):
                tri_to_remove.append(curr_tri)
                tri_adjacent = T.find_all_adjacent_tri(
                    curr_tri)  # trójkąty sąsiadujące z curr_tri

                for triangle in tri_adjacent:
                    if triangle not in tri_visited and triangle not in stack:
                        stack.append(triangle)

        T.adjust_triangulation(tri_to_remove, p)

    T.remove_map_vertexes()
    return T
