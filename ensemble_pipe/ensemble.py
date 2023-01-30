from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *
from params import *
from functions import *

#features = all, categorical, statistical, custom_categorical, custom_statistical
#make dfs for the experiment name (name), do 10-fold cross-validation
#and produce the range for the metrics in each of the 10 folds
def process(name, classes):

    if classes == "all":
        #do all the apps first
        comb = import_datasets(all_apps)
        comb = choose_features(comb)
        train_and_plot(comb, classes, name)
    elif classes == "subclasses":
        #do all the apps first
        comb = import_datasets(three_apps)
        comb = choose_features(comb)
        train_and_plot(comb, classes, name)
    else:
        print("invalid case")

if __name__ == "__main__":
    name = sys.argv[1]
    print("Starting for all classes")
    process(name,"all")
    print("Starting for the three subclasses")
    process(name,"subclasses")