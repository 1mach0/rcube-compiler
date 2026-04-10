from utils import neg_vec, Cubie

def transform_x(pos: Cubie, sign=True):
    x, y, z = pos.coords
    ax_x, ax_y, ax_z = pos.orient

    if sign:
        pos.coords = (x, -z, y)
        pos.orient = (ax_x, neg_vec(ax_z), ax_y)
    else:
        pos.coords = (x, z, -y)
        pos.orient = (ax_x, ax_z, neg_vec(ax_y))
    
    return pos

def transform_y(pos, sign=True):
    x, y, z = pos.coords
    ax_x, ax_y, ax_z = pos.orient
    if sign:
        pos.coords = (-z, y, x)
        pos.orient = (neg_vec(ax_z), ax_y, ax_x)
    else:
        pos.coords = (z, y, -x)
        pos.orient = (ax_z, ax_y, neg_vec(ax_x))

    return pos

def transform_z(pos, sign=True):
    x, y, z = pos.coords
    ax_x, ax_y, ax_z = pos.orient
    if sign:
        pos.coords = (y, -x, z)
        pos.orient = (ax_y, neg_vec(ax_x), ax_z)
    else:
        pos.coords = (-y, x, z)
        pos.orient = (neg_vec(ax_y), ax_x, ax_z)

    return pos