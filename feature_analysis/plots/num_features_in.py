import os
import matplotlib.pyplot as plt
import pandas as pd 
from IPython.display import display
import numpy as np
import seaborn as sns
import matplotlib
import sys
import pickle 

sns.set_theme()
f1s_loc = "/Users/zolboo/research/research/feature_analysis/f1s.pkl"
f1s_pkts = "/Users/zolboo/research/research/feature_analysis/f1s_pkts.pkl"
f1s_pca = "/Users/zolboo/research/research/feature_analysis/f1s_pca.pkl"
f1s_pca_pkts = "/Users/zolboo/research/research/feature_analysis/f1s_pca_pkts.pkl"
f1s_variance = "/Users/zolboo/research/research/feature_analysis/f1s_pca_variance.pkl"
f1s_variance_pkts = "/Users/zolboo/research/research/feature_analysis/f1s_pca_variance_pkts.pkl"  

with open(f1s_loc, "rb") as f:
    f1s = pickle.load(f)
    nums = range(1, 21)
    plt.plot(nums, f1s, color="g", label="Using Mutual Information Features")
    plt.xlabel("Number of features")
    plt.ylabel("F1 Score (lowest of all the splits)")
    plt.axhline(y = 0.99, color="r", label="Using all statistical features")
    plt.title(f"F1 Score as features are added")

with open(f1s_pca, "rb") as f:
    f1s = pickle.load(f)
    nums = range(1, 21)
    plt.plot(nums, f1s, label="Using PCA Features")
    plt.legend(bbox_to_anchor = (1, 0), loc = 'lower right')
    plt.savefig(f"num_features_in_all.png")
    plt.clf()

with open(f1s_pkts, "rb") as f:
    f1s = pickle.load(f)
    nums = range(1, 14)
    plt.plot(nums, f1s, color="g", label="Using Mutual Information Features")


with open(f1s_pca_pkts, "rb") as f:
    f1s = pickle.load(f)
    nums = range(1, 14)
    plt.plot(nums, f1s, label="Using PCA Features")
    plt.xlabel("Number of features")
    plt.ylabel("F1 (lowest of all the splits)")
    plt.axhline(y = 0.81, color="r", label="Using all packet size/timing features")
    plt.title(f"F1 Score as features are added")
    plt.legend(bbox_to_anchor = (1, 0), loc = 'lower right')
    plt.savefig(f"num_features_in_pkts.png")
    plt.clf()

with open(f1s_variance, "rb") as f:
    f1s = pickle.load(f)
    nums = range(1, len(f1s)+1)
    plt.plot(nums, f1s)
    plt.xlabel("Each of the features")
    plt.ylabel("Explained Variance")
    plt.title(f"Variance of the features with the highest variance")
    plt.legend(bbox_to_anchor = (1, 0), loc = 'lower right')
    plt.savefig(f"num_features_in_variance.png")
    plt.clf()

with open(f1s_variance_pkts, "rb") as f:
    f1s = pickle.load(f)
    nums = range(1, len(f1s)+1)
    plt.plot(nums, f1s)
    plt.xlabel("Each of the features")
    plt.ylabel("Explained Variance")
    plt.title(f"Variance of the features with the highest variance")
    plt.legend(bbox_to_anchor = (1, 0), loc = 'lower right')
    plt.savefig(f"num_features_in_variance_pkts.png")
    plt.clf()