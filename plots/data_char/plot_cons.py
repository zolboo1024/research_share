import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import pandas as pd

plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/dialogue_char"
sns.set_theme()

cons_msgs = pickle.load(open("./num_cons.pkl", "rb"))

maxx = 0
for con in cons_msgs:
    if con > maxx:
        maxx = con

# newcons = []
# for i in range(len(newcons)):
#     size = cons_msgs[i]
#     if size < 150:
#         newcons.append(size)

consdf = pd.DataFrame({"cons_msgs": cons_msgs})

plt.hist(data=consdf, x="cons_msgs", bins=maxx)
plt.axvline(x=np.median(cons_msgs), color='g', ls='--', label=f'Median number of messages ({np.median(cons_msgs)})')
plt.legend(loc='upper right', ncol=2, prop={'size': 9}, borderaxespad=5.5)
plt.title("Number of consecutive messages sent in a turn")
plt.savefig(f"{plots_root}/cons.png")