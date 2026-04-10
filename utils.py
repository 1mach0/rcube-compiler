class Cubie:
    def __init__(self, pos: tuple, or_x: tuple, or_y: tuple, or_z: tuple):
        self.coords = pos
        self.orient = (or_x, or_y, or_z)

CORNERS = []
for z in [-1, 1]:
   for y in [-1, 1]:
      for x in [-1, 1]:
         cubie = Cubie(
            (x, y, z),
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
         )
         CORNERS.append(cubie)

EDGES = []
for z in [-1, 0, 1]:
   for y in [-1, 0, 1]:
      for x in [-1, 0, 1]:
         if (x + y + z) % 2 == 0 and (x or y or z):
            cubie = Cubie(
               (x, y, z),
               (1, 0, 0),
               (0, 1, 0),
               (0, 0, 1)
            )
            EDGES.append(cubie)

def neg_vec(v):
   return (-v[0], -v[1], -v[2])