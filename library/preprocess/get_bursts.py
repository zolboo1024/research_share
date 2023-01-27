from const import *
import numpy as np 
from scapy.all import *
import pandas as pd 
from IPython.display import display
import os 
import matplotlib.pyplot as plt
from pandas.plotting import table
import pickle
from pathlib import Path

def get_flows(name):
    f = open(f"{separated_flows_root}/{name}_flows.pkl", "rb")
    return pickle.load(f)

def save_bursts(name):
    flows = get_flows(name)
    bursts = {}
    count = 0
    for app in flows.keys():
        print(app)
        bursts[app] = []
        for flow_index in flows[app].keys():
            flow = flows[app][flow_index]
            if len(flow) == 1:
                bursts[app].append(Burst(flow_index,[flow[0]]))
                continue
            cur_time = flow[0].time
            cur_burst = [flow[0]]
            for i in range(1,len(flow)):
                pkt = flow[i]
                time = pkt.time
                #if within 1 second from last packet, save it into the current burst
                if cur_time + 1 > time:
                    cur_burst.append(pkt)
                else:
                    #if one second has passed, start a new burst and save the previous burst
                    bursts[app].append(Burst(flow_index, cur_burst))
                    cur_burst = []
                    cur_burst.append(pkt)
                cur_time = time
            bursts[app].append(Burst(flow_index, cur_burst))
        count += len(bursts[app])
    print(f"Extracted {count} bursts")
    with open(f"{separated_bursts_root}/{name}_bursts.pkl", "wb") as f:
        pickle.dump(bursts, f)
        
if __name__ == "__main__":
    name = sys.argv[1]
    save_bursts(name)