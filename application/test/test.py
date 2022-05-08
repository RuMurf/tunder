from utils.generate_fingerprint import generate_fingerprint
from utils.add_fingerprint_to_db import *
from utils.match_song import match_song_file
from utils.defaults import *
from pymongo import MongoClient

peak_threshold = 20
target_width = 2

client = MongoClient()
db = client.tunder
collection = "db-fp=100,fps=10,t_start=0.05,t_height=1500,t_width=2,p_th=0"

# match recording
match_song_file("audio/R1-Invaders.wav", footprint=100, fps=10, target_start=0.05, target_height=1500, target_width=2, peak_threshold=0)
# PARAMETERS
# sample_rates = [44100]
footprint_sizes = [100, 60, 30]
target_starts = [0.05, 1]
target_heights = [1500, 3000, 4000]
target_widths = [2, 4, 6]
frames_per_seconds = [5, 10, 50]
peak_thresholds = [20, 10, 0]

for footprint in footprint_sizes:
        for fps in frames_per_seconds:
            for target_start in target_starts:
                for target_height in target_heights:
                    for target_width in target_widths:
                        for peak_threshold in peak_thresholds:
                            match_song_file("audio/R1-Invaders.wav", footprint=footprint, fps = fps, target_start = target_start, target_width = target_width, peak_threshold = peak_threshold)
                            match_song_file("audio/R2-COTD.wav", footprint=footprint, fps = fps, target_start = target_start, target_width = target_width, peak_threshold = peak_threshold)