import numpy as np
from scipy.ndimage import maximum_filter
from tqdm import tqdm
from sys import argv
from utils.defaults import *

def generate_starmap(spectrogram, footprint=FOOTPRINT_SIZE, peak_threshold=PEAK_THRESHOLD):
    print("Generating Starmap... [footprint="+str(footprint)+"]")
    filtered_spectrogram = maximum_filter(spectrogram, footprint)
    peaks = []
    peaks_x = []
    peaks_y = []
    for i in tqdm(range(spectrogram.shape[0])):
        for j in range(spectrogram.shape[1]):
            if spectrogram[i][j] == filtered_spectrogram[i][j] and filtered_spectrogram[i][j] > peak_threshold:
                peaks.append([i,j])
                peaks_x.append(i)
                peaks_y.append(j)
    print("Starmap Generated!")
    return peaks, peaks_x, peaks_y
