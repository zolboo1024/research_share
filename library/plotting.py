from dictionaries import * 
from sklearn_packages import * 
from base_packages import *
from directories import *
from flow_df_functions import *

#takes the list of clfs and evaluates it
#with one fold and produce a table that contains
#the 4 big indicators for each of the clfs.
def train_plot(clfs, X, y, name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    arr1 = []
    for i in range(len(clfs)):
        clf = clfs[i]
        clf.fit(X_train, y_train)
        y_predic = clf.predict(X_test)
        train_predic = clf.predict(X_train)
        accuracy_test = str(np.round(accuracy_score(y_test, y_predic), num_decimal))
        accuracy_train = str(np.round(accuracy_score(y_train, train_predic), num_decimal))
        recall_test = str(np.round(recall_score(y_test, y_predic, average=avg_strat), num_decimal))
        recall_train = str(np.round(recall_score(y_train, train_predic, average=avg_strat), num_decimal))
        f1_test = str(np.round(f1_score(y_test, y_predic, average=avg_strat), num_decimal))
        f1_train = str(np.round(f1_score(y_train, train_predic, average=avg_strat), num_decimal))
        precision_test = str(np.round(precision_score(y_test, y_predic, average=avg_strat), num_decimal))
        precision_train = str(np.round(precision_score(y_train, train_predic, average=avg_strat), num_decimal))
        arr1.append([accuracy_test, precision_test, recall_test, f1_test, accuracy_train, precision_train, recall_train, f1_train])
        df = pd.DataFrame(data=arr1, columns=["Accuracy", "Precision", "Recall", "F1 score", "Training Accuracy", "Training Precision", "Training Recall", "Training F1"])
        export_df(df, f"{name}/{name}_results")
        confusion = confusion_matrix(y_test, y_predic)
        df_cm = pd.DataFrame(confusion, index = apps_fullname, columns = apps_fullname)
        plt.figure(figsize = (10,7))
        sns.heatmap(df_cm, annot=True)
        plt.savefig(f"{plots_root}/{name}/{name}_heatmap.png")
    return arr1

#makes a confusion matrix from the test and predicted values
def export_cm(y_test, y_predic, name, block_names=apps_fullname):
    confusion = confusion_matrix(y_test, y_predic)
    df_cm = pd.DataFrame(confusion, index = block_names, columns = block_names)
    plt.figure(figsize = (10,7))
    sns.heatmap(df_cm, annot=True)
    plt.savefig(f"{plots_root}/{name}.png")

#takes a df and prints out using the IPython library into an PNG
def export_df(df, name):
    df_styled = df.style.background_gradient() #adding a gradient based on values in cell
    dfi.export(df_styled, f'{plots_root}/{name}.png')

#takes a df and prints out using the IPython library into an PNG
def export_df_full(df, name):
    df_styled = df.style.background_gradient() #adding a gradient based on values in cell
    dfi.export(df_styled, f'{name}.png')