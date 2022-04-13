from madmom.audio import Signal
from madmom.audio.signal import FramedSignal
from madmom.audio.spectrogram import Spectrogram
from sys import argv
from utils.defaults import *

def generate_spectrogram(filepath, fps=FRAMES_PER_SECOND):
    print("Generating spectrogram... [fps="+str(fps)+"]")
    signal = Signal(filepath, sample_rate=44100, num_channels=1)
    framed_signal = FramedSignal(signal, fps=fps)
    spectrogram = Spectrogram(framed_signal)
    return spectrogram


if __name__ == "__main__":
    if len(argv) == 2:
        generate_spectrogram(argv[1])
    if len(argv) > 2:
        generate_spectrogram(argv[1], int(argv[2]))
