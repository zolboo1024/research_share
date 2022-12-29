import os
import matplotlib.pyplot as plt
import pandas as pd 
from IPython.display import display
import seaborn as sns
import matplotlib
import sys
log_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/logs"
plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/timeline"
apps = ["webbrowsing"]
full_names = ["Web browsing"]
if __name__ == "__main__":
    sns.set_theme()
    maxx = int(sys.argv[1])
    matplotlib.rc('ytick', labelsize=8)
    path = f"{log_root}/experiment_log_continuousbrowsing_web.txt"
    dic = {}
    lines = open(path, "r").readlines()
    lines = lines
    opening_times = []
    startpoint = int(lines[0].strip().split(" ")[-1][0:10])
    for line in lines:
        if line == "":
            continue
        elif line.strip().split(" ")[0] == "Opening":
            arr = line.strip().split(" ")
            start_time = int(arr[3][:10])-startpoint
            opening_times.append(start_time)
        else:
            arr = line.strip().split(" ")
            status = arr[1]
            port = arr[2]
            time = arr[-1]
            if time=="teardown":
                dic[port].append(maxx)
            elif status=="starting":
                time = int(time[0:10])-startpoint
                dic[port] = [time]
            elif status=="stopping":
                time = int(time[0:10])-startpoint
                if port in dic.keys():
                    dic[port].append(time)
    for key in dic.keys():
        if len(dic[key]) == 1:
            dic[key].append(maxx)
    ports = []
    starting = []
    ending = []
    for key in dic.keys():
        ports.append(key)
        times = dic[key]
        starting.append(times[0])
        ending.append(times[1])
    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    plt.hlines(y = ports, xmin = starting, xmax = ending)
    for j in range(len(ports)):
        port = ports[j]
        start = starting[j]
        end = ending[j]
        plt.scatter([start,end],[port,port])
    for opening in opening_times:
        plt.axvline(x=opening)
    plt.xlabel("Number of seconds")
    plt.ylabel("Flow at port # and its size")
    plt.xlim([0, maxx])
    plt.title(f"Web browsing timeline of connections ({len(ports)} connections)")
    plt.savefig(f"{plots_root}/http_timeline.png",bbox_inches='tight')
    plt.clf()
