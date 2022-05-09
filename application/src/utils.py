from sys import stderr
from madmom.audio.signal import Signal, FramedSignal
from madmom.audio.spectrogram import Spectrogram
from pyparsing import col
from scipy.ndimage import maximum_filter
from pymongo import MongoClient
import math
from matplotlib import pyplot as plt

# Defaults
SAMPLE_RATE = 44100
FOOTPRINT_SIZE = 30
TARGET_START = 0.05
TARGET_HEIGHT = 4000
TARGET_WIDTH = 2
FRAMES_PER_SECOND = 5
PEAK_THRESHOLD = 0
PEAK_FACTOR = 100
CONNECTION_STRING = "mongodb://localhost:27017"
DB = "tunder"
COLLECTION = "fingerprints"

def get_collection(db_name=DB, collection_name=COLLECTION, connection_string=CONNECTION_STRING):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]
    return collection

def generate_spectrogram(filepath, sample_rate=SAMPLE_RATE, fps=FRAMES_PER_SECOND):
    signal = Signal(filepath, sample_rate=SAMPLE_RATE, num_channels=1)
    framed_signal = FramedSignal(signal, fps=fps)
    spectrogram = Spectrogram(framed_signal)
    return spectrogram

def generate_starmap(spectrogram, footprint=FOOTPRINT_SIZE, peak_threshold=PEAK_THRESHOLD):
    filtered_spectrogram = maximum_filter(spectrogram, footprint)
    peaks = []
    peaks_x = []
    peaks_y = []
    for i in range(spectrogram.shape[0]):
        for j in range(spectrogram.shape[1]):
            if spectrogram[i][j] == filtered_spectrogram[i][j] and filtered_spectrogram[i][j] > peak_threshold:
                peaks.append([i,j])
                peaks_x.append(i)
                peaks_y.append(j)
    return peaks, peaks_x, peaks_y

def generate_ordered_starmap(spectrogram, track_length, footprint=FOOTPRINT_SIZE, peak_threshold=PEAK_THRESHOLD, peak_factor=PEAK_FACTOR):
    filtered_spectrogram = maximum_filter(spectrogram, footprint)
    peaks = {}
    peaks_x = []
    peaks_y = []
    for i in range(spectrogram.shape[0]):
        for j in range(spectrogram.shape[1]):
            if spectrogram[i][j] == filtered_spectrogram[i][j] and filtered_spectrogram[i][j] > peak_threshold:
                if spectrogram[i][j] not in peaks:
                    peaks[spectrogram[i][j]] = []
                peaks[spectrogram[i][j]].append([i,j])
                peaks_x.append(i)
                peaks_y.append(j)
    sorted_peaks = dict(sorted(peaks.items(), reverse=True))
    max_peaks = []
    for peak in sorted_peaks.items():
        if len(max_peaks) >= peak_factor * track_length:
            break
        for coord in peak[1]:
            max_peaks.append(coord)
    print(max_peaks)
    return max_peaks, peaks_x, peaks_y

