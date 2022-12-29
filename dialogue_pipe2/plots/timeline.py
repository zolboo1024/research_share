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
trans_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/dialogue/trans"
apps = ["tea","tel","dis","mes","wha","sig"]
full_names = ["Teams", "Telegram", "Discord", "Messenger", "Whatsapp", "Signal"]

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
    maxx = 1800
    matplotlib.rc('ytick', labelsize=8)
    for i in range(6):
        app = apps[i]
        print(app)
        app_df = extract(app)
        app_df = app_df[app_df["end_time"]<maxx*1.5]
        app_name = full_names[i]
        ax = plt.gca()
        #ax.get_yaxis().set_visible(True)
        total_sizes = app_df['total_bytes'].to_numpy()
        #ports = app_df['port_number'].to_numpy()
        ports = range(len(total_sizes))
        starting = app_df['start_time'].to_numpy()
        ending = app_df['end_time'].to_numpy()
        starting,ending = extend(starting,ending)
        starting,ending = remove_gaps(starting,ending)
        pub_sizes = [f"{int(size/1000)} KB" for size in total_sizes]
        plt.yticks(ports, pub_sizes)
        ax.tick_params(axis='y', which='major', labelsize=6)
        plt.hlines(y = ports, xmin = starting, xmax = ending)
        for j in range(len(ports)):
            port = ports[j]
            start = starting[j]
            end = ending[j]
            plt.scatter([start,end],[port,port])
        # for opening in starting:
        #     plt.axvline(x=opening)
        plt.xlabel("Number of seconds")
        plt.ylabel("Flow at port # and its size")
        plt.xlim([0, maxx])
        plt.title(f"{app_name} timeline of connections ({len(ports)} connections)")
        plt.savefig(f"{plots_root}/new_timeline/{app}_{name}_timeline.png",bbox_inches='tight')
        plt.clf()

if __name__ == "__main__":
    plot()