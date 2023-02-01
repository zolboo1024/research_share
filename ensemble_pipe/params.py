num_flowss = {
    "sig": 5298,
    "wha": 5633,
    "dis": 7422,
    "tel": 5805,
    "mes": 8890,
    "tea": 24939,
}

total_training = 3179

reclassify_threshold = 0.9

all_apps = [
    "sig", "wha", "dis", "tel", "mes", "tea"
]

all_apps_fullname = [
    "Discord","Messenger","Telegram","Teams","Whatsapp","Signal"
]
three_apps = [
    "wha", "dis", "tel"
]

three_apps_fullname = [
    "Discord","Telegram","Whatsapp"
]

model = "Random Forest"

size_timing_features = ["label","numPktsSnt",	"numPktsRcvd",	"numBytesSnt",	"numBytesRcvd",	
                    "minPktSz",	"maxPktSz",	"avePktSize",	"stdPktSize",	"minIAT",	
                        "maxIAT",	"aveIAT",	"stdIAT",	"bytps"]

plot_folder = "/home/zolboo/back/research/ensemble_pipe/plots"