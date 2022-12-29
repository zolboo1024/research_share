from const import *

ids = ["1"]
apps = ["dis", "wha", "tel"]
caps = {
    "dis": 3000,
    "wha": 1000,
    "sig": 2000,
    "tea": 20000,
    "tel": 4000,
    "mes": 4000
}
#return the name of the file for the log
def msglogname(app, num):
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/msg_logs/size1hour{num}_{app}.txt"

def portlogname(app, num):
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/msg_ports/size1hour{num}_{app}.txt"

#return the name of the file for the pcap
def pcapname(app, num):
    files = os.listdir("/mnt/c/Users/zolbo/whatsapp/whatsapp/size_pcaps/1hour")
    for f in files:
        if f"{app}_size1hour{num}" in f:
            return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/size_pcaps/1hour/{f}"
    return 0

def get_messagestamps(app, num):
    file_name = msglogname(app, num)
    f = open(file_name, "r")
    lines = f.readlines()
    timestamps = []
    sizes = []
    for line in lines:
        split = line.strip("\n").split()
        if split[0]=="Sending":
            timestamps.append(split[-1])
            sizes.append(int(split[4]))
    return timestamps, sizes


#return the dictionary of active ports dictionary value containing
#all the used ports for a given timestamp (in seconds)
def get_activeports(app, num):
    file_name = portlogname(app, num)
    active_ports = {}
    f = open(file_name, "r")
    lines = f.readlines()
    start_time = int(lines[0].strip("\n").split()[-1][0:10])
    closing_time = 0
    for line in lines:
        split = line.strip("\n").split()
        if len(split) == 5:
            action = split[1]
            port = split[2]
            timestamp = int(split[-1][0:10])
            if action == "starting":
                if port in active_ports.keys() and len(active_ports[port])%2==0:
                    active_ports[port].append(timestamp-1)
                elif port not in active_ports.keys():
                    active_ports[port] = [timestamp-1]
                else: 
                    print("Starting error")
            elif action == "stopping":
                if port in active_ports.keys() and len(active_ports[port])%2==1:
                    active_ports[port].append(timestamp)
                else:
                    print("Stopping error")
            closing_time = timestamp+200
    dic = {}
    for i in range(start_time-10,closing_time+1):
        dic[i] = []
    for port in active_ports.keys():
        if len(active_ports[port]) % 2 == 1:
            active_ports[port].append(closing_time)
        cur_spans = active_ports[port]
        j = 0
        while j < len(cur_spans):
            startt = cur_spans[j]
            j += 1
            stopp = cur_spans[j]
            j += 1
            for k in range(startt, stopp+1):
                dic[k].append(port)
    return dic

#filter out the background traffic
#and only get the packet sizes and timings
def filter_out(app, num):
    pc_name = pcapname(app, num)
    pc = rdpcap(pc_name)
    active_ports = get_activeports(app, num)
    print(f"{pc[0].time}-{pc[-1].time} {min(active_ports.keys())}-{max(active_ports.keys())}")
    ids = []
    dirs = []
    stamps = []
    lens = []
    for pkt in pc:
        if IP not in pkt:
            continue
        toWrite = True
        #get port numbers
        sport = None
        dport = None
        if TCP in pkt:
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
        elif UDP in pkt:
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport
        else:
            continue
        stamp = int(pkt.time)
        dst = pkt[IP].dst
        src = pkt[IP].src
        #only focus on WAN
        if dst.startswith("10.") and src.startswith("10."):
            toWrite = False
            continue
        if str(sport) in active_ports[stamp]:
            ids.append(sport)
            dirs.append("out")
            stamps.append(stamp)
            lens.append(len(pkt))
        elif str(dport) in active_ports[stamp]:
            ids.append(dport)
            dirs.append("in")
            stamps.append(stamp)
            lens.append(len(pkt))
    df = pd.DataFrame({"FlowID": ids, "Direction": dirs, "Timestamp": stamps, "Length": lens})
    return df

def pickle_all():
    for app in apps:
        for num in ids:
            pickle.dump(filter_out(app, num), open(f"./size_pkts_dfs/{app}_{num}_ports.pkl","wb"))

def get_pktsdf(app, num):
    return pickle.load(open(f"./size_pkts_dfs/{app}_{num}_ports.pkl","rb"))

def get_bursts(df, stamps, sizes):
    total_sizes = []
    new_sizes = []
    for i in range(len(sizes)):
        start = int(stamps[i][:10])-1
        stop = int(stamps[i][:10])+2
        burst = df[(df["Timestamp"]>start) & (df["Timestamp"]<stop)]
        uniques = burst["FlowID"].unique()
        largest = 0
        for flowid in uniques:
            curFlow = burst[burst["FlowID"]==flowid]
            if curFlow["Length"].sum() > largest:
                largest = curFlow["Length"].sum()
        if len(burst.index!=0) and (largest < caps[app]) and (largest > sizes[i]):
            new_sizes.append(sizes[i])
            total_sizes.append(largest)
    return total_sizes, new_sizes
    
if __name__ == "__main__":
    #pickle_all()
    for app in apps:
        for num in ids:
            pkts_df = get_pktsdf(app, num)
            msg_stamps, sizes = get_messagestamps(app, num)
            total_sizes, new_sizes = get_bursts(pkts_df, msg_stamps, sizes)
            plt.scatter(new_sizes, total_sizes)
            plt.title(f"Message size vs Largest burst size for {app}")
            plt.ylabel("Total burst size")
            plt.xlabel("Message size")
            plt.savefig(f"{plots_root}/size_alltraffic/sizes_ports_{app}.png")
            plt.close()

