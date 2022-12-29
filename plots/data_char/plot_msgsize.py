import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import pandas as pd

plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/dialogue_char"
sns.set_theme()

sizes = pickle.load(open("./message_sizes.pkl", "rb"))
cons_msgs = pickle.load(open("./num_cons.pkl", "rb"))
per_dialog = pickle.load(open("./num_per_dialog.pkl", "rb"))

newsizes = []
for i in range(len(sizes)):
    size = sizes[i]
    if size < 150:
        newsizes.append(size)

sizedf = pd.DataFrame({"sizes": newsizes})
consdf = pd.DataFrame({"cons_msgs": cons_msgs})
perdf = pd.DataFrame({"per_dialog": per_dialog})

plt.hist(data=sizedf, x="sizes", bins=50)
plt.axvline(x=np.median(newsizes), color='g', ls='--', label=f'Median sizes of a message ({np.median(newsizes)})')
plt.legend(loc='upper right', ncol=2, prop={'size': 9}, borderaxespad=5.5)
plt.title("Number of characters sent per message")
plt.savefig(f"{plots_root}/msgsize.png")