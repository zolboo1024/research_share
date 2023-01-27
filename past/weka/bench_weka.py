from const import *

features = ["all", "statistical", "categorical", "all_out", "statistical_out", "categorical_out"]
#, "custom_categorical", "custom_statistical", "all_out", "statistical_out", "categorical_out", "custom_categorical_out", "custom_statistical_out"]
models = ["rf", "tree", "gb", "mlp"]
model_names = ["Random Forest", "Random Tree", "Gradient Boost", "Multi-Layer Perceptron"]


def get_predics(feature, model):
    #all_splits[i][0] is an array of all actual values for the ith split
    #all_splits[i][1] is an array of all predic values for the ith split
    all_splits = []
    with open(f"{csvs}/weka_{feature}_{model}.txt") as f:
        lines = f.readlines()
        cur_accs = []
        cur_predics = []
        last_index = 1
        for i in range(len(lines)):
            line = lines[i].strip().split(",")
            if len(line) > 1 and line[0].isnumeric():
                if int(line[0])<last_index:
                    all_splits.append([cur_accs, cur_predics])
                    cur_accs = []
                    cur_predics = []
                acc = int(line[1])
                predic = line[2]
                if predic=="?":
                    predic = 0
                else:
                    predic = int(round(float(predic)))
                cur_accs.append(acc)
                cur_predics.append(predic)
                last_index=int(line[0])
        all_splits.append([cur_accs, cur_predics])
        print(len(all_splits))
    return all_splits

if __name__ == "__main__":
    for i in range(len(features)):
        feature = features[i]
        f1_ranges = []
        accur_ranges = []
        pred_ranges = []
        recall_ranges = []
        for j in range(4):
            model = models[j]
            print(model)
            all_splits = get_predics(feature, model)
            all_f1s = []
            all_recalls = []
            all_accs = []
            all_precis = []
            for split in all_splits:
                acc = split[0]
                preds = split[1]
                accur = accuracy_score(acc, preds)
                f1 = f1_score(acc, preds, average=avg_strat)
                prec = precision_score(acc, preds, average=avg_strat)
                recall = recall_score(acc, preds, average=avg_strat)
                print([accur, f1, recall, prec])
                all_f1s.append(round(f1,4))
                all_recalls.append(round(recall,4))
                all_accs.append(round(accur,4))
                all_precis.append(round(prec,4))
            f1_ranges.append(f"{min(all_f1s)}-{max(all_f1s)}")
            accur_ranges.append(f"{min(all_recalls)}-{max(all_recalls)}")
            pred_ranges.append(f"{min(all_accs)}-{max(all_accs)}")
            recall_ranges.append(f"{min(all_precis)}-{max(all_precis)}")
        df = pd.DataFrame({"Model": model_names, "Accuracy": accur_ranges, "F1": f1_ranges, "Recall": recall_ranges, "Precision": pred_ranges})
        export_df(df, f"weka/{feature}")
            
                