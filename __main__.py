# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 20:37
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : __main__.py

import field
import agent
import basic_functions as bf
import robotic_active_olfaction as rao
from configs import *
import time

if __name__ == "__main__":
    agents_no = 5
    t = 1
    c_field = field.load_field(t)
    plume_finding_threshold = 0.2
    woa_threshold = 0.6
    state = 0
    finding_end = COUNTER_MAX
    serial_no = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))

    agents, leader = agent.init_agents_fixed(agents_no, c_field, [-1, -1, 0.5])
    # agents, leader = init_agents_random(agents_no, c_field)

    bf.save_trajectory(agents, leader, serial_no)
    bf.save_results(agents, leader, serial_no, finding_end)
    bf.show_info(agents, leader, t, state)

    while leader.concentration <= plume_finding_threshold and len(leader.history) < COUNTER_MAX:
        t = len(leader.history) * 2
        if t >= 200:
            t = 200
        c_field = field.load_field(t)
        agents, leader = rao.plume_finding(agents, leader, c_field)
        bf.save_trajectory(agents, leader, serial_no)
        bf.save_results(agents, leader, serial_no, finding_end)
        bf.show_info(agents, leader, t, state)

    finding_end = len(leader.history)

    state = 1
    while leader.concentration <= woa_threshold and len(leader.history) < COUNTER_MAX:
        t = len(leader.history) * 2
        if t >= 200:
            t = 200
        c_field = field.load_field(t)
        agents, leader = rao.plume_tracking(agents, leader, c_field)
        bf.save_trajectory(agents, leader, serial_no)
        bf.save_results(agents, leader, serial_no, finding_end)
        bf.show_info(agents, leader, t, state)

    bf.save_trajectory(agents, leader, serial_no)
    bf.save_results(agents, leader, serial_no, finding_end)
