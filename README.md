# rcube-compiler

A lightweight Rubik's Cube state-to-visualization engine that converts abstract cube state representations into fully rendered **MuJoCo** models for simulation, visualization, and future robotic/AI applications.

---

## Overview

`rcube-compiler` is designed to bridge the gap between:

- **Discrete Rubik's Cube logic/state representations**
- **Continuous 3D rigid-body simulation in MuJoCo**

The engine maintains an internal cubie-based Rubik’s Cube representation, applies legal cube transformations, and compiles the resulting state into spatial pose/orientation data that is pushed directly into a MuJoCo scene.

---

## Motivation

This project was built to create a reusable backend for:

- Rubik’s Cube visualization
- Robotic manipulation simulation
- RL/Planning environments
- Cube-solving algorithm visualization
- State compilation for physics engines

Rather than manually animating cube turns, the system models the cube as a collection of rigid cubies and computes exact transformations for each piece.

---

## Features

- Cubie-based Rubik's Cube representation
- Full 3D coordinate/permutation tracking
- Orientation tracking via basis-vector transforms
- Support for standard cube moves:
  - `U`, `D`, `L`, `R`, `F`, `B` (clockwise and counter-clockwise)
- Automatic conversion of cube state into:
  - Position vectors
  - Rotation matrices
  - Quaternions
- Real-time MuJoCo rendering pipeline
- **Smooth face-turn animations** with configurable duration
- **Keyboard interactivity** for all standard moves, scramble, and reset
- **Mouse drag interactivity** (Ctrl+Click & Drag) to rotate faces by dragging cubies
- Animation queue for chaining multiple moves
- Modular architecture for future expansion

---

## Project Structure

```bash
rcube-compiler/
│
└── cube_model/
  ├── Cube.xml           # MuJoCo scene/model definition
  └── assets/            # Textures/materials/images
├── render.py          # MuJoCo rendering/visualization pipeline
├── models.py          # Core Cube/Cubie data structures
├── transforms.py      # Spatial rotation/transform logic
└── utils.py           # Helper math + orientation conversion

```

---


## Architecture

The project is structured in three conceptual layers:

```text
Rubik's Cube Logic Layer
        ↓
Spatial Transform Compilation Layer
        ↓
MuJoCo Rendering Layer
```

### 1. Cube Logic

Maintains abstract puzzle state:

* cubie permutation
* cubie orientation
* legal face turns

### 2. Compiler Layer

Transforms cube state into:

* Cartesian coordinates
* Rotation matrices
* Quaternion representations

### 3. Renderer

Pushes compiled transforms into MuJoCo mocap bodies for visualization.

---

## Example Pipeline

```python
rub = Cube()

rub.U(inv=False)
rub.R(inv=True)

apply_cube_to_mujoco(rub, data)
```

---

## Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

---

## Running

Launch the MuJoCo renderer (requires `mjpython` on macOS):

```bash
mjpython -m render
```

---

## Controls

### Keyboard

| Key | Action |
| :---: | :--- |
| `u` / `U` | Rotate U face (CW / CCW) |
| `d` / `D` | Rotate D face (CW / CCW) |
| `r` / `R` | Rotate R face (CW / CCW) |
| `l` / `L` | Rotate L face (CW / CCW) |
| `f` / `F` | Rotate F face (CW / CCW) |
| `b` / `B` | Rotate B face (CW / CCW) |
| `Space` | Scramble the cube (20 random moves) |
| `Enter` / `Esc` | Reset cube to solved state |

### Mouse

- **Ctrl + Left Click & Drag** on any edge or corner cubie to rotate the corresponding face in the direction of the drag.

---

## Status

✅ All planned features have been implemented:

- [x] Cubie-based state representation and transforms
- [x] MuJoCo rendering pipeline
- [x] Smooth turn interpolation/animation
- [x] Keyboard move interactivity
- [x] Mouse drag interactivity

---

## Long-Term Goal

The eventual goal is to evolve `rcube-compiler` into a generalized:

> **Discrete-to-Continuous Puzzle/Manipulation Compilation Engine**

starting with Rubik’s Cube representations and extending toward broader robotic simulation tasks.

---

## License

MIT License