def get_hashes(spectrogram, peaks, track_id=None, t_start=TARGET_START, t_height=TARGET_HEIGHT, t_width=TARGET_WIDTH, fps=FRAMES_PER_SECOND):
    frequency_bin_size = spectrogram.bin_frequencies[1]

    t_start = int(t_start * fps)
    t_height = int(t_height//frequency_bin_size)
    t_width = int(t_width * fps)
    fingerprint = []

    for peak in peaks:
        try:
            for i in range((peak[0]+t_start), (peak[0]+t_width)):
                for j in range((peak[1]-t_height//2), (peak[1]+t_height//2)):
                    if [i, j] in peaks:
                        fingerprint.append({"hash": str(peak[1])+"-"+str(j)+"-"+str((i - peak[0])), "track_id": track_id, "time_d": peak[0]})
        except IndexError:
            continue
    return fingerprint

def generate_fingerprint(file, track_id=None, sample_rate= SAMPLE_RATE, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, t_start=TARGET_START, t_height=TARGET_HEIGHT, t_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    spectrogram = generate_spectrogram(file, sample_rate=sample_rate, fps=fps)
    peaks, peaks_x, peaks_y = generate_starmap(spectrogram, footprint=footprint, peak_threshold=peak_threshold)
    fingerprint = get_hashes(spectrogram, peaks, track_id, t_start=t_start, t_height=t_height, t_width=t_width, fps=fps)
    return fingerprint

def generate_ordered_fingerprint(file, track_length, peak_factor=PEAK_FACTOR, track_id=None, sample_rate= SAMPLE_RATE, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, t_start=TARGET_START, t_height=TARGET_HEIGHT, t_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    spectrogram = generate_spectrogram(file, sample_rate=sample_rate, fps=fps)
    peaks, peaks_x, peaks_y = generate_starmap(spectrogram, footprint=footprint, peak_threshold=peak_threshold)
    fingerprint = get_hashes(spectrogram, peaks, track_id, t_start=t_start, t_height=t_height, t_width=t_width, fps=fps)
    return fingerprint

def add_fingerprint_to_db(file, track_length, peak_factor=PEAK_FACTOR, db_name=DB, collection_name=COLLECTION, track_id=None, sample_rate= SAMPLE_RATE, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, t_start=TARGET_START, t_height=TARGET_HEIGHT, t_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    collection = get_collection(db_name=db_name, collection_name=collection_name)
    if collection.find_one({"track_id": track_id}):
        print("Error: collection "+collection_name+" already contains track id "+str(track_id))
        return
    
    fingerprint = generate_ordered_fingerprint(file, track_length, peak_factor=peak_factor, track_id=track_id, sample_rate=sample_rate, footprint=footprint, fps=fps, t_start=t_start, t_height=t_height, t_width=t_width, peak_threshold=peak_threshold)
    if len(fingerprint) > 1:
        collection.insert_many(fingerprint)

def match_fingerprint(fingerprint, collection):
    time_ds = {}  # times from start of tracks to start of sample clip

    # calculate time_d of each db hash that matches a sample hash
    for f_hash in fingerprint:
        for db_hash in collection.find({"hash": f_hash["hash"]}):
            if db_hash["time_d"] - f_hash["time_d"] > 0 and db_hash["time_d"] - f_hash["time_d"] < TARGET_WIDTH * FRAMES_PER_SECOND: ##SORT THIS OUT
                if db_hash["track_id"] not in time_ds:
                    time_ds[db_hash["track_id"]] = []
                time_ds[db_hash["track_id"]].append(db_hash["time_d"] - f_hash["time_d"])

    # initialise dictionary to store count of largest bin of time_ds as percentage for each db track
    match_results = {}
    for key in time_ds:
        match_results[key] = 0

    # generate histogram of time_ds for each db track and calculate majority bin (as percentage)
    if len(match_results) > 1:
        # generate histograms
        fig, figs = plt.subplots(1, len(time_ds), sharex=True, sharey=True)
        for i, key in zip(range(len(figs)), time_ds.keys()):
            figs[i].set_title("Track "+str(key))
            n, bins, patches = figs[i].hist(time_ds[key])
            if not math.isnan(max(n)):
                match_results[key] = max(n)

        best_match = 0
        result = 0
        for key in match_results.keys():
            if match_results[key] > best_match:
                best_match = match_results[key]
                result = key
    elif len(match_results) == 1:  # only one track with matching hash(es)
        result = match_results.popitem()[0]
    else:
        result = 0
    
    return result

def match_from_file(file, db_name=DB, collection_name=COLLECTION, sample_rate=SAMPLE_RATE, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, t_start=TARGET_START, t_height=TARGET_HEIGHT, t_width=TARGET_WIDTH):
    fingerprint = generate_fingerprint(file, sample_rate=sample_rate, footprint=footprint, fps=fps, t_start=t_start, t_height=t_height, t_width=t_width)
    collection = get_collection(db_name=db_name, collection_name=collection_name)
    return match_fingerprint(fingerprint, collection)
