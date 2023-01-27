from scipy.stats import burr, chi2, gamma, burr12, norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/dialogue_char"
fig, ax = plt.subplots(1, 1)
sns.set_theme()
x = np.random.normal(loc=18.7, scale=5, size=100)
sns.distplot(x, color='r', hist=False)
plt.axvline(x=18.7, color='g', ls='--', label='Median delay time (18.7 seconds)')
plt.title('Average time spent on typing and sending a message (in seconds)')
ax.set_xlim([0, 45])
fig.legend(loc='upper right', ncol=2, prop={'size': 9}, borderaxespad=5.5)
plt.savefig(f"{plots_root}/norm.png")