from const import *

def input_label(df):
    labels = df["label"]
    inputs = df.drop("label", axis=1)
    return labels, inputs

apps = ["dis", "tea", "tel", "wha", "sig", "mes"]
def get_flows(name):
    apps_flows = {}
    count = 0
    for i in range(len(apps)):
        app = apps[i]
        print(f"Processing {app}")
        file_name = f"{app}_{name}"
        for f in os.listdir(f"{port_pcaps}"):
            if file_name in f:
                file_name = f
        pc_name = f"{port_pcaps}/{file_name}"
        pc = rdpcap(pc_name)
        flows = {}
        for pkt in pc:
            #skip non-WAN packets
            if IP not in pkt:
                continue
            toWrite = True
            #get IP addresses
            dst = pkt[IP].dst
            src = pkt[IP].src
            #only focus on WAN
            if dst.startswith("10.") and src.startswith("10."):
                toWrite = False
                continue
            #get port numbers
            sport = None
            dport = None
            if TCP in pkt:
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
            if UDP in pkt:
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
            if sport == None or dport == None:
                continue
            #get direction
            direction = None
            if src.startswith("10."):
                direction = "A"
            elif dst.startswith("10."):
                direction = "B"
            else:
                continue
            #save it into the dictionary
            flow = Flow(src, dst, sport, dport, direction)
            count += 1
            if flow in flows.keys():
                flows[flow].append(pkt)
            else:
                flows[flow] = []
                flows[flow].append(pkt)
        print(f"{app} {len(flows)}")
        apps_flows[app] = flows
    print(f"Total number of packets: {count}")
    return apps_flows

def pickle_flows(name):
    flows = get_flows(name)
    file_name = f"{separated_flows_root}/{name}_flows.pkl"
    with open(file_name, "wb") as f:
        pickle.dump(flows, f)

if __name__ == "__main__":
    name = sys.argv[1]
    pickle_flows(name)