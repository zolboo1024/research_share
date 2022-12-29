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
    mins.append(max_row["minPktSz"])
    maxes.append(max_row["maxPktSz"])
    means.append(max_row["avePktSize"])
    std.append(max_row["stdPktSize"])
means = np.array(means)
maxes = np.array(maxes)
std = np.array(std)
mins = np.array(mins)
# create stacked errorbars:
plt.errorbar(apps, means, std, fmt='ok', lw=3)
plt.errorbar(apps, means, [means - mins, maxes - means],
             fmt='.k', ecolor='gray', lw=1)
plt.title("Packet size distribution (mean, std, min and max)")
plt.xlim(-1, 6)
save("pktsize.png")

