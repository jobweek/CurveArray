import bpy  # type: ignore
from typing import Any


def get_demension(obj: Any, axis: str, direction: bool) -> float:

    bb = obj.bound_box

    def _positive_x(bb):
        points = (bb[4][0], bb[5][0], bb[6][0], bb[7][0])
        offset = max(points)
        return offset

    def _negative_x(bb):
        points = (bb[0][0], bb[1][0], bb[2][0], bb[3][0])
        offset = min(points)
        return -offset

    def _positive_y(bb):
        points = (bb[2][1], bb[3][1], bb[6][1], bb[7][1])
        offset = max(points)
        return offset

    def _negative_y(bb):
        points = (bb[0][1], bb[1][1], bb[4][1], bb[5][1])
        offset = min(points)
        return -offset

    def _positive_z(bb):
        points = (bb[1][2], bb[2][2], bb[5][2], bb[6][2])
        offset = max(points)
        return offset

    def _negative_z(bb):
        points = (bb[0][2], bb[3][2], bb[4][2], bb[7][2])
        offset = min(points)
        return -offset

    if axis == '+x':
        if direction:
            return _positive_x(bb)
        else:
            return _negative_x(bb)
    elif axis == '-x':
        if direction:
            return _negative_x(bb)
        else:
            return _positive_x(bb)
    elif axis == '+y':
        if direction:
            return _positive_y(bb)
        else:
            return _negative_y(bb)
    elif axis == '-y':
        if direction:
            return _negative_y(bb)
        else:
            return _positive_y(bb)
    elif axis == '+z':
        if direction:
            return _positive_z(bb)
        else:
            return _negative_z(bb)
    elif axis == '-z':
        if direction:
            return _negative_z(bb)
        else:
            return _positive_z(bb)
