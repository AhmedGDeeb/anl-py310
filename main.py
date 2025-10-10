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
from autocorrelation import fi_correlation, correlations

f0_alif, phi_alif, k_alif = fi_correlation(alif_window, fs, 1)
f0_waw, phi_waw, k_waw = fi_correlation(waw_window, fs, 1)
f0_ya, phi_ya, k_ya = fi_correlation(ya_window, fs, 1)

# show results
print(f"""
# fundemental frequency - f0 (Hz):
--------------------------------------
            f0 (Hz)    Ti (sec)
    Alif    {round(f0_alif, 2):5}     {phi_alif}
    Waw     {round(f0_waw, 2):5}     {phi_waw}
    Ya      {round(f0_ya, 2):5}     {phi_ya}
--------------------------------------
""")

# plot correlations
corr_alif = correlations(alif_window)
corr_waw = correlations(waw_window)
corr_ya = correlations(ya_window)

from plot import plot_subplots
plot_subplots(
    "alif_corr_" + file_name, 
    [
        {'data': [i for i in range(len(alif_window))],},
        {'data': [i / fs for i in range(-len(corr_alif)//2+1, len(corr_alif)//2+1)],},
    ], 
    [
        {'data': alif_window, 'title': 'Alif Sample Window', 'grid': True},
        {'data': corr_alif, 'title': 'Alif Sample Correlation', 'grid': True},
    ]
)

plot_subplots(
    "waw_corr_" + file_name, 
    [
        {'data': [i for i in range(len(waw_window))],},
        {'data': [i / fs for i in range(-len(corr_waw)//2+1, len(corr_waw)//2+1)],},
    ], 
    [
        {'data': waw_window, 'title': 'Waw Sample Window', 'grid': True},
        {'data': corr_waw, 'title': 'Waw Sample Correlation', 'grid': True},
    ]
)

plot_subplots(
    "ya_corr_" + file_name, 
    [
        {'data': [i for i in range(len(ya_window))],},
        {'data': [i / fs for i in range(-len(corr_ya)//2+1, len(corr_ya)//2+1)],},
    ], 
    [
        {'data': ya_window, 'title': 'Ya Sample Window', 'grid': True},
        {'data': corr_ya, 'title': 'Ya Sample Correlation', 'grid': True},
    ]
)
# --------------------------------------------------------------
# step 03: hamming
from hamming import hamming_window, apply_hamming_window
from plot import plot_subplots

# Generate Hamming window - raise error if generation fails
ham = hamming_window(window_length)
if ham is None:
    raise ValueError(f"Hamming window generation failed for window length: {window_length}")

# Alif
# ------------------------------------
# Apply Hamming window to the signal - raise error if application fails
alif_hamming = apply_hamming_window(alif_window)
if alif_hamming is None:
    raise ValueError(f"Hamming window application failed for signal of length: {len(alif_window)}")

# Create x-axis ranges for each subplot
# Center the x-axis around zero for better visualization
x_axis_alif = [i for i in range(-len(alif_window)//2, len(alif_window)//2)]
x_axis_ham = [i for i in range(-len(ham)//2, len(ham)//2)]
x_axis_result = [i for i in range(-len(alif_hamming)//2, len(alif_hamming)//2)]

# Generate subplots to visualize the signal processing steps
plot_subplots(
    "alif_hamming_" + file_name, 
    [
        {'data': x_axis_alif,},      # X-axis for original signal
        {'data': x_axis_ham,},       # X-axis for Hamming window
        {'data': x_axis_result,},    # X-axis for windowed result
    ], 
    [
        {'data': alif_window, 'title': 'Alif Sample Window', 'grid': True},        # Original signal
        {'data': ham, 'title': 'Hamming Window', 'grid': True},               # Hamming window coefficients
        {'data': alif_hamming, 'title': 'Sample × Hamming', 'grid': True},    # Windowed signal result
    ]
)

# Waw
# ------------------------------------
# Apply Hamming window to the signal - raise error if application fails
waw_hamming = apply_hamming_window(waw_window)
if waw_hamming is None:
    raise ValueError(f"Hamming window application failed for signal of length: {len(waw_window)}")

# Create x-axis ranges for each subplot
# Center the x-axis around zero for better visualization
x_axis_alif = [i for i in range(-len(waw_window)//2, len(waw_window)//2)]
x_axis_ham = [i for i in range(-len(ham)//2, len(ham)//2)]
x_axis_result = [i for i in range(-len(waw_hamming)//2, len(waw_hamming)//2)]

# Generate subplots to visualize the signal processing steps
plot_subplots(
    "waw_hamming_" + file_name, 
    [
        {'data': x_axis_alif,},      # X-axis for original signal
        {'data': x_axis_ham,},       # X-axis for Hamming window
        {'data': x_axis_result,},    # X-axis for windowed result
    ], 
    [
        {'data': waw_window, 'title': 'Waw Sample Window', 'grid': True},        # Original signal
        {'data': ham, 'title': 'Hamming Window', 'grid': True},               # Hamming window coefficients
        {'data': waw_hamming, 'title': 'Waw Sample × Hamming', 'grid': True},    # Windowed signal result
    ]
)

# Ya
# ------------------------------------
# Apply Hamming window to the signal - raise error if application fails
ya_hamming = apply_hamming_window(ya_window)
if ya_hamming is None:
    raise ValueError(f"Hamming window application failed for signal of length: {len(ya_window)}")

# Create x-axis ranges for each subplot
# Center the x-axis around zero for better visualization
x_axis_alif = [i for i in range(-len(ya_window)//2, len(ya_window)//2)]
x_axis_ham = [i for i in range(-len(ham)//2, len(ham)//2)]
x_axis_result = [i for i in range(-len(ya_hamming)//2, len(ya_hamming)//2)]

# Generate subplots to visualize the signal processing steps
plot_subplots(
    "ya_hamming_" + file_name, 
    [
        {'data': x_axis_alif,},      # X-axis for original signal
        {'data': x_axis_ham,},       # X-axis for Hamming window
        {'data': x_axis_result,},    # X-axis for windowed result
    ], 
    [
        {'data': ya_window, 'title': 'Ya Sample Window', 'grid': True},        # Original signal
        {'data': ham, 'title': 'Hamming Window', 'grid': True},               # Hamming window coefficients
        {'data': ya_hamming, 'title': 'Ya Sample × Hamming', 'grid': True},    # Windowed signal result
    ]
)