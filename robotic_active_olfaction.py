# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 20:26
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : robotic_active_olfaction.py


import basic_functions as bf
import woa
import agent


def plume_finding(agents, leader, c_field):
    agents = bf.go_forward(agents)
    agents = agent.update_agents_c(agents, c_field)
    agents = agent.update_agents_history(agents)
    leader = agent.update_leader(agents, leader)
    return agents, leader


def plume_tracking(agents, leader, c_field):
    agents = woa.woa_3d(agents, leader)
    agents = agent.update_agents_c(agents, c_field)
    agents = agent.update_agents_history(agents)
    leader = agent.update_leader(agents, leader)
    return agents, leader
