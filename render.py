import numpy as np
import mujoco
import mujoco.viewer
import time
import random

from models import Cube

SCALE = 0.04
ANIMATION_DURATION = 0.25  # seconds

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

def quat_mul(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def mat2quat(R):
    tr = np.trace(R)
    if tr > 0:
        S = np.sqrt(tr + 1.0) * 2
        qw = 0.25 * S
        qx = (R[2, 1] - R[1, 2]) / S
        qy = (R[0, 2] - R[2, 0]) / S
        qz = (R[1, 0] - R[0, 1]) / S
    elif (R[0, 0] > R[1, 1]) and (R[0, 0] > R[2, 2]):
        S = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        qw = (R[2, 1] - R[1, 2]) / S
        qx = 0.25 * S
        qy = (R[0, 1] + R[1, 0]) / S
        qz = (R[0, 2] + R[2, 0]) / S
    elif R[1, 1] > R[2, 2]:
        S = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        qw = (R[0, 2] - R[2, 0]) / S
        qx = (R[0, 1] + R[1, 0]) / S
        qy = 0.25 * S
        qz = (R[1, 2] + R[2, 1]) / S
    else:
        S = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        qw = (R[1, 0] - R[0, 1]) / S
        qx = (R[0, 2] + R[2, 0]) / S
        qy = (R[1, 2] + R[2, 1]) / S
        qz = 0.25 * S
    return np.array([qw, qx, qy, qz])

def rotate_vec(v, q):
    w, x, y, z = q
    q_vec = np.array([x, y, z])
    return v + 2.0 * np.cross(q_vec, np.cross(q_vec, v) + w * v)

def to_pos(coords):
    return np.array([SCALE * c for c in coords])

def get_subset(model, cubies, subset=None, colors=None):
    result = []
    for i, cubie in enumerate(cubies):
        mocap_id = model.body_mocapid[i]
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, mocap_id)
        if subset:
            if subset == "centers" and not name.startswith("c_"):
                continue
            if subset == "edges" and not name.startswith("e_"):
                continue
            if subset == "corners" and not name.startswith("x_"):
                continue
        if colors:
            if not any(c in name for c in colors):
                continue
        result.append(cubie)
    return result

def convert_to_correct_orientation(model, cubies):
    blue_face = get_subset(model=model, cubies=cubies, subset="b")
    q_rot = axis_angle_to_quat([1, 0, 0], 3 * np.pi / 2)
    for i, cubie in enumerate(blue_face):
        data.mocap_quat[i] = quat_mul(q1=data.mocap_quat[i], q2=q_rot)

    yellow_face = get_subset(model=model, cubies=cubies, subset="y")
    q_rot = axis_angle_to_quat([0, 0, 1], np.pi / 2)
    for i, cubie in enumerate(yellow_face):
        data.mocap_quat[i] = quat_mul(q1=data.mocap_quat[i], q2=q_rot)

    return data

def get_rotation_axis(move_name, inv):
    if move_name == 'U': return np.array([0, -1, 0]) if not inv else np.array([0, 1, 0])
    elif move_name == 'D': return np.array([0, 1, 0]) if not inv else np.array([0, -1, 0])
    elif move_name == 'R': return np.array([1, 0, 0]) if not inv else np.array([-1, 0, 0])
    elif move_name == 'L': return np.array([-1, 0, 0]) if not inv else np.array([1, 0, 0])
    elif move_name == 'F': return np.array([0, 0, -1]) if not inv else np.array([0, 0, 1])
    elif move_name == 'B': return np.array([0, 0, 1]) if not inv else np.array([0, 0, -1])
    return np.array([0, 0, 0])

def is_cubie_on_face(cubie_coords, move_name):
    x, y, z = cubie_coords
    if move_name == 'U': return y == -1
    elif move_name == 'D': return y == 1
    elif move_name == 'R': return x == 1
    elif move_name == 'L': return x == -1
    elif move_name == 'F': return z == -1
    elif move_name == 'B': return z == 1
    return False

