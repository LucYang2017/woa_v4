# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 8:10
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : agent.py

import random
from configs import *
import numpy as np


class Agent3D:
    def __init__(self):
        self.position = np.array([round(random.uniform(X_MIN, X_MAX), 2), round(random.uniform(Y_MIN, Y_MAX), 2),
                                  round(random.uniform(Z_MIN, Z_MAX), 2)])
        self.concentration = float('-inf')
        self.history = []

    def update_msg(self, new_position, new_concentration):
        self.history.append([self.position, self.concentration])
        self.position = new_position
        self.concentration = new_concentration


def get_agents_positions(agents):
    positions = []
    for agent in agents:
        positions.append(agent.position)
    return np.array(positions)


def update_agents_c(agents, c_field):
    agents_c = get_c_3d(c_field, get_agents_positions(agents))
    for i in range(len(agents)):
        agents[i].concentration = agents_c[i]
    return agents


def init_agents_random(agents_no, c_field):
    leader = Agent3D()
    leader.position = np.array([0, 0, 0])
    leader.concentration = float('-inf')
    agents = []
    for i in range(agents_no):
        agents.append(Agent3D())

    agents = update_agents_c(agents, c_field)
    agents = update_agents_history(agents)
    leader = update_leader(agents, leader)
    return agents, leader


def update_agents_history(agents):
    for agent in agents:
        agent.update_msg(agent.position, agent.concentration)
    return agents

def init_agents_fixed(agents_no, c_field, init_position):
    leader = Agent3D()
    leader.position = np.array([0, 0, 0])
    leader.concentration = float('-inf')
    agents = []
    x = init_position[0]
    y = init_position[1]
    z = init_position[2]
    for i in range(agents_no):
        agents.append(Agent3D())
        agents[-1].position = np.array(
            [x + random.uniform(-0.5, 0.5), y + random.uniform(-0.5, 0.5), z + random.uniform(-0.5, 0.5)])
    agents = update_agents_c(agents, c_field)
    agents = update_agents_history(agents)
    leader = update_leader(agents, leader)
    return agents, leader
