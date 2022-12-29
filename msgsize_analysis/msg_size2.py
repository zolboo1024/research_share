from const import *
from scipy.stats import gaussian_kde
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap

ids = ["2"]
apps = ["dis", "wha", "sig", "tea", "tel", "mes"]
caps = {
    "dis": 3000,
    "wha": 1000,
    "sig": 2000,
    "tea": 20000,
    "tel": 4000,
    "mes": 2500
}
lowests = {
    "dis": 1000,
    "sig": 750,
    "mes": 1000, 
    "tel": 1000,
    "tea": 1000,
    "wha": 500
}
burstlengths = {
    "dis": 6,
    "mes": 10,
    "sig": 4,
    "tea": 30,
    "tel": 20,
    "wha": 6
}
#return the name of the file for the log
def msglogname(app, num):
    if app == "wha":
        return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/msg_logs/size1hour1_{app}.txt"
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/msg_logs/size1hour{num}_{app}.txt"

def portlogname(app, num):
    if app == "wha":
        return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/msg_ports/size1hour1_{app}.txt"
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/msg_ports/size1hour{num}_{app}.txt"

#return the name of the file for the pcap
def pcapname(app, num):
    if app == "wha":
        return "/mnt/c/Users/zolbo/whatsapp/whatsapp/size_pcaps/1hour/wha_size1hour1_1662998881_3600.pcap"
    files = os.listdir("/mnt/c/Users/zolbo/whatsapp/whatsapp/size_pcaps/1hour2")
    print(files)
    print(f"size1hour{num}_{app}")
    for f in files:
        if f"{app}_size1hour{num}" in f:
            return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/size_pcaps/1hour2/{f}"
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
            timestamps.append(float(split[-1]))
            sizes.append(int(split[4]))
    return timestamps, sizes


#return the dictionary of active ports dictionary value containing
#all the used ports for a given timestamp (in seconds)
def get_activeports(app, num):
    file_name = logname(app, num)
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
    #active_ports = get_activeports(app, num)
    #print(f"{pc[0].time}-{pc[-1].time} {min(active_ports.keys())}-{max(active_ports.keys())}")
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
        stamp = pkt.time
        dst = pkt[IP].dst
        src = pkt[IP].src
        #only focus on WAN
        if dst.startswith("10.") and src.startswith("10."):
            toWrite = False
            continue
        if dst.startswith("10."):
            ids.append(sport)
            dirs.append("in")
            stamps.append(stamp)
            lens.append(len(pkt))
        elif src.startswith("10."):
            ids.append(dport)
            dirs.append("out")
            stamps.append(stamp)
            lens.append(len(pkt))
    df = pd.DataFrame({"FlowID": ids, "Direction": dirs, "Timestamp": stamps, "Length": lens})
    return df

def pickle_all():
    for app in apps:
        print(app)
        for num in ids:
            pickle.dump(filter_out(app, num), open(f"./pkt_dfs/{app}_{num}.pkl","wb"))

def get_pktsdf(app, num):
    if app == "wha":
        return pickle.load(open(f"./pkt_dfs/{app}_1.pkl","rb"))
    return pickle.load(open(f"./pkt_dfs/{app}_{num}.pkl","rb"))

def get_ith_pkt(df, stamps, sizes, app, ii):
    nthsizes = []
    new_sizes = []
    for i in range(len(sizes)):
        start = stamps[i]-1
        stop = stamps[i]+2
        burst = df[(df["Timestamp"]>start) & (df["Timestamp"]<stop)]
        # & (df["Direction"]=="out")]
        if len(burst.index)!=0:
            uniques = burst["FlowID"].unique()
            largest = burst[burst["FlowID"]==uniques[0]]
            for flowid in uniques:
                curFlow = burst[burst["FlowID"]==flowid]
                if curFlow["Length"].sum() > largest["Length"].sum():
                    largest = curFlow
            #largest is the array- containing the largest burst
            if (largest["Length"].sum() < caps[app]) and (largest["Length"].sum() > lowests[app]):
                new_sizes.append(sizes[i])
                if ii < len(largest["Length"].values):
                    nthsizes.append(largest["Length"].values[ii])
                else:
                    nthsizes.append(0)
    return nthsizes, new_sizes

def get_bursts(df, stamps, sizes, app):
    total_sizes = []
    new_sizes = []
    for i in range(len(sizes)):
        start = stamps[i]-1
        stop = stamps[i]+2
        burst = df[(df["Timestamp"]>start) & (df["Timestamp"]<stop)]
        # & (df["Direction"]=="out")]
        if len(burst.index)!=0:
            uniques = burst["FlowID"].unique()
            largest = 0
            for flowid in uniques:
                curFlow = burst[burst["FlowID"]==flowid]
                if curFlow["Length"].sum() > largest:
                    largest = curFlow["Length"].sum()
            if len(burst.index)!=0 and (largest < caps[app]) and (largest > lowests[app]):
                new_sizes.append(sizes[i])
                total_sizes.append(largest)
    return total_sizes, new_sizes


def get_wholeburst(df, stamps, sizes, app):
    bursts = []
    new_sizes = []
    for i in range(len(sizes)):
        start = stamps[i]-1
        stop = stamps[i]+2
        burst = df[(df["Timestamp"]>start) & (df["Timestamp"]<stop)]
        # & (df["Direction"]=="out")]
        if len(burst.index)!=0:
            uniques = burst["FlowID"].unique()
            largest = burst[burst["FlowID"]==uniques[0]]
            for flowid in uniques:
                curFlow = burst[burst["FlowID"]==flowid]
                if curFlow["Length"].sum() > largest["Length"].sum():
                    largest = curFlow
            df = df.drop(df[(df["FlowID"] == largest["FlowID"].iloc(0)) & (df["Timestamp"]>start) & (df["Timestamp"]<stop)].index)
            #largest is the array- containing the largest burst
            if (largest["Length"].sum() < caps[app]) and (largest["Length"].sum() > lowests[app]):
                new_sizes.append(sizes[i])
                bursts.append(largest)
    return bursts, new_sizes, df

