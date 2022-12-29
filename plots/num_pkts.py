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

num_flows = []
app = "sig"
app_file = get_filename(app)
app_df = pd.read_csv(app_file, delimiter= '\s+', index_col=False)
num_flows.append(app_df["flowInd"].size)

plt.bar(app_df["flowInd"],app_df["numBytesSnt"]+app_df["numBytesRcvd"])
plt.title("Number of bytes per flow for the app Signal")
save("numbytesmes.png")