from utils import *

def add_db():
    add_fingerprint_to_db("audio/db/01 Highway To Hell.wav", 60*3+28, db_name="test", collection_name="test", track_id=1)
    print("Done 1")
    add_fingerprint_to_db("audio/db/09 Trouble (with a Capital 'T').wav", 60*3+27, db_name="test", collection_name="test", track_id=2)
    print("Done 2")
    add_fingerprint_to_db("audio/db/14 N17.wav", 60*4+36, db_name="test", collection_name="test", track_id=3)
    print("Done 3")
    add_fingerprint_to_db("audio/db/17 Good Riddance (Time Of Your Life).wav", 60*2+34, db_name="test", collection_name="test", track_id=4)
    print("Done 4")

def match():
    print(match_from_file("sound_files/sound-file-1652125736511.wav", "test", "test"))

match()
