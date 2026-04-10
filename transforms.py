from models import Cubie

def transform_x(pos: Cubie, sign=True):
    x, y, z = pos.coords
    if sign:
        pos.coords = (x, -z, y)
    else:
        pos.coords = (x, z, -y)
    
    ax_x, ax_y, ax_z = pos.orient
    if sign:
        pos.orient = (ax_x, not ax_z, ax_y)
    else:
        pos.orient = (ax_x, ax_z, not ax_y)

    return pos

def transform_y(pos, sign=True):
    x, y, z = pos
    if sign:
        pos.coords = (-z, y, x)
    else:
        pos.coords = (z, y, -x)

    ax_x, ax_y, ax_z = pos.orient
    if sign:
        pos.orient = (not ax_z, ax_y, ax_x)
    else:
        pos.orient = (ax_z, ax_y, not ax_x)

    return pos

def transform_z(pos, sign=True):
    x, y, z = pos
    if sign:
        pos.coords = (y, -x, z)
    else:
        pos.coords = (-y, x, z)

    ax_x, ax_y, ax_z = pos.orient
    if sign:
        pos.orient = (ax_y, not ax_x, ax_z)
    else:
        pos.orient = (not ax_y, ax_x, ax_z)

    return pos