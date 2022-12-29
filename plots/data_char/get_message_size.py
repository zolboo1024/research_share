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
    msg_sizes = []
    for dialogue in dialogues:
        lines = dialogue.split("\r\n")
        if len(lines) == 1:
            lines = dialogue.split("\n")
        if len(lines) == 1:
            continue
        firstspeakername = lines[0].split(":\ ")[0]
        secondspeakername = lines[1].split(":\ ")[0]
        i = 2
        #in case the first messages are double texts
        while secondspeakername == firstspeakername:
            secondspeakername = lines[i].split(":\ ")[0]
            i += 1
        for line in lines:
            splitt = line.split(":\ ")
            if len(splitt) == 1:
                continue
            speakername = splitt[0]
            message = splitt[1]
            msg_sizes.append(len(message))
    print(len(msg_sizes))
    f = open("./message_sizes.pkl", "wb")
    pickle.dump(msg_sizes, f)
    # plt.xlabel("Number of seconds")
    # plt.ylabel("Flow at port # and its size")
    # plt.xlim([0, maxx])
    # plt.title(f"Web browsing timeline of connections ({len(ports)} connections)")
    # plt.savefig(f"{plots_root}/http_timeline.png",bbox_inches='tight')
    # plt.clf()
