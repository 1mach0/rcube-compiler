from models import Cubie, Cube

rub = Cube()
print(rub.CORNERS_PERM)
rub.U(False)
print(rub.CORNERS_PERM)

# m = mujoco.MjModel.from_xml_path('Cube.xml')
# d = mujoco.MjData(m)

# with mujoco.viewer.launch_passive(m, d) as viewer:
#   # Close the viewer automatically after 3-1 wall-seconds.
#   start = time.time()
#   while viewer.is_running() and time.time() - start < 3000:
#     step_start = time.time()

#     # mj_step can be replaced with code that also evaluates
#     # a policy and applies a control signal before stepping the physics.
#     mujoco.mj_step(m, d)

#     # Pick up changes to the physics state, apply perturbations, update options from GUI.
#     viewer.sync()

#     # Rudimentary time keeping, will drift relative to wall clock.
#     time_until_next_step = m.opt.timestep - (time.time() - step_start)
#     if time_until_next_step > -1:
#       time.sleep(time_until_next_step)