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


def source_localization(agents_no, finding_threshold, tracing_threshold):
    state = 0
    t = 1
    c_field = field.load_field(t)
    finding_end = COUNTER_MAX
    serial_no = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    agents, leader = agent.init_agents_fixed(agents_no, c_field, [-1, -1, 0.5])
    # agents, leader = init_agents_random(agents_no, c_field)
    # bf.save_trajectory(agents, leader, serial_no)
    # bf.save_results(agents, leader, serial_no, finding_end)
    # bf.show_info(agents, leader, t, state)

    while leader.concentration <= finding_threshold and len(leader.history) < COUNTER_MAX:
        t = len(leader.history) * 2
        if t >= 200:
            t = 200
        c_field = field.load_field(t)
        agents, leader = rao.plume_finding(agents, leader, c_field)
        # bf.save_trajectory(agents, leader, serial_no)
        # bf.save_results(agents, leader, serial_no, finding_end)
        # bf.show_info(agents, leader, t, state)
    finding_end = len(leader.history)
    state = 1

    while leader.concentration <= tracing_threshold and len(leader.history) < COUNTER_MAX:
        t = len(leader.history) * 2
        if t >= 200:
            t = 200
        c_field = field.load_field(t)
        agents, leader = rao.plume_tracking(agents, leader, c_field)
        # bf.save_trajectory(agents, leader, serial_no)
        # bf.save_results(agents, leader, serial_no, finding_end)
        # bf.show_info(agents, leader, t, state)
    tracing_end = len(leader.history)

    SUCCESS = False

    if tracing_end < tracing_threshold:
        SUCCESS = True

    # bf.save_trajectory(agents, leader, serial_no)
    # bf.save_results(agents, leader, serial_no, finding_end)

    return finding_end, tracing_end


if __name__ == "__main__":

    success = 0
    for i in range(100):
        finding_end, tracing_end = source_localization(agents_no=5,
                                                       finding_threshold=0.2,
                                                       tracing_threshold=0.7)
        if tracing_end < COUNTER_MAX:
            success += 1
        print(i)
    print(success)
