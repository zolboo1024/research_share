import os
import sys 

#pull from all the files in dialogue
dst = "/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/toplot/dialogue2"

#then put them in the combined folder
to_put = "/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/toplot/dialogue2/combined"

#apps = ["tea"]
apps = ["tea","mes","dis","sig","tel","wha"]

if __name__ == "__main__":
    for app in apps:
        file_names = ""
        pcap_dir = f"{dst}/"
        files = os.listdir(pcap_dir)
        for f in files:
            name = f"{app}"
            if name in f and f"combined" not in f and "tran" not in f:
                if os.path.getsize(f"{pcap_dir}{f}") >= 0:
                    os.system(f"pcapfix {pcap_dir}{f} -o {pcap_dir}{f}")
                    file_names += f"{pcap_dir}{f} "
        comb_names = []
        i = 0
        split = file_names.split()
        print(f"{app} number of pcaps: {len(split)}")
        while i < len(split):
            cur_names = ""
            for j in range(100):
                if (i>=len(split)):
                    break
                else:
                    cur_name = split[i]
                    cur_names += f"{cur_name} "
                    i += 1
            comb_names.append(cur_names)
        final_names = ""
        for i in range(len(comb_names)):
            cur_names = comb_names[i]
            if len(cur_names) > 2:
                os.system(f"mergecap -F pcap -w {pcap_dir}{app}_part{i}_combined.pcap {cur_names}")
                nameeee = f"{pcap_dir}{app}_part{i}_combined.pcap"
                if os.path.isfile(nameeee):
                    final_names += f"{nameeee} "
        os.system(f"mergecap -F pcap -w {to_put}/{app}_combined.pcap {final_names}")