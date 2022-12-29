#functions to manipulate the features (getting certain types of features)
from directories import *
from dictionaries import *
from base_packages import *
from directories import *
from sklearn_packages import *
from plotting import *

def all_features(df):
    df = df.drop(["lengths","timestamps","directions", "label"],axis=1)
    return df

def only_stat_features(df):
    df = df.drop(["lengths", "timestamps","directions", "label", "flow"],axis=1)
    return df

def out_all_features(df):
    df = df[df["directions"]=="A"]
    return df

def in_all_features(df):
    df = df[df["directions"]=="B"]
    return df

def in_stat_features(df):
    df = df[df["directions"]=="B"]
    return df

def out_stat_features(df):
    df = df[df["directions"]=="A"]
    return df

#separate the df into the X and y. The first returned is the y
#and the second one is the X
def input_label(df):
    labels = df["label"]
    inputs = df.drop("label", axis=1)
    return labels, inputs

#perform feature selection 
def feature_selection(comb, name):
    y, X = input_label(comb)
    np.set_printoptions(suppress=True)
    cols = X.columns
    #get the mutual information
    infos = np.array(mutual_info_classif(X, y)).astype(np.float)
    dic = dict(zip(cols, infos))
    new_dic = {}
    #only consider features that have a MI of over 0.2
    for col in dic.keys():
        if dic[col] > 0.2:
            new_dic[col] = dic[col]
    df = pd.DataFrame({"Feature": new_dic.keys(), "Mutual Information": new_dic.values()})
    export_df(df, f"{name}/mutual_info_features")
    return comb[new_dic.keys()]

#choose features depending on any of these qualifiers: categorical, statistical, customs, mutual-info based and all features
def choose_features(comb, features, name, typee="intra"):
    if typee == "inter":
        to_num = {
            "in": 0,
            "out": 1
        }
        comb["label"] = comb["label"].map(lambda x: to_num[x])
    else:
        comb["label"] = comb["label"].map(lambda x: app_to_num[x])
    labels = comb["label"]
    #convert categorical values into number values
    #now just trying the categorical values
    nonnumeric_cols = []
    comb = comb.fillna(0)
    comb = comb.drop(["timeFirst","timeLast","flowInd"], axis=1)
    to_drop = ["macStat",	"macPairs", "srcMac_dstMac_numP",	"srcMacLbl_dstMacLbl", "srcMac", "dstMac", "srcPort", "hdrDesc", "duration"]
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
        comb = comb[["label","numPktsSnt",	"numPktsRcvd",	"numBytesSnt",	"numBytesRcvd",	"minPktSz",	"maxPktSz",	"avePktSize",	"stdPktSize",	"minIAT",	"maxIAT",	"aveIAT",	"stdIAT",	"bytps"]]
    if features == "mutual_info":
        comb = feature_selection(comb, name)
        comb["label"] = labels
    return comb


#get the csv file of the tranalyzer file for each of the apps
#and display it
def import_csv(name, features, typee):
    arr = []
    for app in apps:
        df = pd.read_csv(tran_name(app,name,"both"), delimiter= '\s+', index_col=False)
        df_dic[app] = df
        df["label"] = app
        arr.append(df)
    comb = pd.concat(arr)
    comb = choose_features(comb, features, name, typee)
    comb = shuffle(comb)
    comb = comb.reset_index(drop=True)
    display(comb)
    comb.to_csv(f"{csvs}/{name}_{features}.csv", index=False)


def train_plotrange(comb, labels, name, cross_validateq, direction, features, typee):
    #split the dataset and fit the classifiers
    y, X = input_label(comb)
    arr = []
    name = name + labels[0]
    f1_ranges = []
    accur_ranges = []
    pred_ranges = []
    recall_ranges = []
    for clf_name in cdic.keys():
        clf = cdic[clf_name]
        print(clf_name)
        #if the cross validation is false- just do one split training with 0.6-0.4
        if cross_validateq == False:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
            clf.fit(X_train, y_train)
            y_predic = clf.predict(X_test)
            train_predic = clf.predict(X_train)
            arr.append([accuracy_score(y_test, y_predic), *score(y_test, y_predic, average='macro')[:3]])
        #if the cross validate is true, do 10-fold cross validation and print out the range
        else:
            _scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
            scores = cross_validate(estimator=clf,
                                X=X,
                                y=y,
                                cv=10,
                                scoring=_scoring,
                                return_train_score=True)
            print(scores)
            #save up the scores into an array for each metric
            f1s = scores["test_f1_macro"]
            f1_ranges.append(f"{round(min(f1s),3)}-{round(max(f1s),3)}")
            accurs = scores["test_accuracy"]
            accur_ranges.append(f"{round(min(accurs),3)}-{round(max(accurs),3)}")
            precs = scores["test_precision_macro"]
            pred_ranges.append(f"{round(min(precs),3)}-{round(max(precs),3)}")
            recalls = scores["test_recall_macro"]
            recall_ranges.append(f"{round(min(recalls),3)}-{round(max(recalls),3)}")
            df = pd.DataFrame({"Accuracy": accurs, "Precision": precs, "Recall": recalls, "F1": f1s})
            export_df(df, f"{name}_fold_{clf_name}_{direction}_{features}")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
            clf.fit(X_train, y_train)
            y_predic = clf.predict(X_test)
            export_cm(y_test, y_predic, f"{name}_cm_{clf_name}_{direction}_{features}", block_names=labels)
    #print out the ranges if we have to cross-validate
    if cross_validateq == True:
        df = pd.DataFrame({"Model": cdic_names, "Accuracy": accur_ranges, "Precision": pred_ranges, "Recall": recall_ranges, "F1": f1_ranges})
        df["mins"] = df["Accuracy"].map(lambda x: float(x.split("-")[0]))
        df.sort_values(by=["mins"], ascending=False)
        df = df.drop("mins", axis=1)
        export_df(df, f"d3_out/all_models_range/{name}_{features}_compare_models")
    if cross_validateq == False:
        df = pd.DataFrame(arr, columns=["Accuracy","Precision","Recall","F1"])
        df["Classifier"] = cdic.keys()
        export_df(df, f"{name}_allclass_{clf_name}_{direction}_{features}")