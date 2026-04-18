from transforms import transform_x, transform_y, transform_z
from utils import CORNERS, EDGES, CENTRES

from copy import deepcopy as dcpy

class Cube:
    def __init__(self):
        self.CORNERS_PERM = dcpy(CORNERS)
        self.EDGES_PERM = dcpy(EDGES)
        self.CENTRES = dcpy(CENTRES)

    def get_all_cubies(self):
        return self.CENTRES + self.EDGES_PERM + self.CORNERS_PERM

    def U(self, inv):
        def transform(minic):
            y = minic.coords[1]
            if y == -1:
                minic = transform_y(minic, not inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
        self.CENTRES = [transform(centre) for centre in self.CENTRES]
    
    def D(self, inv: bool):
        def transform(minic):
            y = minic.coords[1]
            if y == 1:
                minic = transform_y(minic, inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
        self.CENTRES = [transform(centre) for centre in self.CENTRES]

    def R(self, inv: bool):
        def transform(minic):
            x = minic.coords[0]
            if x == 1:
                minic = transform_x(minic, not inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
        self.CENTRES = [transform(centre) for centre in self.CENTRES]

    def L(self, inv: bool):
        def transform(minic):
            x = minic.coords[0]
            if x == -1:
                minic = transform_x(minic, inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
        self.CENTRES = [transform(centre) for centre in self.CENTRES]

    def F(self, inv: bool):
        def transform(minic):
            z = minic.coords[2]
            if z == -1:
                minic = transform_z(minic, not inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
        self.CENTRES = [transform(centre) for centre in self.CENTRES]
    
    def B(self, inv: bool):
        def transform(minic):
            z = minic.coords[2]
            if z == 1:
                minic = transform_z(minic, inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
        self.CENTRES = [transform(centre) for centre in self.CENTRES]
