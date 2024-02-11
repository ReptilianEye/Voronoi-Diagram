from math import sqrt
EPS = 1e-8


def mat_det_3x3(p1, p2, p3):
    det = (p2.x - p1.x)*(p3.y - p2.y) - (p2.y - p1.y)*(p3.x - p2.x)
    if det > EPS:
        return 1
    elif det < -EPS:
        return -1
    else:
        return 0
    # return == -1 -> p3 po prawej stronie prostej (p1,p2)
    # return == -1 -> punkty zgodnie z ruchem wskazówek zegara


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, p):
        return sqrt((self.x - p.x)**2 + (self.y - p.y)**2)


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.o, self.R = self.set_circle()

    def __contains__(self, p):
        # Pozwala na sprawdzenie, czy punkt zawiera się w trójkącie
        a12 = mat_det_3x3(self.p1, self.p2, self.p3)
        b12 = mat_det_3x3(self.p1, self.p2, p)
        a23 = mat_det_3x3(self.p2, self.p3, self.p1)
        b23 = mat_det_3x3(self.p2, self.p3, p)
        a31 = mat_det_3x3(self.p3, self.p1, self.p2)
        b31 = mat_det_3x3(self.p3, self.p1, p)
        return (a12 * b12 >= 0) and (a23 * b23 >= 0) and (a31 * b31 >= 0)

    def __eq__(self, other):
        if self is None or other is None:
            return False
        S_points = {self.p1, self.p2, self.p3}
        O_points = {other.p1, other.p2, other.p3}
        return S_points == O_points

    def __hash__(self):
        return hash((self.p1, self.p2, self.p3))

    def set_circle(self):
        s1 = self.p1.x**2 + self.p1.y**2
        s2 = self.p2.x**2 + self.p2.y**2
        s3 = self.p3.x**2 + self.p3.y**2
        x13 = self.p1.x - self.p3.x
        x32 = self.p3.x - self.p2.x
        x21 = self.p2.x - self.p1.x
        y12 = self.p1.y - self.p2.y
        y23 = self.p2.y - self.p3.y
        y31 = self.p3.y - self.p1.y
        f = 2*(self.p1.x*y23 + self.p2.x*y31 + self.p3.x*y12)
        # Okręg opisany na trójkącie ma środek:
        x0 = (s1*y23 + s2*y31 + s3*y12)/f
        y0 = (s1*x32 + s2*x13 + s3*x21)/f
        # Promień okręgu opisanego na trójkącie wynosi:
        R = sqrt((x21**2 + y12**2) * (x13**2 + y31**2)
                 * (x32**2 + y23**2))/abs(f)
        return Point(x0, y0), R

    def in_circle(self, p):
        if self.o.distance(p) <= self.o.distance(self.p1) - EPS:
            return True
        else:
            return False

    # Sortuje punkty, aby były przeciwnie do ruchu wskzówek zegara,
    # tak że p1 jest najniższym punktem (najbardziej po lewej)
    def sort_tri_vertexes(self):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3
        if mat_det_3x3(p1, p2, p3) < 0:
            p1, p2 = p2, p1
        while (p1.y > min(p2.y, p3.y) or (p1.y == min(p2.y, p3.y) and p1.y != p2.y)):
            p1, p2, p3 = p2, p3, p1
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def get_edges(self):
        edges = set()
        self.sort_tri_vertexes()
        edges.add((self.p1, self.p2))
        edges.add((self.p2, self.p3))
        edges.add((self.p3, self.p1))
        return edges


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, p):
        return sqrt((self.x - p.x)**2 + (self.y - p.y)**2)
