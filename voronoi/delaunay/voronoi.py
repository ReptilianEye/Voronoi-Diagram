from voronoi.delaunay.utils import Point, Triangle, mat_det_3x3
from voronoi.delaunay.delaunay import Triangulation, get_points


class Voronoi:
    def __init__(self):
        self.edges = set()


def get_triangles_o(triangle, triangle_edge, T):
    triagnles_o = [triangle.o]
    if (triangle_edge[1], triangle_edge[0]) in T.edges:
        triangle_adjacent = Triangle(
            triangle_edge[1], triangle_edge[0], T.edges[(triangle_edge[1], triangle_edge[0])])
        triagnles_o.append(triangle_adjacent.o)
    return triagnles_o

# Sprawdza czy punkt należy do mapy


def is_in_map(o, T):
    t1 = Triangle(T.map_vertexes[0], T.map_vertexes[2], T.map_vertexes[3])
    t2 = Triangle(T.map_vertexes[0], T.map_vertexes[1], T.map_vertexes[2])
    return o in t1 or o in t2


def is_added(edge, V):
    return edge in V.edges or (edge[1], edge[0]) in V.edges


def check_intersection(e1, e2):
    x1 = e1[0].x
    y1 = e1[0].y
    x2 = e1[1].x
    y2 = e1[1].y
    x3 = e2[0].x
    y3 = e2[0].y
    x4 = e2[1].x
    y4 = e2[1].y
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return None
    t1 = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    t2 = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        x = x1 + t1 * (x2 - x1)
        y = y1 + t1 * (y2 - y1)
        return Point(x, y)
    return None


def found_adjacent(T, V, triangles_o):
    if is_in_map(triangles_o[0], T) and is_in_map(triangles_o[1], T):
        if not is_added((triangles_o[0], triangles_o[1]), V):
            V.edges.add((triangles_o[0], triangles_o[1]))

    elif is_in_map(triangles_o[0], T) and not is_in_map(triangles_o[1], T):
        map_edges = [(T.map_vertexes[0], T.map_vertexes[1]), (T.map_vertexes[1], T.map_vertexes[2]),
                     (T.map_vertexes[2], T.map_vertexes[3]), (T.map_vertexes[3], T.map_vertexes[0])]
        for map_edge in map_edges:
            intersection_point = check_intersection(
                (triangles_o[0], triangles_o[1]), map_edge)
            if intersection_point:
                V.edges.add((triangles_o[0], intersection_point))
                break

    elif not is_in_map(triangles_o[0], T) and is_in_map(triangles_o[1], T):
        map_edges = [(T.map_vertexes[0], T.map_vertexes[1]), (T.map_vertexes[1], T.map_vertexes[2]),
                     (T.map_vertexes[2], T.map_vertexes[3]), (T.map_vertexes[3], T.map_vertexes[0])]
        for map_edge in map_edges:
            intersection_point = check_intersection(
                (triangles_o[0], triangles_o[1]), map_edge)
            if intersection_point:
                V.edges.add((triangles_o[1], intersection_point))
                break

    elif not is_in_map(triangles_o[0], T) and not is_in_map(triangles_o[1], T):
        map_edges = [(T.map_vertexes[0], T.map_vertexes[1]), (T.map_vertexes[1], T.map_vertexes[2]),
                     (T.map_vertexes[2], T.map_vertexes[3]), (T.map_vertexes[3], T.map_vertexes[0])]
        intersection_points = []
        for map_edge in map_edges:
            intersection_point = check_intersection(
                (triangles_o[0], triangles_o[1]), map_edge)
            if intersection_point:
                intersection_points.append(intersection_point)
        if len(intersection_points) == 2:
            V.edges.add((intersection_points[0], intersection_points[1]))


# Dla point będącego triangle.o funkcja zwraca półprostą (odcinek) z początkiem w point, prostopadłą do triangle_edge
def get_parallel_line(triangle_edge, point):
    middle_point = Point(
        (triangle_edge[0].x + triangle_edge[1].x)/2, (triangle_edge[0].y + triangle_edge[1].y)/2)
    e0 = point
    e1 = Point(point.x + 1e8 * (middle_point.x - point.x),
               point.y + 1e8 * (middle_point.y - point.y))
    return (e0, e1)

# Zwraca półprostą (odcinek) przeciwną do parallel_line


def get_opposite_parallel_line(triangle_edge, point):
    middle_point = Point(
        (triangle_edge[0].x + triangle_edge[1].x)/2, (triangle_edge[0].y + triangle_edge[1].y)/2)
    e0 = point
    e1 = Point(point.x + 1e8 * (point.x - middle_point.x),
               point.y + 1e8 * (point.y - middle_point.y))
    return (e0, e1)


