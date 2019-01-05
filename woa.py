# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 20:23
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : woa.py

from configs import *
import random
import math
import basic_functions


def woa_3d(agents, leader):
    agents_no = len(agents)
    counter = len(leader.history)
    for agent in agents:

        # c_gradient = np.array([0, 0, 0])
        # if counter > 0:
        #     if agent.concentration > agent.history[-1][1]:
        #         c_gradient = agent.position - agent.history[-1][0]

        a = 2 - counter * (2.0 / float(COUNTER_MAX))

        p = random.uniform(0, 1)

        C = np.array([random.uniform(-2, 2) for i in range(len(leader.position))])
        A = random.uniform(-a, a)

        chioce = 0
        if p < 0.5:
            if abs(A) < 1:
                chioce = 0
                D = C * abs(leader.position - agent.position)
                # print(leader.position)
                # print(A * D)
                new_position = leader.position - A * D
            elif abs(A) >= 1:
                chioce = 1
                random_agent_no = random.randint(0, agents_no - 1)
                random_agent = agents[random_agent_no]
                D = C * abs(random_agent.position - agent.position)
                new_position = random_agent.position - A * D
        elif p >= 0.5:
            chioce = 2
            D = abs(leader.position - agent.position)
            b = 1  # 用来定义螺旋大小的常数
            l = random.uniform(-1, 1)
            new_position = D * math.exp(b * l) * math.cos(2 * math.pi * l) + leader.position

        # print('agent no. %d  a = %f  p = %f A = %s C = %s D = %s' % (agents.index(agent), a, p, str(A), str(C), str(D)))
        new_position = basic_functions.check_boundary_3d(new_position)
        agent.position = new_position
    return agents