def get_tangent(face_name, is_ccw, p0):
    if face_name == 'U': axis = np.array([0, -1, 0])
    elif face_name == 'D': axis = np.array([0, 1, 0])
    elif face_name == 'R': axis = np.array([1, 0, 0])
    elif face_name == 'L': axis = np.array([-1, 0, 0])
    elif face_name == 'F': axis = np.array([0, 0, -1])
    elif face_name == 'B': axis = np.array([0, 0, 1])
    else: return np.array([0, 0, 0])
    
    tangent = np.cross(axis, p0)
    if is_ccw:
        tangent = -tangent
    return tangent

# Shared state
move_queue = []
current_move = None
dragging = False
drag_cubie_idx = None
drag_start_pos = None

# Cube representation
rub = Cube()
cubies = rub.get_all_cubies()

def apply_cube_to_mujoco(cubies, data):
    for i, cubie in enumerate(cubies):
        if dragging and i == drag_cubie_idx:
            continue  # Let MuJoCo's perturbation control the dragged cubie
        
        # Position in Cube frame
        data.mocap_pos[i] = to_pos(cubie.coords)
        
        # Local orientation quaternion from basis vectors (row stacked)
        R_local = np.array(cubie.orient)
        q_local = mat2quat(R_local)
        
        # Compose local orientation with initial corrected orientation
        data.mocap_quat[i] = quat_mul(q_local, initial_quats[i])

def key_callback(keycode):
    global rub, current_move, move_queue, dragging
    
    # Handle moves: lowercase for CW, uppercase (Shift + key) for CCW
    if keycode in [85, 117]:    # U / u
        move_queue.append(('U', keycode == 85))
    elif keycode in [68, 100]:  # D / d
        move_queue.append(('D', keycode == 68))
    elif keycode in [82, 114]:  # R / r
        move_queue.append(('R', keycode == 82))
    elif keycode in [76, 108]:  # L / l
        move_queue.append(('L', keycode == 76))
    elif keycode in [70, 102]:  # F / f
        move_queue.append(('F', keycode == 70))
    elif keycode in [66, 98]:   # B / b
        move_queue.append(('B', keycode == 66))
    elif keycode == 32:  # Space - scramble
        print("Scrambling cube...")
        faces = ['U', 'D', 'R', 'L', 'F', 'B']
        for _ in range(20):
            move_queue.append((random.choice(faces), random.choice([True, False])))
    elif keycode in [13, 27]:  # Enter or Esc - reset
        print("Resetting cube to solved state...")
        rub = Cube()
        current_move = None
        move_queue.clear()
        dragging = False
        apply_cube_to_mujoco(rub.get_all_cubies(), data)

# Initialize models
model = mujoco.MjModel.from_xml_path("cube_model/Cube.xml")
data = mujoco.MjData(model)

# Map MuJoCo body ID to our cubies list index
body_to_cubie = {}
for idx in range(len(cubies)):
    for body_id in range(model.nbody):
        if model.body_mocapid[body_id] == idx:
            body_to_cubie[body_id] = idx
            break

# Initialize corrected orientations from original developer logic
data = convert_to_correct_orientation(model, cubies)
initial_quats = [np.copy(data.mocap_quat[i]) for i in range(len(cubies))]

# Set initial pos/quat of all cubies
apply_cube_to_mujoco(cubies, data)

print("="*60)
print("Rubik's Cube Engine - MuJoCo Renderer")
print("="*60)
print("Keyboard Controls:")
print("  - u / U: Rotate U face (lowercase=CW, Shift+U=CCW)")
print("  - d / D: Rotate D face (lowercase=CW, Shift+D=CCW)")
print("  - r / R: Rotate R face (lowercase=CW, Shift+R=CCW)")
print("  - l / L: Rotate L face (lowercase=CW, Shift+L=CCW)")
print("  - f / F: Rotate F face (lowercase=CW, Shift+F=CCW)")
print("  - b / B: Rotate B face (lowercase=CW, Shift+B=CCW)")
print("  - Space: Scramble the cube randomly")
print("  - Enter / Esc: Reset cube to solved state")
print("Mouse Controls:")
print("  - Ctrl + Left Click & Drag: Drag any edge/corner cubie to rotate face")
print("="*60)

