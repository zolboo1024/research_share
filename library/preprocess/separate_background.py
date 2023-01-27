from const import *
apps = ["webbrowsing"]

def get_activeports(app):
    file_name = app
    for f in os.listdir(f"{log_root}"):
        if app in f:
            file_name = f
            break
    active_ports = {}
    f = open(f"{log_root}/{file_name}", "r")
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
            closing_time = timestamp+75
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

def filter_out():
    for i in range(len(apps)):
        app_name = apps[i]
        app = ""
        print(f"Processing {app_name}")
        for f in os.listdir(f"{out_pcaps}"):
            print(f)
            if app_name in f:
                app = f
                break
        pc_name = f"{out_pcaps}/{app}"
        pc = rdpcap(pc_name)
        app_out = f"{out_pcaps}/{app_name}_app.pcap"
        back_out = f"{out_pcaps}/{app_name}_back.pcap"
        app_tran = f"{out_pcaps}/{app_name}_app_tran"
        back_tran = f"{out_pcaps}/{app_name}_back_tran"
        Path(app_tran).mkdir(parents=True, exist_ok=True)
        Path(back_tran).mkdir(parents=True, exist_ok=True)
        w1 = open(app_out, "w")
        w1 = open(back_out, "w")
        active_ports = get_activeports(app_name)
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
            if str(sport) in active_ports[stamp] or str(dport) in active_ports[stamp]:
                wrpcap(app_out, pkt, append=True)
            else:
                wrpcap(back_out, pkt, append=True)
            
        os.system(f"tranalyzer -r {app_out} -w {app_tran}")
        os.system(f"tranalyzer -r {back_out} -w {back_tran}")
                        
if __name__ == "__main__":
    filter_out()