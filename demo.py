from voronoi import Voronoi
points = [(0, 0), (1, 1), (2, 3), (-1, 2.5)]
points = [
    [-4.98119373, 6.83857958],
    [-0.12778136, 6.63343697],
    [-7.33037151, 5.50546613],
    [-2.07501278, 3.20578633],
    [5.8388661, -1.68896804],
    [-3.99228758, -3.77928136],
    [9.74501677, -6.04110336],
    [0.98573669, -6.81810449],
    [5.1283655, -9.2936127],
    [8.95603584, -9.51014394],
]
vor = Voronoi(points)
plt = vor.get_voronoi()
plt.show()
print("done")
