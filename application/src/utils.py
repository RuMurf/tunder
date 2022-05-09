from madmom.audio.signal import Signal, FramedSignal
from madmom.audio.spectrogram import Spectrogram
from scipy.ndimage import maximum_filter
from pymongo import MongoClient

# Defaults
SAMPLE_RATE = 22050
FOOTPRINT_SIZE = 30
TARGET_START = 0.05
TARGET_HEIGHT = 4000
TARGET_WIDTH = 2
FRAMES_PER_SECOND = 5
PEAK_THRESHOLD = 0
CONNECTION_STRING = "mongodb://localhost:27017"

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

def generate_fingerprint(file, track_id=None, sample_rate= SAMPLE_RATE, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    spectrogram = generate_spectrogram(file, sample_rate=sample_rate, fps=fps)
    peaks, peaks_x, peaks_y = generate_starmap(spectrogram, footprint=footprint, peak_threshold=peak_threshold)
    fingerprint = get_hashes(spectrogram, peaks, track_id, target_start=target_start, target_height=target_height, target_width=target_width, fps=fps)
    return fingerprint

def add_fingerprint_to_db(file, db_name="tunder", collection_name="fingerprints", track_id=None, sample_rate= SAMPLE_RATE, footprint=FOOTPRINT_SIZE, fps=FRAMES_PER_SECOND, target_start=TARGET_START, target_height=TARGET_HEIGHT, target_width=TARGET_WIDTH, peak_threshold=PEAK_THRESHOLD):
    # collection_name = "db-fp="+str(footprint)+",fps="+str(fps)+",t_start="+str(target_start)+",t_height="+str(target_height)+",t_width="+str(target_width)+",p_th="+str(peak_threshold)
    client = MongoClient("mongodb://localhost:27017")
    db = client[db_name]
    collection = db[collection_name]
    if collection.find_one({"track_id": track_id}):
        print("Error: collection "+collection_name+" already contains track id "+str(track_id))
        return
    fingerprint = generate_fingerprint(file, track_id, sample_rate=sample_rate, footprint=footprint, fps=fps, target_start=target_start, target_height=target_height, target_width=target_width, peak_threshold=peak_threshold)
    if len(fingerprint) > 1:
        collection.insert_many(fingerprint)