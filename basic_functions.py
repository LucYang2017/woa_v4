# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 8:07
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : basic_functions.py

from agent import *
import print_colors
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


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


def go_forward(agents):
    for agent in agents:
        if len(agent.history) <= 1:
            gradient = np.array([round(random.uniform(X_MIN, X_MAX), 2), round(random.uniform(Y_MIN, Y_MAX), 2),
                                 round(random.uniform(Z_MIN, Z_MAX), 2)])
        else:
            gradient = agent.history[-1][0] - agent.history[-2][0]  # 当前位置减去上一步的位置，得到方向向量
        gradient_len = np.linalg.norm(gradient)
        if gradient_len == 0:
            direction = np.array([round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2),
                                  round(random.uniform(0, 1), 2)])
        else:
            direction = gradient / gradient_len
        new_position = agent.position + STEP_LEN * direction
        new_position = check_boundary_3d(new_position)
        agent.position = new_position
    return agents


def show_info(agents, leader, t, state):
    print('********')
    if state == 0:
        print_colors.green('FINDING')
    elif state == 1:
        print_colors.red('TRACING')
    print('ITER NO. %d\tTIME %d' % (len(leader.history), t))
    print('********')
    for i in range(len(agents)):
        print('agent no. %d\t\tp: %s\tc: %s' % (i, str(agents[i].position), str(agents[i].concentration)))
    print('********')
    print_colors.yellow('AGENT LEADER\tp: %s\tc: %s' % (leader.position, leader.concentration))
    print('********')


def save_results(agents, leader, serial_no, finding_end):
    import os
    path = 'result/' + str(serial_no)
    is_exists = os.path.exists(path)

    if not is_exists:
        os.mkdir(path)

    f = open(path + '/%s-%s.txt' % (serial_no, str(len(leader.history))), 'w')
    for i in range(len(leader.history)):
        if i < finding_end:
            f.write('FINDING  ITER NO. %d\tTIME %d\n' % (i, 2 * i))
        else:
            f.write('FINDING  ITER NO. %d\tTIME %d\n' % (i, 2 * i))
        for j in range(len(agents)):
            f.write('agent no. %d\t\tp: %s\tc: %s\n' % (j, str(agents[j].history[i][0]), str(agents[j].history[i][1])))
        f.write('AGENT LEADER\tp: %s\tc: %s\n' % (str(leader.history[i][0]), str(leader.history[i][1])))
    f.close()
    f = open(path + '/agents.data', 'wb')
    import pickle as p
    p.dump(agents, f)
    f.close()
    f.close()
    f = open(path + '/leader.data', 'wb')
    p.dump(leader, f)
    f.close()


def save_trajectory(agents, leader, serial_no):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.gca(projection='3d')
    # ax.set_title(str(serial_no))
    ax.set_xlabel('X')
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylabel('Y')
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_zlabel('Z')
    ax.set_zlim(Z_MIN, Z_MAX)
    colours = ['b', 'g', 'c', 'm', 'y', 'k', 'w', 'r']

    for agent in agents:
        x = []
        y = []
        z = []
        for p in agent.history:
            x.append(p[0][0])
            y.append(p[0][1])
            z.append(p[0][2])
        colour_no = agents.index(agent) % len(colours)
        ax.plot(np.array(x), np.array(y), np.array(z), c=colours[colour_no])
        for i in range(len(agent.history)):
            ax.scatter(x[i], y[i], z[i], marker='.', c='k')
            ax.text(x[i], y[i], z[i], i + 1, color=colours[colour_no])

    x = []
    y = []
    z = []
    for p in leader.history:
        x.append(p[0][0])
        y.append(p[0][1])
        z.append(p[0][2])
    colour_no = agents.index(agent) % len(colours)
    for i in range(len(agent.history)):
        ax.scatter(x[i], y[i], z[i], marker='*', c='r')
        ax.text(x[i], y[i], z[i], '    ' + str(i + 1), color='r', fontsize='large')
    import os
    path = 'result/' + str(serial_no)
    is_exists = os.path.exists(path)

    if not is_exists:
        os.mkdir(path)

    plt.savefig(path + '/%s-%s.png' % (serial_no, str(len(leader.history))))
    plt.show()


def show_trajectory(agents, leader, serial_no):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.gca(projection='3d')
    ax.set_title(str(serial_no))
    ax.set_xlabel('X')
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylabel('Y')
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_zlabel('Z')
    ax.set_zlim(Z_MIN, Z_MAX)

    colours = ['b', 'g', 'c', 'm', 'y', 'k', 'w', 'r']
    for agent in agents:
        x = []
        y = []
        z = []
        for p in agent.history:
            x.append(p[0][0])
            y.append(p[0][1])
            z.append(p[0][2])
        colour_no = agents.index(agent) % len(colours)
        ax.plot(np.array(x), np.array(y), np.array(z), c=colours[colour_no])
        for i in range(len(agent.history)):
            ax.scatter(x[i], y[i], z[i], marker='.', c='k')
            ax.text(x[i], y[i], z[i], i + 1, color=colours[colour_no])
    x = []
    y = []
    z = []
    for p in leader.history:
        x.append(p[0][0])
        y.append(p[0][1])
        z.append(p[0][2])
    colour_no = agents.index(agent) % len(colours)
    ax.plot(np.array(x), np.array(y), np.array(z), c=colours[colour_no])
    for i in range(len(agent.history)):
        ax.scatter(x[i], y[i], z[i], marker='*', c='r')
        ax.text(x[i], y[i], z[i], '    ' + str(i + 1), color='r', fontsize='large')
    plt.show()
