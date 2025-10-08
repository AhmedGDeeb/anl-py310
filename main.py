import os

import matplotlib.pyplot as plt

# importing configurations
from config import fs, duration, channels, bit_depth

# change this to the path of the test record
# if empty, it will record a new file
file_name = 'record_20251007_142931.wav'
alif_start = 12800
waw_start = 24000
ya_start = 36000

# --------------------------------------------------------------
# step 00: recording audio
from recorder import record, load_audio

# Record the word
if file_name == "" or file_name == None:
    print("You did not specify any file, recording new...")
    audio, fs, file_name = record(fs, duration, channels, bit_depth)
elif not os.path.exists(file_name):
    print(f"File {file_name} does not exist, recording new...")
    audio, fs, file_name = record(fs, duration, channels, bit_depth)
else:
    # file found, continue execution
    pass

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

# --------------------------------------------------------------
# step 00: plot record
time = [i * duration / len(samples) for i in range(len(samples))]
# plot record
plt.figure()
plt.title('Sound Spectrum')
plt.xlabel('Time (s)')  # Changed from ms to seconds
plt.ylabel('Amplitude (dB)')
plt.grid(True)
plt.tight_layout()
plt.plot(
    time,
    samples,
)
plt.savefig(f'{file_name}_spectrum.png', dpi=300, bbox_inches='tight')
plt.show()

# --------------------------------------------------------------
# step 01: extract vowel windows and plot
window_duration_ms = 30
window_length = int(window_duration_ms / 1000 * fs)
print(f"Window length: {window_length} samples, {window_duration_ms} ms")

# extract windows
alif_window = samples[alif_start:alif_start+window_length]
waw_window = samples[waw_start:waw_start+window_length]
ya_window = samples[ya_start:ya_start+window_length]

print(f"""# Windows:
-----------------------------------------------------------
      alif: [{alif_start}:{alif_start+window_length}] samples, [{alif_start/fs*1000:.2f}:{(alif_start+window_length)/fs*1000:.2f}] ms
      waw: [{waw_start}:{waw_start+window_length}] samples, [{waw_start/fs*1000:.2f}:{(waw_start+window_length)/fs*1000:.2f}] ms
      ya: [{ya_start}:{ya_start+window_length}] samples, [{ya_start/fs*1000:.2f}:{(ya_start+window_length)/fs*1000:.2f}] ms
-----------------------------------------------------------
""")

# Alif
plt.figure()
plt.title('Alif Window')
plt.xlabel('Sample index')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.plot(
    [i for i in range(alif_start, alif_start+window_length)],
    alif_window
)
plt.savefig(f'alif_window_{file_name}.png')
plt.show()

# Waw
plt.figure()
plt.title('Waw Window')
plt.xlabel('Sample index')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.plot(
    [i for i in range(waw_start, waw_start+window_length)],
    waw_window
)
plt.savefig(f'waw_window_{file_name}.png')
plt.show()

# Ya
plt.figure()
plt.title('Ya Window')
plt.xlabel('Sample index')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.plot(
    [i for i in range(ya_start, ya_start+window_length)],
    ya_window
)
plt.savefig(f'ya_window_{file_name}.png')
plt.show()

# --------------------------------------------------------------
# step 02: f0 - fundemental period
from autocorrelation import fi_correlation

f0_alif, phi_alif, k_alif = fi_correlation(alif_window, fs, 1)
f0_waw, phi_waw, k_waw = fi_correlation(waw_window, fs, 1)
f0_ya, phi_ya, k_ya = fi_correlation(ya_window, fs, 1)

print(f"""
# fundemental frequency - f0 (Hz):
--------------------------------------
            f0 (Hz)    Ti (sec)
    Alif    {round(f0_alif, 2):5}     {phi_alif}
    Waw     {round(f0_waw, 2):5}     {phi_waw}
    Ya      {round(f0_ya, 2):5}     {phi_ya}
--------------------------------------
""")
