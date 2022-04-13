from utils.generate_spectrogram import generate_spectrogram
from utils.generate_starmap import generate_starmap
from utils.get_hashes import get_hashes
from utils.defaults import *

def generate_fingerprint(file, track_id=None, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH):
    spectrogram = generate_spectrogram(file, fps)
    peaks, peaks_x, peaks_y = generate_starmap(spectrogram, footprint)
    fingerprint = get_hashes(spectrogram, peaks, track_id, target_start, target_height, target_width, fps)
    return fingerprint
