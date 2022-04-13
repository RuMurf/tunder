from utils.defaults import *
from tqdm import tqdm

def get_hashes(spectrogram, peaks, track_id=None, t_start=TARGET_START, t_height=TARGET_HEIGHT, t_width=TARGET_WIDTH, fps=FRAMES_PER_SECOND):
    print("Generating Fingerprint...")
    frequency_bin_size = spectrogram.bin_frequencies[1]

    t_start = int(t_start * fps)
    t_height = int(t_height//frequency_bin_size)
    t_width = int(t_width * fps)
    fingerprint = []

    for peak in tqdm(peaks):
        try:
            for i in range((peak[0]+t_start), (peak[0]+t_width)):
                for j in range((peak[1]-t_height//2), (peak[1]+t_height//2)):
                    if [i, j] in peaks:
                        fingerprint.append({"hash": str(peak[1])+"-"+str(j)+"-"+str((i - peak[0])), "track_id": track_id, "time_d": peak[0]})
        except IndexError:
            continue
    print("Track "+str(track_id)+" Fingerprint Generated with "+str(len(fingerprint))+" hashes!\n")
    return fingerprint