if __name__ == "__main__":
    if sys.argv[1] == "plot":
        app = "wha"
        for num in ids:
            pkts_df = get_pktsdf(app, num)
            msg_stamps, sizes = get_messagestamps(app, num)
            total_sizes, new_sizes = get_bursts(pkts_df, msg_stamps, sizes, app)
            plt.scatter(new_sizes, total_sizes)
            plt.title(f"Message size vs Largest burst size for {app}")
            plt.ylabel("Total burst size")
            plt.xlabel("Message size")
            plt.savefig(f"{plots_root}/size_alltraffic/1hour2/sizes_{app}_alltraffic.png")
            plt.close()
    elif sys.argv[1] == "table":
        pearsons = []
        orderedapps = []
        scores = []
        for app in apps:
            for num in ids:
                orderedapps.append(fullnames[app])
                pkts_df = get_pktsdf(app, num)
                msg_stamps, sizes = get_messagestamps(app, num)
                total_sizes, new_sizes = get_bursts(pkts_df, msg_stamps, sizes, app)
                pearsons.append(pearsonr(total_sizes, new_sizes)[0])
                #reshape since it only has 1 feature
                X = np.array(total_sizes).reshape(-1,1)
                reg = LinearRegression().fit(X, new_sizes)
                mean_abs = mean_absolute_error(reg.predict(X), new_sizes)
                scores.append(mean_abs)
        export_df(pd.DataFrame({"App":orderedapps, "Pearson Correlation":pearsons}), "size_alltraffic/1hour2/pearsons")
        export_df(pd.DataFrame({"App":orderedapps, "Regression MAE":scores}), "size_alltraffic/1hour2/scores")
    elif sys.argv[1] == "comparenth":
        for app in apps:
            for num in ids:
                pkts_df = get_pktsdf(app, num)
                msg_stamps, sizes = get_messagestamps(app, num)
                print(app)
                for i in range(10):
                    nthsizes, new_sizes = get_ith_pkt(pkts_df, msg_stamps, sizes, app, i)
                    print(pearsonr(nthsizes, new_sizes)[0])
    elif sys.argv[1] == "clustersizes":
        for app in apps: 
            for num in ids:
                pkts_df = get_pktsdf(app, num)
                msg_stamps, sizes = get_messagestamps(app, num)
                print(app)
                bursts, new_sizes = get_wholeburst(pkts_df, msg_stamps, sizes, app)
                sizes_toplot = []
                positions = []
                for burst in bursts:
                    burst_length = len(burst.index)
                    for i in range(burst_length):
                        sizes_toplot.append(burst["Length"].values[i])
                        positions.append(i)
                # "Viridis-like" colormap with white background
                # Calculate the point density
                xy = np.vstack([positions, sizes_toplot])
                z = gaussian_kde(xy)(xy)
                sc = plt.scatter(positions, sizes_toplot, c=z, s=25)
                plt.colorbar(sc)
                plt.title(f"{app}: Clustering packet sizes for each position in the burst")
                plt.ylabel("Packet size")
                plt.xlabel("Position in the burst")
                plt.savefig(f"{plots_root}/size_alltraffic/1hour2/position_sizes_{app}.png")
                plt.close()
    elif sys.argv[1] == "fingerprint":
        name = "fingerprint"
        for app in apps:
            for num in ids:
                pkts_df = get_pktsdf(app, num)
                msg_stamps, sizes = get_messagestamps(app, num)
                print(app)
                bursts, new_sizes, left_over = get_wholeburst(pkts_df, msg_stamps, sizes, app)
                datapoints = []
                labels = []
                burst_length = burstlengths[app]
                #positive datapoint
                for i in range(len(bursts)):
                    datapoint = []
                    burst = bursts[i]
                    length_arr = burst["Length"].values
                    if len(length_arr) >= burst_length:
                        datapoint.extend(burst["Length"].values[:burst_length])
                        datapoint.extend(burst["Direction"].values[:burst_length])
                    for i in range(3):
                        datapoints.append(datapoint)
                        labels.append(1)
                #negative datapoint
                left_lengths = left_over["Length"].values
                left_dirs = left_over["Direction"].values
                for i in range(len(left_lengths)-burst_length):
                    datapoint = []
                    lengths = left_lengths[i:(i+burst_length)]
                    dirs = left_dirs[i:(i+burst_length)]
                    datapoint.extend(lengths)
                    datapoint.extend(dirs)
                    datapoints.append(datapoint)
                    labels.append(0)
                #build the df and train
                ml_df = pd.DataFrame(datapoints)
                for col in ml_df:
                    if ml_df[col].dtype == "object":
                        ml_df[col] = ml_df[col].astype("category").cat.codes
                ml_df = shuffle(ml_df)
                ml_df = ml_df.fillna(0)
                X_train, X_test, y_train, y_test = train_test_split(ml_df, labels, test_size=0.4)
                clf = cdic["Random Forest"]
                clf.fit(X_train, y_train)
                y_predic = clf.predict(X_test)
                train_predic = clf.predict(X_train)
                export_cm_df(y_test, y_predic, f"{name}/{name}_cm_{app}", app)