def not_found_adjacent(T, V, triangle_edge, triangle):
    map_edges = [(T.map_vertexes[0], T.map_vertexes[1]), (T.map_vertexes[1], T.map_vertexes[2]),
                 (T.map_vertexes[2], T.map_vertexes[3]), (T.map_vertexes[3], T.map_vertexes[0])]
    if triangle.o in triangle:
        parallel_line = get_parallel_line(triangle_edge, triangle.o)
        for map_edge in map_edges:
            intersection_point = check_intersection(parallel_line, map_edge)
            if intersection_point:
                V.edges.add((triangle.o, intersection_point))
                break
    else:
        # Jeśli punkt znajduje się po prawej stronie odcinka triangle_edge (poza trójkątem) to odcinek przeciwny do parallel_line
        if mat_det_3x3(triangle_edge[0], triangle_edge[1], triangle.o) < 0:
            opposite_parallel_line = get_opposite_parallel_line(
                triangle_edge, triangle.o)
            for map_edge in map_edges:
                intersection_point = check_intersection(
                    opposite_parallel_line, map_edge)
                if intersection_point:
                    V.edges.add((triangle.o, intersection_point))
                    break
    # Jeśli punkt znajduje się po lewej stronie odcinka triangle_edge (poza trójkątem) to parallel_line
        else:
            parallel_line = get_parallel_line(triangle_edge, triangle.o)
            intersection_points = []
            for map_edge in map_edges:
                intersection_point = check_intersection(
                    parallel_line, map_edge)
                if intersection_point:
                    intersection_points.append(intersection_point)
            if len(intersection_points) == 1:
                V.edges.add((triangle.o, intersection_points[0]))
            elif len(intersection_points) == 2:
                V.edges.add((intersection_points[0], intersection_points[1]))


def add_edgeV_no_triangles(V, edge, map_edges):
    x1 = edge[0].x
    y1 = edge[0].y
    x2 = edge[1].x
    y2 = edge[1].y
    left_x = map_edges[0][0].x - 1
    right_x = map_edges[0][1].x + 1
    if x1 == x2:
        new_y = (y1 + y2)/2
        line = (Point(left_x, new_y), Point(right_x, new_y))
        intersection_points = [None for _ in range(2)]
        intersection_points[0] = check_intersection(line, map_edges[1])
        intersection_points[1] = check_intersection(line, map_edges[3])
        V.edges.add((intersection_points[0], intersection_points[1]))
    elif y1 == y2:
        down_y = map_edges[0][0].y - 1
        up_y = map_edges[1][1].y + 1
        new_x = (x1 + x2)/2
        line = (Point(new_x, down_y), Point(new_x, up_y))
        intersection_points = [None for _ in range(2)]
        intersection_points[0] = check_intersection(line, map_edges[0])
        intersection_points[1] = check_intersection(line, map_edges[2])
        V.edges.add((intersection_points[0], intersection_points[1]))
    else:
        a = -1 / ((y2 - y1) / (x2 - x1))
        b = ((y1 + y2)/2) - (a * ((x1 + x2)/2))
        line = (Point(left_x, a*left_x + b), Point(right_x, a*right_x + b))
        intersection_points = []
        for map_edge in map_edges:
            intersection_point = check_intersection(line, map_edge)
            if intersection_point:
                intersection_points.append(intersection_point)
        V.edges.add((intersection_points[0], intersection_points[1]))


def no_triangles(T, V, Points):
    V.edges.clear()
    Points_sorted = sorted(Points, key=lambda point: (point[1], point[0]))
    P = get_points(Points_sorted)
    map_edges = [(T.map_vertexes[0], T.map_vertexes[1]), (T.map_vertexes[1], T.map_vertexes[2]),
                 (T.map_vertexes[2], T.map_vertexes[3]), (T.map_vertexes[3], T.map_vertexes[0])]
    for i in range(1, len(P)):
        add_edgeV_no_triangles(V, (P[i-1], P[i]), map_edges)


# Funkcja dodająca krawędź pomiędzy triangle i drugim trójkątem o krawędzi triangle_edge
def add_edgeV(T, V, triangle_edge, triangle):
    # pierwszy element - triangle, drugi - jego sąsiad
    triangles_o = get_triangles_o(triangle, triangle_edge, T)
    if len(triangles_o) == 2:
        found_adjacent(T, V, triangles_o)
    elif len(triangles_o) == 1:
        not_found_adjacent(T, V, triangle_edge, triangle)


def voronoi(T, Points):
    V = Voronoi()
    T.adjust_map_size()

    for triangle in T.triangles:
        add_edgeV(T, V, (triangle.p1, triangle.p2), triangle)
        add_edgeV(T, V, (triangle.p2, triangle.p3), triangle)
        add_edgeV(T, V, (triangle.p3, triangle.p1), triangle)

    if len(T.triangles) == 0:
        no_triangles(T, V, Points)

    map_edges = [(T.map_vertexes[0], T.map_vertexes[1]), (T.map_vertexes[1], T.map_vertexes[2]),
                 (T.map_vertexes[2], T.map_vertexes[3]), (T.map_vertexes[3], T.map_vertexes[0])]
    for edge in map_edges:
        V.edges.add(edge)

    return V.edges
