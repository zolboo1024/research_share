import os
import numpy as np
import seaborn as sns
import matplotlib
import sys
import pickle 
import pandas as pd
import matplotlib.pyplot as plot

timestamps = "/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/experiments/timestamps.pkl"
plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/misc"

stamps = ""

with open(timestamps, "rb") as f:
    stamps = pickle.load(f)

curstamp = stamps[0]
delays = []
for i in range(1, len(stamps)):
    stamp = stamps[i]
    delay = stamp - curstamp
    if delay < 200:
        delays.append(delay)
    curstamp = stamp
print(min(delays))
print(max(delays))
print(np.mean(delays))
# delays = np.array(delays)
# delays = pd.DataFrame({"Delay between messages(in seconds)": delays})
# histplot = sns.histplot(data=delays, x="Delay between messages(in seconds)", kde=True)
# fig = histplot.get_figure()
# fig.savefig(f"{plots_root}/stamps1.png") 