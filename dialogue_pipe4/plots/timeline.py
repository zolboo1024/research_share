import os
import matplotlib.pyplot as plt
import pandas as pd 
from IPython.display import display
import numpy as np
import seaborn as sns
import matplotlib
import sys
import directories 
import random 

plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/timeline"
trans_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/toplot/dialogue2/trans"
apps = ["tea","tel","dis","sig"]
full_names = ["Teams", "Telegram", "Discord", "Signal"]

def get_tran(app_name):
    return f"{trans_root}/{app_name}_tran/{app_name}_combined_flows.txt"

def extract(app_name):
    tran_name = get_tran(app_name)
    app_df = ""
    with open(tran_name, "r") as f:
        app_df = pd.read_csv(tran_name, delimiter= '\s+', index_col=False)
    app_df = app_df.sort_values(by=['timeFirst'])
    time_first = app_df['timeFirst'].to_numpy()
    time_last = app_df['timeLast'].to_numpy()
    num_pkts_sent = app_df['numBytesSnt'].to_numpy()
    num_pkts_received = app_df['numBytesRcvd'].to_numpy()
    port_numbers = app_df["srcPort"].to_numpy()
    i = 0
    start_time = []
    end_time = []
    abs_start = np.min(time_first)
    total_sizes = []
    port_number = []
    while i < len(time_first)-1:
        out_time_first = time_first[i]-abs_start
        in_time_first = time_first[i+1]-abs_start
        out_time_last = time_last[i]-abs_start
        in_time_last = time_last[i+1]-abs_start
        total_size = num_pkts_sent[i]+num_pkts_received[i]
        cur_time_first = min(out_time_first, in_time_first)
        cur_time_last = max(out_time_last, in_time_last)
        start_time.append(cur_time_first)
        end_time.append(cur_time_last)
        total_sizes.append(total_size)
        port_number.append(port_numbers[i])
        i += 2
    return pd.DataFrame({"start_time": start_time, "end_time": end_time, "total_bytes": total_sizes, "port_number": port_number})

def extend(start_times, end_times):
    for i in range(len(start_times)):
        endd = end_times[i]
        startt = start_times[i]
        duration = endd - startt 
        if duration < 5: 
            new_length = random.randint(8, 16)
            end_times[i] = startt + new_length
    return(start_times, end_times)
    
def remove_gaps(start_times, end_times):
    last_time = end_times[0]
    i = 1 
    while i < len(start_times):
        cur_time = start_times[i]
        diff = cur_time - last_time
        if diff > 8: 
            shift = diff - 7
            for j in range(i+1, len(start_times)):
                start_times[j] = start_times[j] - shift
                end_times[j] = end_times[j] - shift
        last_time = end_times[i]
        i += 1
    return(start_times, end_times)

def plot():
    sns.set_theme()
    name = "dialogue"
    offsett = 72000
    maxx = 900
    matplotlib.rc('ytick', labelsize=8)
    for i in range(4):
        app = apps[i]
        print(app)
        app_df = extract(app)
        starting,ending = remove_gaps(app_df["start_time"].to_numpy(),app_df["end_time"].to_numpy())
        app_df["start_time"] = starting
        app_df["end_time"] = ending
        app_df["end_time"] = app_df["end_time"]-offsett
        app_df = app_df[(app_df["end_time"]<maxx*1.5)&(app_df["end_time"]>0)]
        app_name = full_names[i]
        ax = plt.gca()
        #ax.get_yaxis().set_visible(True)
        total_sizes = app_df['total_bytes'].to_numpy()
        #ports = app_df['port_number'].to_numpy()
        ports = range(len(total_sizes))
        starting = app_df['start_time'].to_numpy()
        ending = app_df['end_time'].to_numpy()
        #starting,ending = extend(starting,ending)

        small_ports = []
        small_starting = []
        small_ending = []
        small_sizes = []
        large_ports = []
        large_starting = []
        large_ending = []
        large_sizes = []
        for j in range(len(ports)):
            cur_size = total_sizes[j]
            if cur_size < 7000:
                small_ports.append(ports[j])
                small_starting.append(starting[j])
                small_ending.append(ending[j])
                small_sizes.append(cur_size)
            else:
                large_ports.append(ports[j])
                large_starting.append(starting[j])
                large_ending.append(starting[j])
                large_sizes.append(cur_size)

        print(small_ports)
        print(large_ports)
        #for the large flows
        large_pub_sizes = [f"{int(size/1000)} KB" for size in large_sizes]
        plt.yticks(large_ports, large_pub_sizes)

        ax.tick_params(axis='y', which='major', labelsize=6)
        plt.hlines(y = large_ports, xmin = large_starting, xmax = large_ending)
        for j in range(len(large_ports)):
            port = large_ports[j]
            start = large_starting[j]
            end = large_ending[j]
            plt.scatter([start,end],[port,port])
        
        #for the small flows
        small_pub_sizes = [f"{int(size/1000)} KB" for size in small_sizes]
        plt.yticks(small_ports, small_pub_sizes)
        ax.tick_params(axis='y', which='major', labelsize=6, color="red")
        plt.hlines(y = small_ports, xmin = small_starting, xmax = small_ending)
        for j in range(len(small_ports)):
            port = small_ports[j]
            start = small_starting[j]
            end = small_ending[j]
            plt.scatter([start,end],[port,port])

        # for opening in starting:
        #     plt.axvline(x=opening)
        plt.xlabel("Number of seconds")
        plt.ylabel("Flow at port # and its size")
        plt.xlim([0, maxx])
        plt.title(f"{app_name} timeline of connections ({len(ports)} connections)")
        plt.savefig(f"{plots_root}/timeline4/{app}_{name}_timeline.png",bbox_inches='tight')
        plt.clf()

if __name__ == "__main__":
    plot()