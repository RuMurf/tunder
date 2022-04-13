from pymongo import MongoClient
from tqdm import tqdm
from utils.generate_fingerprint import generate_fingerprint
from utils.defaults import *

def generate_fingerprint_add_to_db(file, track_id=None, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    collection_name = "db-fp="+str(footprint)+",fps="+str(fps)+",t_start="+str(target_start)+",t_height="+str(target_height)+",t_width="+str(target_width)+",p_th="+str(peak_threshold)
    client = MongoClient("mongodb://localhost:27017")
    db = client["tunder"]
    collection = db[collection_name]
    if collection.find_one({"track_id": track_id}):
        print("Error: collection "+collection_name+" already contains track id "+str(track_id))
        return
    fingerprint = generate_fingerprint(file, track_id, footprint, fps, target_start, target_height, target_width, peak_threshold)
    if len(fingerprint) > 1:
        collection.insert_many(fingerprint)
    

def generate_multiple_fingerprints_add_to_db(files, track_ids=None, footprints=[FOOTPRINT_SIZE], fpss=[FRAMES_PER_SECOND], target_starts=[TARGET_START], target_heights=[TARGET_HEIGHT], target_widths=[TARGET_WIDTH], peak_thresholds=[PEAK_THRESHOLD]):
    if track_ids is None:
        track_ids = range(1, len(files)+1)

    counter = 1
    for footprint in footprints:
        for fps in fpss:
            for target_start in target_starts:
                for target_height in target_heights:
                    for target_width in target_widths:
                        for peak_threshold in peak_thresholds:
                            for file, track_id in zip(files, track_ids):
                                generate_fingerprint_add_to_db(file, track_id, footprint, fps, target_start, target_height, target_width, peak_threshold)
                            print("CREATED "+str(counter)+" DATABASES OUT OF "+str(len(footprints)*len(fpss)*len(target_starts)*len(target_heights)*len(target_widths)*len(peak_thresholds)))
                            counter += 1
