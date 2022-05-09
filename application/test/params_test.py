from src.utils import *

def add_db():
    add_fingerprint_to_db("audio/db/01 Highway To Hell.wav", 60*3+28, db_name="tunder", collection_name="fingerprints", track_id=1)
    print("Done 1")
    add_fingerprint_to_db("audio/db/02 Trouble (with a Capital 'T').wav", 60*3+27, db_name="tunder", collection_name="fingerprints", track_id=2)
    print("Done 2")
    add_fingerprint_to_db("audio/db/03 N17.wav", 60*4+36, db_name="tunder", collection_name="fingerprints", track_id=3)
    print("Done 3")
    add_fingerprint_to_db("audio/db/04 Good Riddance (Time Of Your Life).wav", 60*2+34, db_name="tunder", collection_name="fingerprints", track_id=4)
    print("Done 4")
    add_fingerprint_to_db("audio/db/05 Run To The Hills.wav", 60*3+53, db_name="tunder", collection_name="songs", track_id=5)
    print("Done 5")

def match():
    print(match_from_file("sound_files/sound-file-1652123624894.wav", "tunder", "fingerprints"))

match()
