from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *
from params import *

num_flowss = {
    "sig": 5298,
    "wha": 5633,
    "dis": 7422,
    "tel": 5805,
    "mes": 8890,
    "tea": 24939,
}

total_training = 3179

all_apps = {
    "sig", "wha", "dis", "tel", "mes", "tea"
}

three_apps = {
    "wha", "dis", "tel"
}

models = ["Random Forest"]

#get the name of the tranalyzer produced file 
#only applicable for the flow analysis so leaving it here.
def tran_name(app, name):
    return f"/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/dialogue/trans/{app}_tran/{app}_combined_flows.txt"

def import_datasets(apps):
    arr = []
    for app in apps:
        print(app)
        df = pd.read_csv(tran_name(app,name), delimiter= '\s+', index_col=False)
        print(len(df.index))
        print(num_flowss[app])
        df = df.sample(n=num_flowss[app])
        df["label"] = app
        arr.append(df)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    comb = pd.concat(arr)
    return comb

#choose features depending on any of these qualifiers: categorical, statistical, customs, mutual-info based and all features
def choose_features(comb, features, name):
    if typee == "inter":
        to_num = {
            "in": 0,
            "out": 1
        }
        comb["label"] = comb["label"].map(lambda x: to_num[x])
    else:
        comb["label"] = comb["label"].map(lambda x: app_to_num[x])
    labels = comb["label"]

    comb = comb[["label","numPktsSnt",	"numPktsRcvd",	"numBytesSnt",	"numBytesRcvd",	
                    "minPktSz",	"maxPktSz",	"avePktSize",	"stdPktSize",	"minIAT",	
                        "maxIAT",	"aveIAT",	"stdIAT",	"bytps"]]

    comb = shuffle(comb)
    return comb


def train_each_class(comb, classes):
    trained_model = {}
    for model in models:
        clf = cdic[model]

        arr = []
        f1_ranges = []
        pred_ranges = []
        recall_ranges = []

        dis_scores = []
        mes_scores = []
        tel_scores = []
        tea_scores = []
        wha_scores = []
        sig_scores = []

        all_scores = [dis_scores, mes_scores, tel_scores, tea_scores, wha_scores, sig_scores]

        if classes == "subset":
            all_scores = [dis_scores, tel_scores, wha_scores]


        for i in range(1,11):
            xy_train = comb.groupby("label").sample(n=3179, random_state=i)
            x_train = xy_train.drop("label", axis=1)
            y_train = xy_train["label"]
            print(y_train)
            xy_test = comb.drop(xy_train.index)
            x_test = xy_test.drop("label", axis=1)
            y_test = xy_test['label']
            clf.fit(x_train, y_train)
            y_predic = clf.predict(x_test)
            train_predic = clf.predict(x_train)

            for j in range(len(all_scores)):
                all_scores[j].append([])

            recalls = recall_score(y_test, y_predic, average=None)
            print(recalls)
            for j in range(len(all_scores)):
                all_scores[j][-1].append(recalls[j])

            precisions = precision_score(y_test, y_predic, average=None)
            for j in range(len(all_scores)):
                all_scores[j][-1].append(precisions[j])

            f1s = f1_score(y_test, y_predic, average=None)
            for j in range(len(all_scores)):
                all_scores[j][-1].append(f1s[j])

        for i in range(len(apps)):
            all_recalls = []
            for j in range(10): #iteration
                all_recalls.append(all_scores[i][j][0])
            recall_ranges.append(f"{round(min(all_recalls),3)}-{round(max(all_recalls),3)}")
        
        for i in range(len(apps)):
            all_precisions = []
            for j in range(10): #iteration
                all_precisions.append(all_scores[i][j][1])
            pred_ranges.append(f"{round(min(all_precisions),3)}-{round(max(all_precisions),3)}")

        for i in range(len(apps)):
            all_f1s = []
            for j in range(10): #iteration
                all_f1s.append(all_scores[i][j][2])
            f1_ranges.append(f"{round(min(all_f1s),3)}-{round(max(all_f1s),3)}")
            
        df = pd.DataFrame({"IMA Class": apps_fullname, "Precision": pred_ranges, "Recall": recall_ranges, "F1": f1_ranges})
        export_df(df, f"{name}/{name}_{features}_compare_classes")
