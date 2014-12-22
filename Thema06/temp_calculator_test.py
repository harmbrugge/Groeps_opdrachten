#!/usr/bin/env python3

# Tm= 64.9 +41*(yG+zC-16.4)/(wA+xT+yG+zC)
probe_file = open('probes_2', 'r')


for cur_probe in probe_file:
    cur_c_count = cur_probe.count('c')
    cur_g_count = cur_probe.count('g')
    cur_a_count = cur_probe.count('a')
    cur_t_count = cur_probe.count('t')
    cur_tm = 64.9 + 41 * (cur_g_count+cur_c_count-16.4)/(cur_a_count+cur_t_count+cur_g_count+cur_c_count)
    print(cur_probe.strip(), cur_tm)

probe_file.close()