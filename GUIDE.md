# Rubik's Cube Coordinate & State Guide

This document serves as a reference for the coordinate system, piece indexing, and orientation states used throughout this project.

---

## Center Piece Mapping

Purely a subjective choice, this project follows the `CFOP` convention.

| Face | Color | Coordinate/Direction |
| :--- | :--- | :--- |
| **U** | Yellow | Up |
| **D** | White | Down |
| **F** | Blue | Front |
| **B** | Green | Back |
| **R** | Red | Right |
| **L** | Orange | Left |

---

## Corners

### Permutation (Positioning)
Corners are indexed `0-7` based on their 3D spatial coordinates.

| Index | Coordinates (x, y, z) | Faces | Name |
| :---: | :---: | :---: | :--- |
| **0** | (-1, -1, -1) | L, U, F | Left-Up-Front |
| **1** | ( 1, -1, -1) | R, U, F | Right-Up-Front |
| **2** | (-1,  1, -1) | L, D, F | Left-Down-Front |
| **3** | ( 1,  1, -1) | R, D, F | Right-Down-Front |
| **4** | (-1, -1,  1) | L, U, B | Left-Up-Back |
| **5** | ( 1, -1,  1) | R, U, B | Right-Up-Back |
| **6** | (-1,  1,  1) | L, D, B | Left-Down-Back |
| **7** | ( 1,  1,  1) | R, D, B | Right-Down-Back |

### Orientation (Rotation)
| Value | State | Description |
| :---: | :--- | :--- |
| **0** | Normal | Correct orientation |
| **1** | Clockwise | Twisted once clockwise |
| **2** | Anti-Clockwise | Twisted once counter-clockwise |

---

## Edges

### Permutation (Positioning)
Edges are indexed `0-11` based on their 3D spatial coordinates.

| Index | Coordinates (x, y, z) | Name |
| :---: | :---: | :--- |
| **0** | ( 0, -1, -1) | **UF** (Up-Front) |
| **1** | (-1,  0, -1) | **LF** (Left-Front) |
| **2** | ( 1,  0, -1) | **RF** (Right-Front) |
| **3** | ( 0,  1, -1) | **DF** (Down-Front) |
| **4** | (-1, -1,  0) | **UL** (Up-Left) |
| **5** | ( 1, -1,  0) | **UR** (Up-Right) |
| **6** | (-1,  1,  0) | **DL** (Down-Left) |
| **7** | ( 1,  1,  0) | **DR** (Down-Right) |
| **8** | ( 0, -1,  1) | **UB** (Up-Back) |
| **9** | (-1,  0,  1) | **LB** (Left-Back) |
| **10** | ( 1,  0,  1) | **RB** (Right-Back) |
| **11** | ( 0,  1,  1) | **DB** (Down-Back) |

### Orientation (Flip)
| Value | State | Description |
| :---: | :--- | :--- |
| **0** | Normal | Edge is flipped correctly |
| **1** | Abnormal | Edge is flipped (bad edge) |
