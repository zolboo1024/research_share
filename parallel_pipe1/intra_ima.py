from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *

total_training = 3179
#get the name of the tranalyzer produced file 
#only applicable for the flow analysis so leaving it here.
def non_tran_name(app, name):
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/dialogue/trans/{app}_tran/{app}_combined_flows.txt"

#get the name of the tranalyzer produced file 
#only applicable for the flow analysis so leaving it here.
def parallel_tran_name(app, name):
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/parallel1/trans/{app}_tran/{app}_combined_flows.txt"

#features = all, categorical, statistical, custom_categorical, custom_statistical
#make dfs for the experiment name (name), do 10-fold cross-validation
#and produce the range for the metrics in each of the 10 folds
def process(name, direction, features, cdic=cdic, cross_validateq=False):
    arr = []
    accurs = []
    precs = []
    recalls = []
    f1s = []
    confs = []
    for app in apps:
        print(app)
        parallel_df = pd.read_csv(parallel_tran_name(app,name), delimiter= '\s+', index_col=False)
        non_df = pd.read_csv(non_tran_name(app,name), delimiter= '\s+', index_col=False)

        print(len(parallel_df.index))
        non_df = non_df.sample(n=len(parallel_df.index))
        non_df["label"] = "out"
        parallel_df["label"] = "in"
        comb = pd.concat([parallel_df, non_df])
        comb = choose_features(comb, features, name, typee="inter")
        comb = shuffle(comb)
        clf = cdic["Random Forest"]

        y = comb["label"]
        X = comb.drop("label", axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
        clf.fit(X_train, y_train)
        y_predic = clf.predict(X_test)
        predictions = clf.predict_proba(X_test)
        best_confs = []
        for prediction in predictions:
            best_confs.append(max(prediction))
        confs.append(sum(best_confs)/len(best_confs))
        train_predic = clf.predict(X_train)
        all_scores = [accuracy_score(y_test, y_predic), *score(y_test, y_predic, average='macro')[:3]]
        accurs.append(all_scores[0])
        precs.append(all_scores[1])
        recalls.append(all_scores[2])
        f1s.append(all_scores[3])

        importance = clf.feature_importances_
        featuress = X.columns
        feat = []
        imps = []
        for i in range(len(importance)):
            feature = featuress[i]
            imp = importance[i]
            if imp > 0.01:
                imps.append(imp)
                feat.append(feature)
        if len(imps) > 8:
            imps = imps[:8]
            feat = feat[:8]
        df = pd.DataFrame({"Feature": feat, "Importance": imps})
        df = df.sort_values(by=["Importance"], ascending=False)
        export_df(df, f"{name}/importance_{app}_{features}")

    df = pd.DataFrame({"App Name": apps_fullname, "Accuracy": accurs, "Precision": precs, "Recall": recalls, "F1": f1s, "Confidence (Probability)": confs})
    export_df(df, f"{name}/{features}")

if __name__ == "__main__":
    name = sys.argv[1]
    feature_options = ["all", "categorical", "statistical", "custom_statistical"]
    for feature in feature_options:
        process(name,"both",feature, cross_validateq=True)