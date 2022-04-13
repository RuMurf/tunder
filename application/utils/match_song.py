from pymongo import MongoClient
from matplotlib import pyplot as plt
from utils.generate_fingerprint import generate_fingerprint
from utils.defaults import *
# from config import *

def match_song_fingerprint(fingerprint, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    collection_name = "db-fp=" + str(footprint) + ",fps=" + str(fps) + ",t_start=" + str(target_start) + ",t_height=" + str(target_height) + ",t_width=" + str(target_width)+",p_th="+str(peak_threshold)
    client = MongoClient(CONNECTION_STRING)
    db = client["tunder"]
    collection = db[collection_name]
    
    print("Querying Database...")
    matching_hashes = []
    time_ds = {1: [], 2: [], 3: [], 4: []}
    for f_hash in fingerprint:
        for db_hash in collection.find({"hash": f_hash["hash"]}):
            if db_hash["time_d"] - f_hash["time_d"] > 0 and db_hash["time_d"] - f_hash["time_d"] < target_width*fps:
                time_ds[db_hash["track_id"]].append(db_hash["time_d"] - f_hash["time_d"])
    print(time_ds)
    fig, figs = plt.subplots(1, len(time_ds), sharex=True, sharey=True)
    for i in range(len(figs)):
        figs[i].set_title("Track "+str(i+1))
        figs[i].hist(time_ds[i+1])
    plt.savefig("edata/statistics/"+collection_name+".png")
    plt.show()

def match_song_file(file, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    fingerprint = generate_fingerprint(file, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH)
    file_id = file.split("/")[-1].split("-")[0]
    collection_name = "db-fp=" + str(footprint) + ",fps=" + str(fps) + ",t_start=" + str(target_start) + ",t_height=" + str(target_height) + ",t_width=" + str(target_width)+",p_th="+str(peak_threshold)
    client = MongoClient(CONNECTION_STRING)
    db = client["tunder"]
    collection = db[collection_name]
    
    print("Querying Database...")
    matching_hashes = []
    time_ds = {1: [], 2: [], 3: [], 4: []}
    for f_hash in fingerprint:
        for db_hash in collection.find({"hash": f_hash["hash"]}):
            if db_hash["time_d"] - f_hash["time_d"] > 0 and db_hash["time_d"] - f_hash["time_d"] < target_width*fps:
                time_ds[db_hash["track_id"]].append(db_hash["time_d"] - f_hash["time_d"])
    print(time_ds)
    fig, figs = plt.subplots(1, len(time_ds), sharex=True, sharey=True)
    for i in range(len(figs)):
        figs[i].set_title("Track "+str(i+1))
        figs[i].hist(time_ds[i+1])
    plt.savefig("edata/statistics/"+file_id+"-"+collection_name+".png")
    plt.show()


    # for hash_point in collection.find({"hash": {'$in': [d["hash"] for d in fingerprint]}}):
    #     matching_hashes.append(hash_point)
    #
    # print("Evaluating Matches...")
    # match_time_ds = {}
    # for matching_hash in matching_hashes:
    #     for f_hash in fingerprint:
    #         if f_hash["hash"] == matching_hash["hash"]:
    #             if matching_hash["track_id"] not in match_time_ds:
    #                 match_time_ds[matching_hash["track_id"]] = [matching_hash["time_d"] - f_hash["time_d"]]
    #             elif matching_hash["time_d"] - f_hash["time_d"] >= 0:
    #             # else:
    #                 match_time_ds[matching_hash["track_id"]].append(matching_hash["time_d"] - f_hash["time_d"])
    # print(match_time_ds)
    # fig, (fig1, fig2) = plt.subplots(1,2, sharex=True, sharey=True)
    # fig1.hist(match_time_ds[1])
    # fig2.hist(match_time_ds[2])
    # plt.savefig(PROJECT_DIR+"edata/statistics/"+collection_name+".png")
    # plt.show()

