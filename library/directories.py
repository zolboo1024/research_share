#mapping of all the directories I used

tran_root =  "/mnt/c/Users/zolbo/whatsapp/whatsapp/trans"
plots_root = "/Users/zolboo/research/research/results"
pcaps_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/pcaps"
separated_flows_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/flows_separated"
separated_bursts_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/bursts_separated"
sizes_times_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/sizes_times"
four_hr_root =  "/mnt/c/Users/zolbo/whatsapp/whatsapp/four_hours"
port_pcaps = "/mnt/c/Users/zolbo/whatsapp/whatsapp/port_pcaps"
out_pcaps = "/mnt/c/Users/zolbo/whatsapp/whatsapp/all_pcaps"
log_root =  "/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/logs"
csvs = "/Users/zolboo/research/research/results"

def tran_name(app, name, direction):
    return f"{tran_root}/{app}_{name_dic[app]}_{direction}/{app}_{name}_{name_dic[app]}_fil_{direction}_flows.txt"