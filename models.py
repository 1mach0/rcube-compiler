from transforms import transform_x, transform_y, transform_z
from utils import CORNERS, EDGES

class Cubie:
    def __init__(self, pos_x: int, pos_y: int, pos_z: int, or_x: bool, or_y: bool, or_z: bool):
        self.coords = (pos_x, pos_y, pos_z)
        self.orient = (or_x, or_y, or_z)


class Cube:
    def __init__(self):
        self.CORNERS_PERM = CORNERS.copy()
        self.EDGES_PERM = EDGES.copy()

    def move(self, move_name):
        "redirect to proper channel"
        pass

    def U(self, inv):
        def transform(coords):
            if coords[1] == -1:
                coords = transform_y(coords, not inv)
            return coords
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
    
    def D(self, inv: bool):
        def transform(coords):
            if coords[1] == 1:
                coords = transform_y(coords, inv)
            return coords
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]

    def R(self, inv: bool):
        def transform(coords):
            if coords[0] == 1:
                coords = transform_x(coords, not inv)
            return coords
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
    
    def L(self, inv: bool):
        def transform(coords):
            if coords[0] == -1:
                coords = transform_x(coords, inv)
            return coords
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]

    def F(self, inv: bool):
        def transform(coords):
            if coords[2] == -1:
                coords = transform_z(coords, not inv)
            return coords
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
    
    def B(self, inv: bool):
        def transform(coords):
            if coords[2] == 1:
                coords = transform_z(coords, inv)
            return coords
        
        self.CORNERS_PERM = [transform(corner) for corner in self.CORNERS_PERM]
        self.EDGES_PERM = [transform(edge) for edge in self.EDGES_PERM]
