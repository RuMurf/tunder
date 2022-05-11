from src.utils import *


DB_NAME = "parameter_tuning"
COLLECTION_NAME = "test 1"

def add_to_db(db_name, collection_name, peak_factor=PEAK_FACTOR, sample_rate= SAMPLE_RATE, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, t_start=TARGET_START, t_height=TARGET_HEIGHT, t_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    collection = get_collection(db_name, collection_name)
    collection.insert_one({
        "peak_factor": peak_factor,
        "sample_rate": sample_rate,
        "footprint": footprint,
        "fps": fps,
        "t_start": t_start,
        "t_height": t_height,
        "t_width": t_width,
        "peak_threshold": peak_threshold
    })
    add_fingerprint_to_db("audio/db/01 Highway To Hell.wav", 60*3+28, db_name=db_name, collection_name=collection_name, track_id=1, peak_factor=peak_factor, sample_rate=sample_rate, footprint=footprint, fps=fps, t_start=t_start, t_height=t_height, t_width=t_width, peak_threshold=peak_threshold)
    print("Done 1")
    add_fingerprint_to_db("audio/db/02 Trouble (with a Capital 'T').wav", 60*3+27, db_name=db_name, collection_name=collection_name, track_id=2)
    print("Done 2")
    add_fingerprint_to_db("audio/db/03 N17.wav", 60*4+36, db_name=db_name, collection_name=collection_name, track_id=3)
    print("Done 3")
    add_fingerprint_to_db("audio/db/04 Good Riddance (Time Of Your Life).wav", 60*2+34, db_name=db_name, collection_name=collection_name, track_id=4)
    print("Done 4")

def match():
    print(match_from_file("sound_files/sound-file-1652123624894.wav", "tunder", "fingerprints"))


add_to_db(DB_NAME, "test 12", peak_threshold=10)