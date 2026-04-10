from models import Cubie

CORNERS = []
for z in [-1, 1]:
   for y in [-1, 1]:
      for x in [-1, 1]:
         cubie = Cubie()
         cubie.coords = [x, y, z]
         cubie.orient = []
         CORNERS.append([x, y, z])

EDGES = []
for z in [-1, 0, 1]:
   for y in [-1, 0, 1]:
      for x in [-1, 0, 1]:
         if (x + y + z) % 2 == 0 and (x or y or z):
            EDGES.append([x, y, z])

def neg_vec(v):
   return (-v[0], -v[1], -v[2])