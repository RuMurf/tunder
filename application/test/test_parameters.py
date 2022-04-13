from utils.match_song import match_song_file
from utils.generate_fingerprint import generate_fingerprint
from utils.add_fingerprint_to_db import *
from utils.defaults import *

# PARAMETERS
# sample_rates = [44100]
footprint_sizes = [100, 60, 30]
target_starts = [0.05, 1]
target_heights = [1500, 3000, 4000]
target_widths = [2, 4, 6]
frames_per_seconds = [5, 10, 50]
peak_thresholds = [20, 10, 0]

# DB FILES
db_directory = "audio/db/"
db_files = [db_directory+"01 Invaders.wav", db_directory+"02 Children Of The Damned.wav", db_directory+"03 The Prisoner.wav", db_directory+"04 22 Acacia Avenue.wav"]

# generate databases
generate_multiple_fingerprints_add_to_db(db_files, footprints=footprint_sizes, fpss=frames_per_seconds, target_starts=target_starts, target_heights=target_heights, target_widths=target_widths, peak_thresholds=peak_thresholds)

# TEST RECORDING FILES
recordings = ["audio/R1-Invaders.wav", "audio/R2-COTD.wav"]
