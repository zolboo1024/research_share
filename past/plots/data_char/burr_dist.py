from scipy.stats import burr, chi2, gamma, burr12
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plots_root = "/mnt/c/Users/zolbo/whatsapp/whatsapp/plots/dialogue_char"
fig, ax = plt.subplots(1, 1)
sns.set_theme()
c, d = 1.5, 1
mean, var, skew, kurt = burr12.stats(c, d, moments='mvsk')
x = np.linspace(burr12.ppf(0.01, c, d),
                burr12.ppf(0.999, c, d), 1000)
ax.plot(x*7, burr12.pdf(x, c, d),
       'r-', lw=2, alpha=0.6)
plt.axvline(x=7.15, color='g', ls='--', label='Median delay time (6.15 minutes)')
plt.title('Delay time to open a message on an IMA (in minutes)')
ax.set_xlim([0, 60])
fig.legend(loc='upper right', ncol=2, prop={'size': 9}, borderaxespad=5.5)
rv = burr12(c, d)
plt.savefig(f"{plots_root}/burr.png")