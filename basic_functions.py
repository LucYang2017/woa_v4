# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 8:07
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : basic_functions.py

from configs import *
import random
import math


def check_boundary_3d(position):
    if position[0] < X_MIN:
        position[0] = X_MIN + abs(X_MIN - position[0]) + 0.05
    elif position[0] > X_MAX:
        position[0] = X_MAX - abs(X_MAX - position[0]) - 0.05

    if position[1] < Y_MIN:
        position[1] = Y_MIN + abs(Y_MIN - position[1]) + 0.05
    elif position[1] > Y_MAX:
        position[1] = Y_MAX - abs(Y_MAX - position[1]) - 0.05

    if position[2] < Z_MIN:
        position[2] = Z_MIN + abs(Z_MIN - position[2]) + 0.05
    elif position[2] > Z_MAX:
        position[2] = Z_MAX - abs(Z_MAX - position[2]) - 0.05

    position[0] = round(position[0], 2)
    position[1] = round(position[1], 2)
    position[2] = round(position[2], 2)
    return position
