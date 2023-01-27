from base_packages import *
from directories import *

def get_df(name):
    f = open(f"{sizes_times_root}/{name}_sizes-times.pkl", "rb")
    return pickle.load(f)

def train_result(name, cross_validateq=False):
    df = build_table(name)
    df = shuffle(df)
    y = df["cat"]
    X = df.drop(["cat"], axis=1)
    X = X.drop(["timestamps","lengths","directions","label"], axis=1)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    display(X)
    for clf_name in cdic.keys():
        clf = cdic[clf_name]
        if cross_validateq == False:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
            clf.fit(X_train, y_train)
            y_predic = clf.predict(X_test)
            train_predic = clf.predict(X_train)
            accuracy_test = np.round(accuracy_score(y_test, y_predic), 2)
            accuracy_train = np.round(accuracy_score(y_train, train_predic), 2)
            print(f"{clf_name}: {accuracy_test} {accuracy_train}")
        else:
            _scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
            scores = cross_validate(estimator=clf,
                                X=X,
                                y=y,
                                cv=10,
                                scoring=_scoring,
                                return_train_score=True)
            df = pd.DataFrame({"Accuracy": scores["test_accuracy"], "Precision": scores["test_precision_macro"], "Recall": scores["test_recall_macro"], "F1": scores["test_f1_macro"]})
            export_df(df, f"{name}/{name}_fold_{clf_name}")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
            clf.fit(X_train, y_train)
            y_predic = clf.predict(X_test)
            export_cm(y_test, y_predic, f"{name}/{name}_cm_{clf_name}")

def build_table(name):
    df = get_df(name)
    df["duration"] = df["timestamps"].map(lambda x: x[-1]-x[0])
    df["numPkts"] = df["lengths"].map(lambda x: len(x))
    df["numBytes"] = df["lengths"].map(lambda x: np.sum(x))
    df["avgPktSize"] = df["lengths"].map(lambda x: np.average(x))
    df["stdPktSize"] = df["lengths"].map(lambda x: np.std(x))
    df["minPktSize"] = df["lengths"].map(lambda x: np.amin(x))
    df["maxPktSize"] = df["lengths"].map(lambda x: np.amax(x))
    df["pps"] = df["timestamps"].map(lambda x: 0 if (x[-1]-x[0])==0 else len(x)/(x[-1]-x[0]))
    df["cat"] = df["label"].map(lambda x: app_to_num[x])
    df["flow"] = df["flow"].astype("category").cat.codes
    df["direction_cat"] = df["directions"].astype("category").cat.codes
    return df

def neural_network(name,cross_valid=False):
    df = build_table(name)
    clf = MLPClassifier()
    df["timestamps"] = df["timestamps"].map(lambda x: np.subtract(x, np.amin(x)))
    df["size"] = df["timestamps"].map(lambda x: len(x))
    stamps = df["timestamps"].map(lambda x: np.array(x)).to_numpy()
    sizes = df["lengths"].map(lambda x: np.array(x)).to_numpy()
    y = df["cat"]
    X = []
    Path(f'{plots_root}/{name}').mkdir(parents=True, exist_ok=True)
    for i in range(len(stamps)):
        stamp = stamps[i]
        size = sizes[i]
        arr = []
        for j in range(20):
            if j > len(stamp)-1:
                arr.append(0)
                arr.append(0)
            else:
                arr.append(stamp[j])
                arr.append(size[j])
        X.append(arr)
    if cross_valid:
        _scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
        results = cross_validate(estimator=clf,
                                X=X,
                                y=y,
                                cv=10,
                                scoring=_scoring,
                                return_train_score=True)
        print(results)
        with open(f"{sizes_times_root}/{name}_fold_results","wb") as f:
            pickle.dump(results, f)
        cross_validatee(name)
    else:
        results = train_plot([clf], X, y, name)
        print(results)

def cross_validatee(name):
    f = open(f"{sizes_times_root}/{name}_fold_results","rb") 
    scores = pickle.load(f)
    df = pd.DataFrame({"Accuracy": scores["test_accuracy"], "Precision": scores["test_precision_macro"], "Recall": scores["test_recall_macro"], "F1": scores["test_f1_macro"]})
    export_df(df, f"{name}_cross_neural")

if __name__ == "__main__":
    name = sys.argv[1]
    func = sys.argv[2]
    if "neural" in func:
        neural_network(name)
    elif "cross_neural" in func:
        neural_network(name, cross_validate=True)
    elif "all_class" in func:
        train_result(name, True)
    else:
        print("Wrong arguments")

