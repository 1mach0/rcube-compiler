import numpy as np
import mujoco
import mujoco.viewer

from models import Cube
from utils import orient_to_matrix

SCALE = 0.04

def quat_mul(q1, q2):
    # Hamilton product
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def axis_angle_to_quat(axis, angle):
    axis = np.array(axis)
    axis = axis / np.linalg.norm(axis)

    s = np.sin(angle / 2)
    return np.array([
        np.cos(angle / 2),
        axis[0]*s,
        axis[1]*s,
        axis[2]*s
    ])

def to_pos(coords):
    return np.array([SCALE * c for c in coords])

def get_subset(model, cubies, subset=None, colors=None):
    result = []

    for i, cubie in enumerate(cubies):
        mocap_id = model.body_mocapid[body_id]
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, mocap_id)

        if subset:
            if subset == "centers" and not name.startswith("c_"):
                continue
            if subset == "edges" and not name.startswith("e_"):
                continue
            if subset == "corners" and not name.startswith("x_"):
                continue

        if colors:
            # e.g. ["y"] or ["y","b"]
            if not any(c in name for c in colors):
                continue

        result.append(cubie)

    return result

def apply_cube_to_mujoco(cube, model, data):
    cubies = cube.get_all_cubies()

    for i, cubie in enumerate(cubies):
        data.mocap_pos[i] = to_pos(cubie.coords)

model = mujoco.MjModel.from_xml_path("Cube.xml")
data = mujoco.MjData(model)

rub = Cube()

for body_id in range(model.nbody):
    name = mujoco.mj_id2name(
        model,
        mujoco.mjtObj.mjOBJ_BODY,
        body_id
    )
    print(body_id, name)

cubies = rub.get_all_cubies()

blue_face = get_subset(model=model, cubies=cubies, subset="b")
q_rot = axis_angle_to_quat([1, 0, 0], 3 * np.pi / 2)
for i, cubie in enumerate(blue_face):
    data.mocap_quat[i] = quat_mul(q1=data.mocap_quat[i], q2=q_rot)

yellow_face = get_subset(model=model, cubies=cubies, subset="y")
q_rot = axis_angle_to_quat([0, 0, 1], np.pi / 2)
for i, cubie in enumerate(yellow_face):
    data.mocap_quat[i] = quat_mul(q1=data.mocap_quat[i], q2=q_rot)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        apply_cube_to_mujoco(rub, model=model, data=data)
        mujoco.mj_forward(model, data)
        viewer.sync()