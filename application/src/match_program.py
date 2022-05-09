
import sys
sys.path.append('C:\\Users\\Ruairi\\Projects\\tunder\\application')
from pymongo import MongoClient
from matplotlib import pyplot as plt
from utils.generate_fingerprint import generate_fingerprint
from utils.defaults import *
import math

file = sys.argv[1]

# def match_song(file):
fingerprint = generate_fingerprint(file, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH)
collection_name = "db-fp=100,fps=10,t_start=0.05,t_height=1500,t_width=2,p_th=0" #"db-fp=" + str(footprint) + ",fps=" + str(fps) + ",t_start=" + str(target_start) + ",t_height=" + str(target_height) + ",t_width=" + str(target_width)+",p_th="+str(peak_threshold)
client = MongoClient(CONNECTION_STRING)
db = client["tunder"]
    
collection = db[collection_name]

matching_hashes = []
time_ds = {}
for f_hash in fingerprint:
    for db_hash in collection.find({"hash": f_hash["hash"]}):
        if db_hash["time_d"] - f_hash["time_d"] > 0 and db_hash["time_d"] - f_hash["time_d"] < TARGET_WIDTH*FRAMES_PER_SECOND:
            if db_hash["track_id"] not in time_ds:
                time_ds[db_hash["track_id"]] = []
            time_ds[db_hash["track_id"]].append(db_hash["time_d"] - f_hash["time_d"])

match_results = {}
for key in time_ds:
    match_results[key] = 0


if len(match_results) > 1:
    fig, figs = plt.subplots(1, len(time_ds), sharex=True, sharey=True)
    for i in range(len(figs)):
        figs[i].set_title("Track "+str(i+1))
        n, bins, patches = figs[i].hist(time_ds[i+1])
        if not math.isnan(max(n)):
            match_results[i] = max(n)
    best_match = 0
    result = 0
    for i in range(len(match_results)):
        if match_results[i] > best_match:
            best_match = match_results[i]
            result = i+1
else:
    result = match_results.popitem()[0]

print(result)
sys.stdout.flush()