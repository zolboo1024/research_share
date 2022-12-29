import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
from IPython.display import display
import seaborn as sns

tran_root =  "/home/zolboo/whatsapp/whatsapp/andr/traffic/tran/"
plots_root = "/home/zolboo/whatsapp/whatsapp/andr/traffic/plots/"

def get_filename(app):
    return f"{tran_root}{app}_germany_hellotcp_flows.txt"

def save(name):
    plt.savefig(f"{plots_root}{name}")

num_pkts_rec = []
num_pkts_snt = []
apps = ["dis","tea","tel","mes","wha","sig"]
mins = []
maxes = []
means = []
std = []
for app in apps:
    app_file = get_filename(app)
    app_df = pd.read_csv(app_file, delimiter= '\s+', index_col=False)
    app_df["totalBytes"] = app_df["numBytesSnt"]+app_df["numBytesRcvd"]
    max_row = app_df.loc[app_df["totalBytes"].idxmax()]
    flow_ind = max_row["flowInd"]
    max_row = app_df.loc[app_df["flowInd"]==flow_ind].sum()
    num_pkts_rec.append(max_row["numPktsRcvd"])
    num_pkts_snt.append(max_row["numPktsSnt"])

fig, ax = plt.subplots()
width = 0.35
ax.bar(apps, num_pkts_snt, width, label='Packets sent')
ax.bar(apps, num_pkts_rec, width, bottom=num_pkts_snt,
       label='Packets received')
ax.set_ylabel('Number of packets')
ax.set_title('Total packets exchanged in the biggest communication')
ax.legend()
save("numpkts.png")

# # create stacked errorbars:
# plt.errorbar(np.arange(8), means, std, fmt='ok', lw=3)
# plt.errorbar(np.arange(8), means, [means - mins, maxes - means],
#              fmt='.k', ecolor='gray', lw=1)
# plt.xlim(-1, 8)
# plt.bar(apps, num_flows)
# plt.title("Number of total flows per application")
#save("numflows.png")