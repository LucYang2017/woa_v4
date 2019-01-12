# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 8:13
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : field.py


import numpy as np
from configs import *
from scipy.interpolate import griddata
import print_colors
import math


def scinum_2_float(sci_num):
    """
    转换科学计数法的数字或字符串为浮点类型,E的大小写区别可能造成报错
    :param sci_num: 科学计数法表达的数字，类型一般是字符串，比如 6.0000000e+000 "3.4717316e-009"
    :return: 返回浮点类型的数字
    """
    sci_num = str(sci_num)
    base = float(sci_num.split('E')[0])
    power = float(sci_num.split('E')[1])
    return base * pow(10, power)


def generate_raw_field(file_name):
    raw_data = open('data/' + str(FIELD_TYPE) + '/' + str(file_name) + '.txt', 'r', encoding='utf-8').readlines()[1:]
    raw_field = []
    # for i in range(len(raw_data)):  # 这个for用于处理有风速信息的数据
    #     msg = raw_data[i].split(',')[1:]
    #     if round(scinum_2_float(msg[1]), 2) == height:
    #         x_coordinate = round(scinum_2_float(msg[0]), 2)
    #         y_coordinate = round(scinum_2_float(msg[1]), 2)
    #         z_coordinate = round(scinum_2_float(msg[2]), 2)
    #         position = [x_coordinate, y_coordinate, z_coordinate]
    #         x_airflow_velocity = scinum_2_float(msg[3])
    #         y_airflow_velocity = scinum_2_float(msg[4])
    #         z_airflow_velocity = scinum_2_float(msg[5])
    #         airflow_velocity = [x_airflow_velocity, y_airflow_velocity, z_airflow_velocity]
    #         concentration = [round(scinum_2_float(msg[6]), 3)]
    #         node_msg = position + airflow_velocity + concentration
    #         node_msgs.append(node_msg)
    for i in range(len(raw_data)):  # 用于处理没有风速信息的数据
        msg = raw_data[i].split(',')[1:]
        x_coordinate = round(scinum_2_float(msg[0]), 2)
        y_coordinate = round(scinum_2_float(msg[1]), 2)
        z_coordinate = round(scinum_2_float(msg[2]), 2)
        position = [x_coordinate, y_coordinate, z_coordinate]
        concentration = [round(scinum_2_float(msg[-1]), 3)]
        node = position + concentration
        raw_field.append(node)
    return np.array(raw_field)


def generate_empty_grid(accuracy):
    grid = []
    x_max = round(X_MAX, 2)
    x_min = round(X_MIN, 2)
    y_max = round(Y_MAX, 2)
    y_min = round(Y_MIN, 2)
    z_max = round(Z_MAX, 2)
    z_min = round(Z_MIN, 2)

    def start_end(min, max, accuracy):
        if min <= 0:
            start = int(min / accuracy) * accuracy
        else:
            start = (int(min / accuracy) + 1) * accuracy

        if max <= 0:
            end = (int(max / accuracy) - 1) * accuracy
        else:
            end = int(max / accuracy) * accuracy
        return round(start, 2), round(end, 2)

    x_start, x_end = start_end(x_min, x_max, accuracy)
    y_start, y_end = start_end(y_min, y_max, accuracy)
    z_start, z_end = start_end(z_min, z_max, accuracy)

    for i in np.arange(x_start, x_end + accuracy, accuracy):
        for j in np.arange(y_start, y_end + accuracy, accuracy):
            for k in np.arange(z_start, z_end + accuracy, accuracy):
                grid.append([i, j, k])

    # print('%f %f %f %f %f %f' % (x_start, x_end, y_start, y_end, z_start, z_end))
    # print(np.array(grid))
    return np.array(grid)


def generate_field(raw_field, empty_grid):
    grid_c = griddata(raw_field[:, :3], raw_field[:, 3], empty_grid, method='linear')
    for c in grid_c:
        if np.isnan(c):
            c = 0
    field = np.column_stack((empty_grid, grid_c))
    return field


def save_field(field, file_name):
    import pickle as p
    f = open('field/' + str(FIELD_TYPE) + '/' + str(file_name) + '.data', 'wb')
    p.dump(field, f)
    f.close()


def query_c(positions, field):
    accuracy = abs(field[0][2] - field[1][2])

    x_max = field[-1][0]
    x_min = field[0][0]
    y_max = field[-1][1]
    y_min = field[0][1]
    z_max = field[-1][2]
    z_min = field[0][2]

    x_total = (x_max - x_min) / accuracy + 1
    y_total = (y_max - y_min) / accuracy + 1
    z_total = (z_max - z_min) / accuracy + 1

    c_array = []

    def get_nearest_coordinate_value(coordinate_value, coordinate_min, coordinate_max):
        d_min = float('inf')
        nearest_coordinate_value = 0

        for i in np.arange(coordinate_min, coordinate_max + accuracy, accuracy):
            d = abs(coordinate_value - i)
            if d <= d_min:
                d_min = d
                nearest_coordinate_value = i
        return nearest_coordinate_value

    for position in positions:

        x = get_nearest_coordinate_value(position[0], x_min, x_max)
        y = get_nearest_coordinate_value(position[1], y_min, y_max)
        z = get_nearest_coordinate_value(position[2], z_min, z_max)
        x_counter = (x - x_min) / accuracy + 1
        y_counter = (y - y_min) / accuracy + 1
        z_counter = (z - z_min) / accuracy + 1
        c_index = int((x_counter - 1) * y_total * z_total + (y_counter - 1) * z_total + z_counter)
        c = field[c_index]
        # if np.linalg.norm(c[:3] - np.array(position)) > accuracy * 1.7321:
        if np.linalg.norm(c[:3] - np.array([x, y, z])) != 0:

            for i in range(len(field)):  # 防止出现不对的情况
                if np.linalg.norm(field[i][:3] - np.array([x, y, z])) == 0:
                    c_index = i
        c = field[c_index]
        if np.linalg.norm(c[:3] - np.array([x, y, z])) != 0:
            print_colors.red('ATTENTION !! This position is far away from the supposed position!!')
            print_colors.red('Distance:\t\t\t\t%s' % (np.linalg.norm(c[:3] - np.array(position))))
            print_colors.red('In position:\t%s' % (position))
            print_colors.red('Formed position:\t%s' % ([x, y, z]))
            print_colors.red('Out position:\t\t%s' % (c[:3]))

        # print('%f %f %f %d' % (x, y, z, c_index))
        if np.isnan(c[-1]):
            c[-1] = 0
        c_array.append(c[-1])
    return np.array(c_array)


def prepare_field_data_base(t_start, t_end):
    epg = generate_empty_grid(0.05)
    for i in range(t_start, t_end + 1):
        raw_f = generate_raw_field(i)
        field = generate_field(raw_f, epg)
        save_field(field, i)
        print('%d saved' % (i))


def load_field(file_name):
    import pickle as p
    f = open('field/' + str(FIELD_TYPE) + '/' + str(file_name) + '.data', 'rb')
    return p.load(f)
