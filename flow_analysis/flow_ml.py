from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *

#get the name of the tranalyzer produced file 
#only applicable for the flow analysis so leaving it here.
def tran_name(app, name):
    return f"{port_pcaps}/{app}_{name}_tran/{app}_{name}_combined_flows.txt"

#direction = A, B or both
#features = all, categorical, statistical, custom_categorical, custom_statistical
#make dfs for the experiment name (name), do 10-fold cross-validation
#and produce the range for the metrics in each of the 10 folds
def process(name, direction, features, cdic=cdic, cross_validateq=False):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name,direction), delimiter= '\s+', index_col=False)
        df_dic[app] = df
        df["label"] = app
        arr.append(df)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    comb = pd.concat(arr)
    comb = choose_features(comb, features)
    comb = shuffle(comb)
    #split the dataset and fit the classifiers
    y = comb["label"]
    X = comb.drop("label", axis=1)
    arr = []
    f1_ranges = []
    accur_ranges = []
    pred_ranges = []
    recall_ranges = []
    for clf_name in cdic.keys():
        clf = cdic[clf_name]
        print(clf_name)
        if cross_validateq == False:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
            clf.fit(X_train, y_train)
            y_predic = clf.predict(X_test)
            train_predic = clf.predict(X_train)
            arr.append([accuracy_score(y_test, y_predic), *score(y_test, y_predic, average='macro')[:3]])
        else:
            _scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
            scores = cross_validate(estimator=clf,
                                X=X,
                                y=y,
                                cv=10,
                                scoring=_scoring,
                                return_train_score=True)
            print(scores)
            f1s = scores["test_f1_macro"]
            f1_ranges.append(f"{round(min(f1s),4)}-{round(max(f1s),4)}")
            accurs = scores["test_accuracy"]
            accur_ranges.append(f"{round(min(accurs),4)}-{round(max(accurs),4)}")
            precs = scores["test_precision_macro"]
            pred_ranges.append(f"{round(min(precs),4)}-{round(max(precs),4)}")
            recalls = scores["test_recall_macro"]
            recall_ranges.append(f"{round(min(recalls),4)}-{round(max(recalls),4)}")
            df = pd.DataFrame({"Accuracy": accurs, "Precision": precs, "Recall": recalls, "F1": f1s})
            export_df(df, f"{name}/{name}_fold_{clf_name}_{direction}_{features}")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
            clf.fit(X_train, y_train)
            y_predic = clf.predict(X_test)
            export_cm(y_test, y_predic, f"{name}/{name}_cm_{clf_name}_{direction}_{features}", apps_fullname=["Discord", "Messenger", "Teams", "Telegram", "Whatsapp", "Signal"])
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

#direction = A, B or both
#features = all, categorical, statistical, custom_categorical, custom_statistical
def ctree(namess,direction,features_type):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name,direction), delimiter= '\s+', index_col=False)
        df_dic[app] = df
        df["label"] = app
        arr.append(df)
    comb = pd.concat(arr)
    comb = choose_features(comb, features_type)
    #split the dataset and fit the tree
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
    df_cm = pd.DataFrame(confusion, index = app_full, columns = app_full)
    plt.figure(figsize = (10,7))
    sns.heatmap(df_cm, annot=True)
    plt.savefig(f"{plots_root}/heatmap_{namess}_{direction}_{features_type}.png")
    export_df(df, f"{name}/importance_{namess}_{direction}_{features_type}")

def build_count_table(name,direction):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name,direction), delimiter= '\s+', index_col=False)
        df_dic[app] = df
        df["label"] = app
        arr.append(df)
    count_df = pd.concat(arr)
    app_counts = []
    for i in range(len(apps)):
        app = apps[i]
        app_counts.append(len(count_df[count_df["label"]==app].index))
    count_df = pd.DataFrame({"App": app_full, "Number of Total Flows": app_counts})
    export_df(count_df, f"{name}/num_flows_{name}_{direction}")

if __name__ == "__main__":
    name = sys.argv[1]
    feature_options = ["mutual_info"]
    #, "all", "categorical", "statistical", "custom_categorical", "custom_statistical"]
    for feature in feature_options:
        process(name,"both",feature, cross_validateq=True)
        #build_count_table(name, "both")
        #ctree(name,"both",feature)
        #import_csv(name, feature)