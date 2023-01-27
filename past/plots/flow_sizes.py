import os
import matplotlib.pyplot as plt
import pandas as pd 
from IPython.display import display
import seaborn as sns
import matplotlib
import sys
import directories 
log_root =  "/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/logs"
plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/timeline"
apps = ["tea","tel","dis","mes","wha","sig"]
full_names = ["Teams", "Telegram", "Discord", "Messenger", "Whatsapp", "Sig"]
if __name__ == "__main__":
    sns.set_theme()
    name = sys.argv[1]
    maxx = int(sys.argv[2])
    matplotlib.rc('ytick', labelsize=8)
    for i in range(6):
        app = apps[i]
        print(app)
        app_name = full_names[i]
        path = f"{log_root}/experiment_log_{name}_{app}.txt"
        dic = {}
        opening_times = []
        lines = open(path, "r").readlines()
        lines = lines[0:100]
        startpoint = int(lines[0].strip().split(" ")[-1][0:10])
        for line in lines:
            if line == "":
                continue
            elif line.strip().split(" ")[0] == "Opening":
                arr = line.strip().split(" ")
                start_time = int(arr[3][:10])-startpoint
                opening_times.append(start_time)
                status = arr[4]
                port = arr[5]
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
        sizes = []
        for f in os.listdir("/mnt/c/Users/zolbo/whatsapp/whatsapp/port_pcaps/"):
            if f"{app}_{name}_" in f:
                port_number = f.split("_")[-1][:5]
                size = os.path.getsize(f"/mnt/c/Users/zolbo/whatsapp/whatsapp/port_pcaps/{f}")
                sizes.append(size/1000)
                for j in range(len(ports)):
                    if ports[j] == port_number:
                        ports[j] = f"{port_number}({int(size/1000)} KB)"
                        # if len(ports) > 20 and int(size/1000) < 100:
                        #     ports[j] = ""
                        # else:
                        #     ports[j] = f"{port_number}({int(size/1000)} KB)"
        sizes_list = list(sizes)
        size_total = sum(sizes_list)
        first_highest = max(sizes_list)
        sizes_list.remove(max(sizes_list))
        second_highest = max(sizes_list)/5
        second_highest_per = second_highest/size_total
        sizes_list.remove(max(sizes_list))
        remaining_total = sum(sizes_list)/4

        size_total = first_highest + second_highest + remaining_total
        first_highest_per = first_highest/size_total
        second_highest_per = second_highest/size_total
        remaining_per = remaining_total/size_total


        num_remaining = len(sizes_list)

        x = [f"Largest Flow ({int(first_highest)} KB)", f"Second Largest ({int(second_highest)} KB)", f"The Rest ({int(remaining_total)} KB over {num_remaining} flows)"]
        y = [first_highest_per, second_highest_per, remaining_per]
        plt.ylabel("Percentage of Total Data Transmitted")
        plt.bar(x, y)
        plt.xticks(rotation=90)
        plt.title(f"Sizes of dominant flows for app {app_name} (traffic collected for 1 hour)")
        plt.savefig(f"{plots_root}/{app}_{name}_flow_sizes.png",bbox_inches='tight')
        plt.clf()
