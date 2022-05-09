from utils.generate_fingerprint import *
import csv
from pymongo import MongoClient
from tqdm import tqdm

# PARAMETERS
# sample_rates = [44100]
footprint_sizes = [100, 60, 30]
target_starts = [0.05, 1]
target_heights = [1500, 3000, 4000]
target_widths = [2, 4, 6]
frames_per_seconds = [5, 10, 50]
peak_thresholds = [20, 10, 0]
files = ["audio/R1-Invaders.wav", "audio/R2-COTD.wav"]

# initialize csv for results
csv_titles = "Track 1 Result, Track 2 Result, footprint, t_start, t_height, t_width, fps, peak_threshold"
csv_file = open("parameters.csv", "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(csv_titles)

# run tests
for footprint in tqdm(footprint_sizes):                     
    for t_start in target_starts:
        for t_height in target_heights:
            for t_width in target_widths:
                for fps in frames_per_seconds:
                    for peak_threshold in peak_thresholds:
                        sample_fingerprint = generate_fingerprint(file, footprint=footprint, target_start=t_start, target_height=t_height, target_width=t_width, fps=fps, peak_threshold=peak_threshold)
                                                    
                        for db_footprint in footprint_sizes:
                            for db_t_start in target_starts:
                                for db_t_height in  target_heights:
                                    for db_t_width in target_widths:
                                        for db_fps in frames_per_seconds:
                                            for db_peak_threshold in peak_thresholds:
                                                for file in files:
                                                    db = MongoClient(CONNECTION_STRING)["tunder"]
                                                    print(db.list_collection_names)




fingerprint = generate_fingerprint(file, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH)
file_id = file.split("/")[-1].split("-")[0]
#collection_name =  "db-fp=100,fps=10,t_start=0.05,t_height=1500,t_width=2,p_th=0" #"db-fp=" + str(footprint) + ",fps=" + str(fps) + ",t_start=" + str(target_start) + ",t_height=" + str(target_height) + ",t_width=" + str(target_width)+",p_th="+str(peak_threshold)
client = MongoClient(CONNECTION_STRING)
db = client["tunder"]
for collection_name in db.list_collection_names():
    
    collection = db[collection_name]
    
    print("Querying Database...")
    matching_hashes = []
    time_ds = {1: [], 2: [], 3: [], 4: []}
    for f_hash in fingerprint:
        for db_hash in collection.find({"hash": f_hash["hash"]}):
            if db_hash["time_d"] - f_hash["time_d"] > 0 and db_hash["time_d"] - f_hash["time_d"] < target_width*fps:
                time_ds[db_hash["track_id"]].append(db_hash["time_d"] - f_hash["time_d"])
    print(time_ds)
    match_results = [0, 0, 0, 0]
    fig, figs = plt.subplots(1, len(time_ds), sharex=True, sharey=True)
    for i in range(len(figs)):
        figs[i].set_title("Track "+str(i+1))
        n, bins, patches = figs[i].hist(time_ds[i+1])
        if not math.isnan(max(n)/sum(n)):
            match_results[i] = max(n)/sum(n)
    plt.savefig("edata/statistics/"+file_id+"-"+collection_name+".png")
    plt.show()
    print("match results:"+str(match_results))