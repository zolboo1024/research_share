import os
import matplotlib.pyplot as plt
import pandas as pd 
from IPython.display import display
import seaborn as sns
import matplotlib
import pickle
import sys

plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/dialogue_char"
pickle_dir = "/mnt/c/Users/zolbo/whatsapp/whatsapp/data_collection/scripts/dialogue/dialogues.pkl"

if __name__ == "__main__":
    f = open(pickle_dir, "rb")
    dialogues = pickle.load(f)
    f.close()
    num_msgs = []
    for dialogue in dialogues:
        lines = dialogue.split("\r\n")
        if len(lines) == 1:
            lines = dialogue.split("\n")
        if len(lines) == 1:
            continue
        num_msgs.append(len(lines))
    print(len(num_msgs))
    f = open("./num_per_dialog.pkl", "wb")
    pickle.dump(num_msgs, f)
    # plt.xlabel("Number of seconds")
    # plt.ylabel("Flow at port # and its size")
    # plt.xlim([0, maxx])
    # plt.title(f"Web browsing timeline of connections ({len(ports)} connections)")
    # plt.savefig(f"{plots_root}/http_timeline.png",bbox_inches='tight')
    # plt.clf()
