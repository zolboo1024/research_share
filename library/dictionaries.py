#apps is the array of app codes
#apps_fullname is the array of the full names for the apps
#app to num is a dictionary of it translating it to an index
#fullnames is an array of the full names
#cdic is the dictionary of all the models used
#cdic_names is the array of all the model names

from sklearn_packages import *

apps = ["dis","mes","tel","tea","wha","sig"]
apps_fullname = ["Discord","Messenger","Telegram","Teams","Whatsapp","Signal"]

app_to_num = {
    "dis": 0,
    "mes": 1,
    "tel": 2,
    "tea": 3,
    "wha": 4,
    "sig": 5
}

fullnames = {
    "dis": "Discord",
    "mes": "Messenger",
    "tel": "Telegram",
    "tea": "Teams",
    "wha": "Whatsapp",
    "sig": "Signal"
}

cdic = {
    "Nearest Neighbors": KNeighborsClassifier(),
    "Linear SVM": SVC(tol=1e-5, max_iter=100),
    "C4.5 Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "Neural Net": MLPClassifier(max_iter=50),
    "Naive Bayes": GaussianNB(),
    "Logistic Regression": LogisticRegression(),
    "Gradient Boost": GradientBoostingClassifier(),
    #"AdaBoost": AdaBoostClassifier(),
    #"Gaussian Process": GaussianProcessClassifier(1.0 * RBF(1.0)),
}

cdic_names = [
    "Nearest Neighbors",
    "Linear SVM",
    "C4.5 Decision Tree",
    "Random Forest",
    "Neural Net",
    "Naive Bayes",
    "Logistic Regression",
    "Gradient Boost"
]