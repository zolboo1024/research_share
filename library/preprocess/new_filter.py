from const import *
apps = ["dis", "mes", "tea", "tel", "wha"]

def filter_out(name):
    for i in range(len(apps)):
        app = apps[i]
        print(f"Processing {app}")
        file_name = f"{app}_{name}"
        for f in os.listdir(f"{port_pcaps}"):
            if file_name in f:
                file_name = f
        pc_name = f"{port_pcaps}/{file_name}"
        pc = rdpcap(pc_name)
        tran_out_name = f"{tran_root}/{app}_{name}/"
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
            if src.startswith("10.") and toWrite==True:
                wrpcap(out_name, pkt, append=True)
            elif dst.startswith("10.") and toWrite==True:
                wrpcap(in_name, pkt, append=True)
        os.system(f"tranalyzer -r {out_name} -w {tran_out_name}")
        os.system(f"tranalyzer -r {in_name} -w {tran_in_name}")
                        
names = ["germany_hello", "india_hello", "out_hello"]
for name in names:
    filter_out(name)