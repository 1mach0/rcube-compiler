import numpy as np
import mujoco
import mujoco.viewer

from models import Cube
from utils import orient_to_matrix


SCALE = 0.04

def to_pos(coords):
    return np.array([SCALE * c for c in coords])

def orient_to_quat(orient):
    mat = orient_to_matrix(orient)
    quat = np.zeros(4)
    mujoco.mju_mat2Quat(quat, mat.flatten())
    return quat

def apply_cube_to_mujoco(cube, data):
    cubies = cube.get_all_cubies()  # you define this

    for i, cubie in enumerate(cubies):
        data.xpos[i] = to_pos(cubie.coords)
        data.xquat[i] = orient_to_quat(cubie.orient)



model = mujoco.MjModel.from_xml_path("cube.xml")
data = mujoco.MjData(model)

rub = Cube()

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():

        # --- update cube logic ---
        # example:
        # rub.U(inv=False)

        # --- push to mujoco ---
        apply_cube_to_mujoco(rub, data)

        viewer.sync()