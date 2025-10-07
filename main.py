import os


import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal.windows import hamming
from scipy.signal import lfilter, find_peaks, freqz 

# importing configurations
from config import fs, duration, channels, bit_depth

# change this to the path of the test record
# if empty, it will record a new file
file_name = ''
alif_start = None
waw_start = None
ya_start = None

# --------------------------------------------------------------
# step 00: recording audio
from recorder import record
# Record the word
if file_name == "" or file_name == None:
    print("You did not sepcify any file, recording new...")
    audio, fs, file_name = record(fs, duration, channels, bit_depth)
elif not os.path.exists(file_name):
    print(f"File {file_name} does not exist, recoding new...")
    audio, fs, file_name = record(fs, duration, channels, bit_depth)
else:
    # file found, continue execution
    pass

# --------------------------------------------------------------
# step 00: recording audio
from recorder import load_audio
print(f"loading record {file_name}", end="")
print(" Done.")
if fs == 0:
    print(f"Sampling rate (frequency) of the record {file_name} = 0, exit program.")
    exit(-2)

samples, fs = load_audio(file_name, fs)
if len(samples) == 0:
    print(f"{file_name} is empty, exit program.")
    exit(-3)

if not fs > 0:
    print(f"Error loading {file_name}, sampling rate is {fs}, exit program.")
    exit(-4)
duration = len(samples)/fs

print(f"Audio length: {len(samples)} samples")
print(f"Duration: {duration:.2f} seconds")
print(f"Sampling rate (frequency): {fs} Hz")