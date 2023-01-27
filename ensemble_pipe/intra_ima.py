from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *

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

#features = all, categorical, statistical, custom_categorical, custom_statistical
#make dfs for the experiment name (name), do 10-fold cross-validation
#and produce the range for the metrics in each of the 10 folds
def process(name, direction, features, cdic=cdic, cross_validateq=False):
    arr = []
    for app in apps:
          df = pd.read_csv(tran_name(app,name), delimiter= '\s+', index_col=False)
        print(len(df.index))
        print(num_flowss[app])
        df = df.sample(n=num_flowss[app])
        df["label"] = app
        arr.append(df)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    comb = pd.concat(arr)
    comb = choose_features(comb, features, name)
    comb = shuffle(comb)

    arr = []
    f1_ranges = []
    accur_ranges = []
    pred_ranges = []
    recall_ranges = []
    for clf_name in cdic.keys():
        clf = cdic[clf_name]
        print(clf_name)
        if cross_validateq == False:
            print("splitting correctly")
            xy_train = comb.groupby("label").sample(n=3179, random_state=1)
            x_train = xy_train.drop("label", axis=1)
            y_train = xy_train["label"]
            xy_test = comb.drop(xy_train.index)
            x_test = xy_test.drop("label", axis=1)
            y_test = xy_test['label']
            clf.fit(x_train, y_train)
            y_predic = clf.predict(x_test)
            train_predic = clf.predict(x_train)
            arr.append([accuracy_score(y_test, y_predic), *score(y_test, y_predic, average='macro')[:3]])
        else:
            print("old split")
            f1s = []
            accurs = []
            precs = []
            recalls = []
            for i in range(1,11):
                xy_train = comb.groupby("label").sample(n=3179, random_state=i)
                x_train = xy_train.drop("label", axis=1)
                y_train = xy_train["label"]
                xy_test = comb.drop(xy_train.index)
                x_test = xy_test.drop("label", axis=1)
                y_test = xy_test['label']
                clf.fit(x_train, y_train)
                y_predic = clf.predict(x_test)
                train_predic = clf.predict(x_train)
                accurs.append(accuracy_score(y_test, y_predic))
                scoress = score(y_test, y_predic, average='macro')
                f1s.append(scoress[2])
                precs.append(scoress[0])
                recalls.append(scoress[1])
            f1_ranges.append(f"{round(min(f1s),3)}-{round(max(f1s),3)}")
            accur_ranges.append(f"{round(min(accurs),3)}-{round(max(accurs),3)}")
            pred_ranges.append(f"{round(min(precs),3)}-{round(max(precs),3)}")
            recall_ranges.append(f"{round(min(recalls),3)}-{round(max(recalls),3)}")
            df = pd.DataFrame({"Accuracy": accurs, "Precision": precs, "Recall": recalls, "F1": f1s})
            export_df(df, f"{name}/{name}_fold_{clf_name}_{direction}_{features}")
            
    if cross_validateq == True:
        df = pd.DataFrame({"Model": cdic_names, "Accuracy": accur_ranges, "Precision": pred_ranges, "Recall": recall_ranges, "F1": f1_ranges})
        df["mins"] = df["Accuracy"].map(lambda x: float(x.split("-")[0]))
        df.sort_values(by=["mins"], ascending=False)
        df = df.drop("mins", axis=1)
        export_df(df, f"{name}/all_models_range/{name}_{features}_compare_models")
    if cross_validateq == False:
        df = pd.DataFrame(arr, columns=["Accuracy","Precision","Recall","F1"])
        df["Classifier"] = cdic.keys()
        export_df(df, f"{name}/{name}_allclass_{clf_name}_{direction}_{features}")

def build_count_table(name):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name), delimiter= '\s+', index_col=False)
        df["label"] = app
        arr.append(df)
    count_df = pd.concat(arr)
    app_counts = []
    for i in range(len(apps)):
        app = apps[i]
        to_add = len(count_df[count_df["label"]==app].index)
        app_counts.append(to_add)
    count_df = pd.DataFrame({"App": apps_fullname, "Number of Total Flows": app_counts})
    export_df(count_df, f"{name}/num_flows_{name}")

if __name__ == "__main__":
    name = sys.argv[1]
    function = sys.argv[2]
    feature_options = ["all", "categorical", "statistical", "custom_statistical"]
    for feature in feature_options:
        if function == "process":
            process(name,"both",feature, cross_validateq=True)
        if function == "count":
            build_count_table(name)
        #ctree(name,"both",feature)
        #import_csv(name, feature)