from base_packages import *
from directories import *
from flow_df_functions import *
from sklearn_packages import *
from plotting import *
from params import *
from functions import *

def split_dataset(comb):
    xy_train = comb.groupby("label").sample(n=total_training, random_state=1)
    x_train = xy_train.drop("label", axis=1)
    y_train = xy_train["label"]
    xy_test = comb.drop(xy_train.index)
    x_test = xy_test.drop("label", axis=1)
    y_test = xy_test['label']
    return x_train, y_train, x_test, y_test

def get_both_models():
    print("Building the three class model")
    #model for the three classes
    subset_comb = import_datasets(three_apps)
    subset_comb = choose_features(subset_comb)
    subset_rf = get_trained_model(subset_comb)

    print("Building the all class model")
    #initial model for all the classes
    comb = import_datasets(all_apps)
    comb = choose_features(comb)
    all_rf = get_trained_model(comb)

    return subset_rf, all_rf, comb

def get_confidence_and_pipe_based():
    name = sys.argv[1]
    print("Starting confidence and pipe based ensemble")
    subset_rf, all_rf, comb = get_both_models()

    #get the training and testing dataset for the main problem (all classes)
    x_train, y_train, x_test, y_test = split_dataset(comb)

    print("Building the confidence-pipe based model")
    y_predic = all_rf.predict(x_test)

    print_scores(y_test, y_predic, all_apps_fullname, name+"_before")

    indexes_to_replace = []
    probs = all_rf.predict_proba(x_test)
    for i in range(len(y_predic)):
        prob_chosen = max(probs[i]) #probability of the chosen class
        if prob_chosen < reclassify_threshold and (y_predic[i] == 0 or y_predic[i] == 2 or y_predic[i] == 4):
            indexes_to_replace.append(i)
    x_to_reclassify = x_test.iloc[indexes_to_replace]
    new_classification = subset_rf.predict(x_to_reclassify)
    for i in range(len(indexes_to_replace)):
        cur_index = indexes_to_replace[i]
        new_y = new_classification[i]
        y_predic[cur_index] = new_y
    
    print_scores(y_test, y_predic, all_apps_fullname, name+"_after")


def get_confidence_based():
    name = sys.argv[1]
    print("Starting confidence-based ensemble")
    subset_rf, all_rf, comb = get_both_models()

    #get the training and testing dataset for the main problem (all classes)
    x_train, y_train, x_test, y_test = split_dataset(comb)

    print("Building the confidence based model")
    y_predic = all_rf.predict(x_test)

    print_scores(y_test, y_predic, all_apps_fullname, name+"_before")

    indexes_to_replace = []
    probs = all_rf.predict_proba(x_test)
    for i in range(len(y_predic)):
        prob_chosen = max(probs[i]) #probability of the chosen class
        if prob_chosen < reclassify_threshold:
            indexes_to_replace.append(i)
    x_to_reclassify = x_test.iloc[indexes_to_replace]
    new_classification = subset_rf.predict(x_to_reclassify)
    for i in range(len(indexes_to_replace)):
        cur_index = indexes_to_replace[i]
        new_y = new_classification[i]
        y_predic[cur_index] = new_y
    
    print_scores(y_test, y_predic, all_apps_fullname, name+"_after")

def get_pipe():
    name = sys.argv[1]
    print("Starting pipe-based ensemble")
    subset_rf, all_rf, comb = get_both_models()
    #get the training and testing dataset for the main problem (all classes)
    x_train, y_train, x_test, y_test = split_dataset(comb)

    #saving the initial model
    y_predic = all_rf.predict(x_test)
    print_scores(y_test, y_predic, all_apps_fullname, name+"_before")

    print("Building the pipe model")

    indexes_to_replace = []
    for i in range(len(y_predic)):
        if y_predic[i] == 0 or y_predic[i] == 2 or y_predic[i] == 4:
            indexes_to_replace.append(i)  
    x_to_reclassify = x_test.iloc[indexes_to_replace]
    y_true_to_reclassify = y_test.iloc[indexes_to_replace]
    new_classification = subset_rf.predict(x_to_reclassify)
    print_scores(y_true_to_reclassify, new_classification, all_apps_fullname, name+"_only_reclassified")
    for i in range(len(indexes_to_replace)):
        cur_index = indexes_to_replace[i]
        new_y = new_classification[i]
        y_predic[cur_index] = new_y
    
    print_scores(y_test, y_predic, all_apps_fullname, name+"_after")


def get_ensemble():
    name = sys.argv[1]
    print("Starting ensemble-based ensemble")
    subset_rf, all_rf, comb = get_both_models()

    #get the training and testing dataset for the main problem (all classes)
    x_train, y_train, x_test, y_test = split_dataset(comb)

    #convert the train dataset
    rf_all_x_train = all_rf.predict(x_train)
    rf_three_x_train = subset_rf.predict(x_train)
    x_train_new = pd.DataFrame({"Feature 1": rf_all_x_train, "Feature 2": rf_three_x_train})

    #convert the test dataset
    rf_all_x_test = all_rf.predict(x_test)
    rf_three_x_test = subset_rf.predict(x_test)

    print_scores(y_test, rf_all_x_test, all_apps_fullname, name+"_before")

    three_rf_recalls = precision_score(y_test, rf_three_x_test, average=None)
    all_rf_recalls = precision_score(y_test, rf_all_x_test, average=None)
    print(three_rf_recalls)
    print(all_rf_recalls)

    x_test_new = pd.DataFrame({"Feature 1": rf_all_x_test, "Feature 2": rf_three_x_test})

    print("Building the ensemble model")
    #build a model on the new x
    clf = cdic[model]
    clf.fit(x_train_new, y_train)
    y_predic = clf.predict(x_test_new)

    print_scores(y_test, y_predic, all_apps_fullname, name+"_after")

    

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

def train_separately():
    name = sys.argv[1]
    print("Starting for all classes")
    process(name,"all")
    print("Starting for the three subclasses")
    process(name,"subclasses")

if __name__ == "__main__":
    get_pipe()