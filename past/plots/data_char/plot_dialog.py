import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import pandas as pd

plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/dialogue_char"
sns.set_theme()

per_dialog = pickle.load(open("./num_per_dialog.pkl", "rb"))

newper = []
for i in range(len(per_dialog)):
    size = per_dialog[i]
    if size < 32:
        newper.append(size)

perdf = pd.DataFrame({"per_dialog": newper})

plt.hist(data=perdf, x="per_dialog", bins=29)

plt.axvline(x=np.median(per_dialog), color='g', ls='--', label=f'Median number of messages ({np.median(per_dialog)})')
plt.legend(loc='upper right', ncol=2, prop={'size': 9}, borderaxespad=5.5)
plt.title("Number of messages sent per dialog")
plt.savefig(f"{plots_root}/dialog.png")