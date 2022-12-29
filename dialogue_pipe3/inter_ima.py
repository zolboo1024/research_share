from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *

outs = ["youtube","webbrowsing","gmail"]

num_flowss = {
    "sig": 5298,
    "wha": 5633,
    "dis": 7422,
    "tel": 5805,
    "mes": 8890,
    "tea": 24939,
}

total_training = 3179

#get the name of the tranalyzer produced file 
#only applicable for the flow analysis so leaving it here.
def tran_name(app, name):
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/dialogue/trans/{app}_tran/{app}_combined_flows.txt"

def tran_name_out(app):
    return f"{out_pcaps}/{app}_app_tran/{app}_app_flows.txt"

def tran_name_back(app):
    return f"{out_pcaps}/{app}_back_tran/{app}_back_flows.txt"

#direction = A, B or both
#features = all, categorical, statistical, custom_categorical, custom_statistical
def process(name, direction, features, cdic=cdic, cross_validateq=False):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name), delimiter= '\s+', index_col=False)
        df["label"] = "in"
        arr.append(df)
        df = df.sample(n=num_flowss[app])
    for out in outs:
        print("outing")
        df = pd.read_csv(tran_name_out(out), delimiter= '\s+', index_col=False)
        df["label"] = "out"
        df2 = pd.read_csv(tran_name_back(out), delimiter= '\s+', index_col=False)
        df2["label"] = "out"
        arr.append(df)
        arr.append(df2)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    comb = pd.concat(arr)
    comb = choose_features(comb, features, name, typee="inter")
    comb = shuffle(comb)
    
    train_plotrange(comb, ["Inclass", "Outclass"], name, cross_validateq, direction, features, typee="inter")

#direction = A, B or both
#features = all, categorical, statistical, custom_categorical, custom_statistical
def ctree(name,direction,features_type):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name,direction), delimiter= '\s+', index_col=False)
        df["label"] = "in"
        arr.append(df)
    for out in outs:
        print("outing")
        df = pd.read_csv(tran_name_out(out), delimiter= '\s+', index_col=False)
        df["label"] = "out"
        df2 = pd.read_csv(tran_name_back(out), delimiter= '\s+', index_col=False)
        df2["label"] = "out"
        arr.append(df)
        arr.append(df2)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    comb = pd.concat(arr)
    display(comb[comb["label"]=="out"])
    comb = choose_features(comb, features_type)
    comb = shuffle(comb)
    #split the dataset and fit the classifiers
    y = comb["label"]
    X = comb.drop("label", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    y_predic = clf.predict(X_test)
    train_predic = clf.predict(X_train)
    features = X.columns
    importance = clf.feature_importances_
    feat = []
    imps = []
    for i in range(len(importance)):
        feature = features[i]
        imp = np.round(importance[i],3)
        if imp > 0.01:
            imps.append(imp)
            feat.append(feature)
    df = pd.DataFrame({"Feature": feat, "Importance": imps})
    df = df.sort_values(by=["Importance"], ascending=False)
    confusion = confusion_matrix(y_test, y_predic)
    df_cm = pd.DataFrame(confusion, index = ["Inclass","Outclass"], columns = ["Inclass","Outclass"])
    plt.figure(figsize = (10,7))
    sns.heatmap(df_cm, annot=True)
    plt.savefig(f"{plots_root}/inout/heatmap_{name}_{direction}_{features_type}.png")
    export_df(df, f"inout/importance_{name}_{direction}_{features_type}")

def build_count_table(name,direction):
    arr = []
    for i in range(len(apps)):
        app = apps[i]
        df = pd.read_csv(tran_name(app,name), delimiter= '\s+', index_col=False)
        df["label"] = app
        df["inout"] = "Inclass"
        arr.append(df)
    for out in outs:
        df = pd.read_csv(tran_name_out(out), delimiter= '\s+', index_col=False)
        df["label"] = out
        df["inout"] = "Outclass"
        df2 = pd.read_csv(tran_name_back(out), delimiter= '\s+', index_col=False)
        df2["label"] = "background"
        df2["inout"] = "Outclass"
        arr.append(df)
        arr.append(df2)
    all_labels = ["tea", "dis", "sig", "tel", "mes", "wha", "youtube", "webbrowsing", "gmail", "background"]
    fullnames = ["Teams", "Discord", "Signal", "Telegram", "Messenger", "Whatsapp", "Streaming", "Web browsing", "Email", "Background"]
    count_df = pd.concat(arr)
    app_counts = []
    for i in range(len(all_labels)):
        label = all_labels[i]
        app_counts.append(len(count_df[count_df["label"]==label].index))
    count_df = pd.DataFrame({"Setting": fullnames, "Number of Total Flows": app_counts})
    export_df(count_df, f"inout/num_flows")

def import_csv(name, features, direction="both"):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name,direction), delimiter= '\s+', index_col=False)
        df["label"] = "in"
        arr.append(df)
        print(len(df.index))
    for out in outs:
        print("outing")
        df = pd.read_csv(tran_name_out(out), delimiter= '\s+', index_col=False)
        df["label"] = "out"
        df2 = pd.read_csv(tran_name_back(out), delimiter= '\s+', index_col=False)
        df2["label"] = "out"
        arr.append(df)
        arr.append(df2)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    comb = pd.concat(arr)
    comb = choose_features(comb, features)
    comb = shuffle(comb)
    comb = comb.reset_index(drop=True)
    display(comb)
    comb.to_csv(f"{csvs}/{name}_{features}_out.csv", index=False)

if __name__ == "__main__":
    name = sys.argv[1]
    function = sys.argv[2]
    feature_options = ["mutual_info", "all", "categorical", "statistical", "custom_statistical"]
    for feature in feature_options:
        if function == "process":
            process(name,"both",feature, cross_validateq=True)
        if function == "count":
            build_count_table(name)
        # ctree(name,"both",feature)
        #build_count_table(name, "both")
        #import_csv(name, feature)
