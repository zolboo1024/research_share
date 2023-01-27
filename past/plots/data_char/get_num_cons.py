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
    num_cons = []
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

        lastSpeaker = firstspeakername
        curNum = 1
        for i in range(1, len(lines)):
            line = lines[i]
            splitt = line.split(":\ ")
            if len(splitt) == 1:
                continue
            speakername = splitt[0]
            if speakername == lastSpeaker:
                curNum += 1
            else:
                num_cons.append(curNum)
                curNum = 1
            lastSpeaker = speakername
        num_cons.append(curNum)
    print(len(num_cons))
    f = open("./num_cons.pkl", "wb")
    pickle.dump(num_cons, f)
    # plt.xlabel("Number of seconds")
    # plt.ylabel("Flow at port # and its size")
    # plt.xlim([0, maxx])
    # plt.title(f"Web browsing timeline of connections ({len(ports)} connections)")
    # plt.savefig(f"{plots_root}/http_timeline.png",bbox_inches='tight')
    # plt.clf()