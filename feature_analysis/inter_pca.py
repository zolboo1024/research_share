from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *
from params import * 

outs = ["all", "gmail", "youtube", "webbrowsing"]
out_fullnames = {
    "all": "Background", 
    "gmail": "Mail", 
    "youtube": "Streaming", 
    "webbrowsing": "Web_Browsing"
}
num_flowss = {
    "sig": 5298,
    "wha": 5633,
    "dis": 7422,
    "tel": 5805,
    "mes": 8890,
    "tea": 24939,
}
app_names = {
    "sig": "Signal",
    "wha": "Whatsapp",
    "dis": "Discord",
    "tel": "Telegram",
    "mes": "Messenger",
    "tea": "Teams",
}
app_names_lowercase = {
    "sig": "signal",
    "wha": "whatsapp",
    "dis": "discord",
    "tel": "telegram",
    "mes": "messenger",
    "tea": "teams",
}

total_training = 3179

#get the name of the tranalyzer produced file 
#only applicable for the flow analysis so leaving it here.
def tran_name(app, name):
    return f"{in_pcap_directory}/{app_names[app]}/{app_names_lowercase[app]}_encrypted_traffic_flows.txt"

def tran_name_out(app):
    return f"{out_pcap_directory}/{out_fullnames[app]}/{app}_encrypted_traffic_flows.txt"

pca = PCA()
explained_variance = []
#perform feature selection 
def feature_selection(comb, name, num_features=1):
    global explained_variance
    global pca 

    y, X = input_label(comb)
    np.set_printoptions(suppress=True)
    cols = X.columns
    print(cols)
    #get the pca if it has not been computed 
    if(len(explained_variance) == 0):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)
        explained_variance = pca.explained_variance_ratio_

    df = pd.DataFrame({"Feature": cols, "PCA": explained_variance})
    df = df.sort_values(by="PCA", ascending=False)
    df = df.head(num_features)
    export_df(df, f"{name}/{num_features}_pca")
    return comb[df["Feature"].tolist()]

#choose features depending on any of these qualifiers: categorical, statistical, customs, mutual-info based and all features
def choose_features(comb, features, name, num_features=1, typee="intra"):
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
    to_drop = ["macStat", "connSipDprt", "macPairs", "srcMac_dstMac_numP",	
        "srcMacLbl_dstMacLbl", "srcMac", "dstMac", "srcPort", "hdrDesc", "duration"]
    for each in to_drop:
        if each in comb.columns:
            comb = comb.drop(each, axis=1)
    for col in comb.columns:
        if comb[col].dtype == "object":
            nonnumeric_cols.append(col)
            comb[col] = comb[col].astype("category").cat.codes
    
    #drop the categorical features
    comb = comb.drop(nonnumeric_cols, axis=1)

    #only packet size features
    #comb = comb[["label","numPktsSnt",	"numPktsRcvd",	"numBytesSnt",	"numBytesRcvd",	"minPktSz",	"maxPktSz",	"avePktSize",	"stdPktSize",	"minIAT",	"maxIAT",	"aveIAT",	"stdIAT",	"bytps"]]

    if features == "mutual_info":
        comb = feature_selection(comb, name, num_features=num_features)
        comb["label"] = labels
    return comb


#direction = A, B or both
#features = all, categorical, statistical, custom_categorical, custom_statistical
def process(name, direction, features, num_features=1, cdic=cdic, cross_validateq=False):
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
        arr.append(df)
    Path(f"{plots_root}/{name}").mkdir(parents=True, exist_ok=True)
    comb = pd.concat(arr)
    comb = choose_features(comb, features, name, num_features=num_features, typee="inter")
    comb = shuffle(comb)
    
    arr = []
    f1_ranges = []
    accur_ranges = []
    pred_ranges = []
    recall_ranges = []
    clf_name = "Random Forest"
    clf = cdic[clf_name]
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
    export_df(df, f"{name}/{num_features}_pca_table")
    return min(f1s)

if __name__ == "__main__":
    name = sys.argv[1]
    function = "process"
    feature = "mutual_info"
    f1s = []
    for i in range(1, 21):
        f1s.append(process(name,"both",feature, num_features=i, cross_validateq=True))
    with open("f1s_out_pca.pkl", "wb") as f:
        pickle.dump(f1s, f)
    with open("f1s_out_pca_variance.pkl", "wb") as f:
        pickle.dump(explained_variance, f)