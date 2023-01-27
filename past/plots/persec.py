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

pps = []
bps = []
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
    # flow_ind = max_row["flowInd"]
    # max_row = app_df.loc[app_df["flowInd"]==flow_ind].sum()
    pps.append(max_row["pktps"])
    bps.append(max_row["bytps"])

fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.bar(apps, pps)
ax1.set_title("Number of packets per second")
ax2.bar(apps, bps)
ax2.set_xlabel("Number of bytes per second")
plt.show()
save("ppsbps.png")