# Move functions dictionary
MOVE_FUNCS = {
    'U': lambda cube, inv: cube.U(inv),
    'D': lambda cube, inv: cube.D(inv),
    'R': lambda cube, inv: cube.R(inv),
    'L': lambda cube, inv: cube.L(inv),
    'F': lambda cube, inv: cube.F(inv),
    'B': lambda cube, inv: cube.B(inv),
}

with mujoco.viewer.launch_passive(model, data, key_callback=key_callback) as viewer:
    while viewer.is_running():
        now = time.time()
        
        # 1. Handle mouse dragging interaction
        if viewer.perturb.active:
            if not dragging:
                select_id = viewer.perturb.select
                if select_id in body_to_cubie:
                    drag_cubie_idx = body_to_cubie[select_id]
                    drag_start_pos = np.copy(data.mocap_pos[drag_cubie_idx])
                    dragging = True
        else:
            if dragging:
                # User released drag, compute displacement
                end_pos = np.copy(data.mocap_pos[drag_cubie_idx])
                displacement = end_pos - drag_start_pos
                dist = np.linalg.norm(displacement)
                
                # Check for significant drag
                if dist > 0.012 and current_move is None:
                    # Displacement is already in local/aligned frame
                    disp_local = displacement
                    p0 = cubies[drag_cubie_idx].coords
                    
                    # Edges or corners only
                    if np.sum(np.abs(p0) == 1) >= 2:
                        candidate_faces = [face for face in ['U', 'D', 'R', 'L', 'F', 'B'] if is_cubie_on_face(p0, face)]
                        best_move = None
                        best_dot = -1.0
                        
                        for face in candidate_faces:
                            for inv in [False, True]:
                                tangent = get_tangent(face, inv, p0)
                                dot = np.dot(disp_local, tangent)
                                if dot > best_dot:
                                    best_dot = dot
                                    best_move = (face, inv)
                        
                        if best_move and best_dot > 0.005:
                            move_queue.append(best_move)
                
                dragging = False
                drag_cubie_idx = None
                apply_cube_to_mujoco(cubies, data)
        
        # 2. Process animation queue & state machine
        if current_move is None:
            if len(move_queue) > 0 and not dragging:
                move_name, inv = move_queue.pop(0)
                # Store start state for interpolation
                start_coords = [np.copy(c.coords) for c in cubies]
                # Store start quaternions in world frame
                start_quats = [np.copy(data.mocap_quat[i]) for i in range(len(cubies))]
                
                current_move = {
                    'name': move_name,
                    'inv': inv,
                    'axis': get_rotation_axis(move_name, inv),
                    'start_time': now,
                    'start_coords': start_coords,
                    'start_quats': start_quats
                }
        
        if current_move is not None:
            dt = now - current_move['start_time']
            if dt < ANIMATION_DURATION:
                # Interpolate angle from 0 to pi/2 (90 degrees)
                theta = (np.pi / 2.0) * (dt / ANIMATION_DURATION)
                q_rot = axis_angle_to_quat(current_move['axis'], theta)
                
                # Apply rotation to cubies on the moving face
                for i in range(len(cubies)):
                    start_pos_local = to_pos(current_move['start_coords'][i])
                    start_q_world = current_move['start_quats'][i]
                    
                    if is_cubie_on_face(current_move['start_coords'][i], current_move['name']):
                        # Position: rotate locally
                        data.mocap_pos[i] = rotate_vec(start_pos_local, q_rot)
                        
                        # Orientation: rotate locally in world frame
                        data.mocap_quat[i] = quat_mul(q_rot, start_q_world)
                    else:
                        # Stationary cubies
                        data.mocap_pos[i] = start_pos_local
                        data.mocap_quat[i] = start_q_world
            else:
                # End of animation: apply state update to models
                MOVE_FUNCS[current_move['name']](rub, current_move['inv'])
                current_move = None
                apply_cube_to_mujoco(cubies, data)
        else:
            # If no animation is active, make sure positions/orientations match the current state
            apply_cube_to_mujoco(cubies, data)
            
        mujoco.mj_forward(model, data)
        viewer.sync()
        
        # Limit loop rate
        time.sleep(0.005)