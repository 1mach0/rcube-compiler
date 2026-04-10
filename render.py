from models import Cube

rub = Cube()
for cubelet in rub.CORNERS_PERM:
    print(cubelet.coords)

rub.U(inv=False)

for cubelet in rub.CORNERS_PERM:
    print(cubelet.coords)