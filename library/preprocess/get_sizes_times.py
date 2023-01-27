from const import *

def get_bursts(name):
    f = open(f"{separated_bursts_root}/{name}_bursts.pkl", "rb")
    return pickle.load(f)

def get_size_time(name):
    bursts = get_bursts(name)
    flows = []
    sizes = []
    timestamps = []
    directions = []
    labels = []
    count = 0
    for app in bursts.keys():
        app_bursts = bursts[app]
        for burst in app_bursts:
            size = []
            timestamp = []
            for pkt in burst.packets:
                size.append(len(pkt))
                timestamp.append(pkt.time)
            flows.append(str(burst.flow))
            directions.append(burst.flow.direction)
            sizes.append(size)
            timestamps.append(timestamp)
            labels.append(app)
            count += len(size)
    print(f"Processed {count} packets")
    df = pd.DataFrame({"flow": flows, "lengths": sizes, "timestamps":timestamps, "directions":directions, "label": labels})
    with open(f"{sizes_times_root}/{name}_sizes-times.pkl", "wb") as f:
        pickle.dump(df,f)

if __name__ == "__main__":
    name = sys.argv[1]
    get_size_time(name)