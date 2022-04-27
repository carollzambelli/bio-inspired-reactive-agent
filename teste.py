import numpy as np
import pandas as pd
import iterable

sensors = ["i_ini", "i_vz", "i_bfs", "i_b", "i_s", "i_bs", "i_gl", "i_bf", 
                "i_fs", "i_f", "behind", "i_cl", "i_died"]
values = [[[0]*1]*4]*len(sensors)




lut = {}
for key in sensors:
    for value in values:
        lut[key] = value
        values.remove(value)
        break  