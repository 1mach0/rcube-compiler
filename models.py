from transforms import transform_x, transform_y, transform_z
from utils import CORNERS, EDGES, CENTRES

class Cube:
    def __init__(self):
        self.CORNERS_PERM = CORNERS
        self.EDGES_PERM = EDGES
        self.CENTRES = CENTRES

    def move(self, move_name):
        "redirect to proper channel"
        pass

    def U(self, inv):
        def transform(minic):
            y = minic.coords[1]
            if y == -1:
                minic = transform_y(minic, not inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
    
    def D(self, inv: bool):
        def transform(minic):
            y = minic.coords[1]
            if y == 1:
                minic = transform_y(minic, inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]

    def R(self, inv: bool):
        def transform(minic):
            x = minic.coords[0]
            if x == 1:
                minic = transform_x(minic, not inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
    
    def L(self, inv: bool):
        def transform(minic):
            x = minic.coords[0]
            if x == -1:
                minic = transform_x(minic, inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]

    def F(self, inv: bool):
        def transform(minic):
            z = minic.coords[2]
            if z == -1:
                minic = transform_z(minic, not inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
    
    def B(self, inv: bool):
        def transform(minic):
            z = minic.coords[2]
            if z == 1:
                minic = transform_z(minic, inv)
            return minic
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
