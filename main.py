import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter
import tkinter as tk

# Audio Settings
sample_rate = 44100
block_size = 1024

# Global parameters
gain = 1.0
bass_gain = 1.0
mid_gain = 1.0
treble_gain = 1.0

# Filter Design
def butter_filter(cutoff, fs, btype):
    return butter(2, np.array(cutoff)/(fs/2), btype=btype)

b_low, a_low = butter_filter(200, sample_rate, 'low')
b_mid, a_mid = butter_filter([200, 2000], sample_rate, 'band')
b_high, a_high = butter_filter(2000, sample_rate, 'high')

# Audio Processing
def process_audio(indata, outdata, frames, time, status):
    global gain, bass_gain, mid_gain, treble_gain

    audio = indata[:, 0]

    bass = lfilter(b_low, a_low, audio) * bass_gain
    mid = lfilter(b_mid, a_mid, audio) * mid_gain
    treble = lfilter(b_high, a_high, audio) * treble_gain

    mixed = (bass + mid + treble) * gain

    outdata[:, 0] = mixed
    outdata[:, 1] = mixed

# Start Audio Stream
stream = sd.Stream(channels=2,
                   samplerate=sample_rate,
                   blocksize=block_size,
                   callback=process_audio)
stream.start()

# GUI Setup
root = tk.Tk()
root.title("DSP Live Mixer")

def update_gain(val):
    global gain
    gain = float(val)

def update_bass(val):
    global bass_gain
    bass_gain = float(val)

def update_mid(val):
    global mid_gain
    mid_gain = float(val)

def update_treble(val):
    global treble_gain
    treble_gain = float(val)

# Sliders
tk.Label(root, text="Gain").pack()
tk.Scale(root, from_=0, to=2, resolution=0.1, orient="horizontal", command=update_gain).pack()

tk.Label(root, text="Bass").pack()
tk.Scale(root, from_=0, to=2, resolution=0.1, orient="horizontal", command=update_bass).pack()

tk.Label(root, text="Mid").pack()
tk.Scale(root, from_=0, to=2, resolution=0.1, orient="horizontal", command=update_mid).pack()

tk.Label(root, text="Treble").pack()
tk.Scale(root, from_=0, to=2, resolution=0.1, orient="horizontal", command=update_treble).pack()

root.mainloop()