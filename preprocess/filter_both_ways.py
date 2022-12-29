from const import *
apps = ["dis", "tea", "tel", "wha", "mes"]

def filter_out(name):
    for i in range(len(apps)):
        app = apps[i]
        print(f"Processing {app}")
        pc_name = f"{pcaps_root}/{app}/{name}/{app}_{name}_{name_dic[app]}.pcap"
        pc = rdpcap(pc_name)
        out_name = f"{pcaps_root}/{app}/{name}/{app}_{name}_{name_dic[app]}_fil.pcap"
        tran_out_name = f"{tran_root}/{app}_{name_dic[app]}"
        Path(tran_out_name).mkdir(parents=True, exist_ok=True)
        w1 = open(out_name, "w")
        for pkt in pc:
            if IP not in pkt:
                continue
            dst = pkt[IP].dst
            src = pkt[IP].src
            toWrite = True
            #only focus on WAN
            if dst.startswith("10.") and src.startswith("10."):
                toWrite = False
                continue
            #filter out the traffic from other apps
            for k in dic:
                addr = k[0]
                n = k[1]
                if not app in n:
                    if dst.startswith(addr) or src.startswith(addr):
                        toWrite = False
                        continue
            if toWrite == True:
                wrpcap(out_name, pkt, append=True)
        os.system(f"tranalyzer -r {out_name} -w {tran_out_name}")
                        
names = ["out_hello"]
#"germany_hello", "india_hello", "out_hello", "nims_hello"]
for name in names:
    filter_out(name)