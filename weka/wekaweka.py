from const import *

apps = ["dis", "mes", "tea", "tel", "wha", "sig"]
app_full = ["Discord", "Messenger", "Teams", "Telegram", "Whatsapp", "Signal"]

def tran_name(app, name, direction="both"):
    if direction == "both":
        return f"{port_pcaps}/{app}_{name}_tran/{app}_{name}_combined_flows.txt"
    else:
        return f"{port_pcaps}/{app}_{name}_tran/{app}_{name}_combined_flows.txt"

def input_label(df):
    labels = df["label"]
    inputs = df.drop("label", axis=1)
    return labels, inputs

def choose_features(comb, features):
    comb["label"] = comb["label"].map(lambda x: app_to_num[x])
    #convert categorical values into number values
    #now just trying the categorical values
    nonnumeric_cols = []
    comb = comb.fillna(0)
    comb = comb.drop(["timeFirst","timeLast","flowInd"], axis=1)
    to_drop = ["macStat",	"macPairs", "srcMac_dstMac_numP",	"srcMacLbl_dstMacLbl", "srcMac", "dstMac", "srcPort", "hdrDesc"]
    for each in to_drop:
        if each in comb.columns:
            comb = comb.drop(each, axis=1)
    for col in comb.columns:
        if comb[col].dtype == "object":
            nonnumeric_cols.append(col)
            comb[col] = comb[col].astype("category").cat.codes
    if features == "all":
        pass
    if features == "categorical":
        comb = comb[["label", *nonnumeric_cols]]
    if features == "statistical":
        comb = comb.drop(nonnumeric_cols, axis=1)
    if features == "custom_categorical":
        comb = comb[["dstIPOrg","srcIPOrg","%dir","dstPortClass", "label"]]
    if features == "custom_statistical":
        comb = comb[["label","duration", "numPktsSnt",	"numPktsRcvd",	"numBytesSnt",	"numBytesRcvd",	"minPktSz",	"maxPktSz",	"avePktSize",	"stdPktSize",	"minIAT",	"maxIAT",	"aveIAT",	"stdIAT",	"bytps"]]
    return comb

#direction = A, B or both
#features = all, categorical, statistical, custom_categorical, custom_statistical
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
            df = pd.DataFrame({"Accuracy": scores["test_accuracy"], "Precision": scores["test_precision_macro"], "Recall": scores["test_recall_macro"], "F1": scores["test_f1_macro"]})
            export_df(df, f"{name}/{name}_fold_{clf_name}_{direction}_{features}")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
            clf.fit(X_train, y_train)
            y_predic = clf.predict(X_test)
            export_cm(y_test, y_predic, f"{name}/{name}_cm_{clf_name}_{direction}_{features}", apps_fullname=["Discord", "Messenger", "Teams", "Telegram", "Whatsapp", "Signal"])
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
    feature_options = ["all", "categorical", "statistical", "custom_categorical", "custom_statistical"]
    for feature in feature_options:
        process(name,"both",feature, cross_validateq=False)
        #build_count_table(name, "both")
        #ctree(name,"both",feature)