import traceback
from datetime import datetime
from typing import Tuple, Optional, Dict, Any

import librosa
import numpy as np
import soundfile as sf
import sounddevice as sd

def record(fs: int, duration: float, channels: int = 1, bit_depth: int = 16) -> Tuple[Optional[np.ndarray], Optional[int], Optional[str]]:
    """
    Record audio from the default microphone and save to a WAV file.
    
    This function records audio for a specified duration and saves it as a WAV file
    with a timestamped filename. The recording uses the system's default audio input.
    
    Parameters:
    -----------
    fs : int
        Sampling frequency in Hz (e.g., 44100, 48000)
    duration : float
        Recording duration in seconds (must be positive)
    channels : int, optional
        Number of audio channels (1 for mono, 2 for stereo). Default is 1.
    bit_depth : int, optional
        Bit depth for recording (16, 24, or 32). Default is 16.
        
    Returns:
    --------
    audio_data : numpy.ndarray or None
        Recorded audio data as numpy array. Returns None if recording fails.
    fs : int or None
        Sampling frequency. Returns None if recording fails.
    file_name : str or None
        Name of the saved WAV file. Returns None if recording fails.
        
    Raises:
    -------
    ValueError
        If input parameters are invalid
    RuntimeError
        If recording fails due to hardware or permission issues
        
    Examples:
    ---------
    >>> audio, fs, filename = record(44100, 5.0)  # Record 5 seconds at 44.1kHz
    >>> audio, fs, filename = record(48000, 3.0, channels=2, bit_depth=24)
    """
    # Input validation
    if not isinstance(fs, int) or fs <= 0:
        raise ValueError(f"Sampling frequency must be a positive integer, got {fs}")
    
    if not isinstance(duration, (int, float)) or duration <= 0:
        raise ValueError(f"Duration must be a positive number, got {duration}")
    
    if channels not in [1, 2]:
        raise ValueError(f"Channels must be 1 (mono) or 2 (stereo), got {channels}")
    
    # Bit depth to dtype mapping
    bit_depth_map: Dict[int, str] = {
        16: 'int16',
        24: 'int32',  # 24-bit is typically stored in 32-bit containers
        32: 'float32'
    }
    
    if bit_depth not in bit_depth_map:
        raise ValueError(f"Bit depth must be 16, 24, or 32, got {bit_depth}")
    
    dtype = bit_depth_map[bit_depth]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"record_{timestamp}.wav"
    
    try:
        # User prompt for recording
        input(f"Recording the word ({duration} second(s) only)... Press Enter to start recording...")
        print('Start recording...', end='', flush=True)
        
        # Record audio
        audio_data = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=channels,
            dtype=dtype
        )
        
        # Wait for recording to complete
        sd.wait()
        print(" Recording complete!")
        
        # Validate recorded data
        if audio_data is None or audio_data.size == 0:
            raise RuntimeError("No audio data was recorded")
        
        # Determine appropriate subtype for soundfile based on bit depth
        subtype_map = {
            16: 'PCM_16',
            24: 'PCM_24',
            32: 'FLOAT'
        }
        subtype = subtype_map.get(bit_depth, 'PCM_16')
        
        # Save to file
        sf.write(file_name, audio_data, fs, subtype=subtype)
        print(f"Audio saved as: {file_name}")
        
        return audio_data, fs, file_name
        
    except sd.PortAudioError as e:
        print(f"\n[record] Audio device error: {e}")
        print("Please check your microphone connection and permissions.")
        return None, None, None
        
    except sf.LibsndfileError as e:
        print(f"\n[record] File saving error: {e}")
        print("Could not save audio file. Check file permissions and disk space.")
        return None, None, None
        
    except KeyboardInterrupt:
        print("\n\n[record] Recording cancelled by user")
        return None, None, None
        
    except Exception as e:
        print(f"\n[record] Unexpected error: {e}")
        print("Traceback:")
        traceback.print_exc()
        return None, None, None


def load_audio(file_name: str, fs: Optional[int] = None) -> Tuple[np.ndarray, int]:
    """
    Load audio from a file using librosa.
    
    This function loads audio data from various file formats and resamples
    to the target sampling rate if specified.
    
    Parameters:
    -----------
    file_name : str
        Path to the audio file to load
    fs : int, optional
        Target sampling frequency in Hz. If None, uses the file's native sampling rate.
        
    Returns:
    --------
    y : numpy.ndarray
        Audio time series as a 1D numpy array (mono) or 2D array (multi-channel)
    sr : int
        Actual sampling rate of the loaded audio
        
    Raises:
    -------
    FileNotFoundError
        If the specified audio file doesn't exist
    ValueError
        If the file cannot be read as audio or parameters are invalid
    RuntimeError
        If audio loading fails for other reasons
        
    Examples:
    ---------
    >>> audio, sr = load_audio("recording.wav")  # Load with native sampling rate
    >>> audio, sr = load_audio("song.mp3", 22050)  # Load and resample to 22.05kHz
    """
    # Input validation
    if not isinstance(file_name, str) or not file_name.strip():
        raise ValueError("File name must be a non-empty string")
    
    if fs is not None and (not isinstance(fs, int) or fs <= 0):
        raise ValueError(f"Sampling frequency must be a positive integer or None, got {fs}")
    
    try:
        # Load audio file
        y, sr = librosa.load(file_name, sr=fs, mono=False)
        
        # Validate loaded data
        if y is None or y.size == 0:
            raise ValueError(f"Loaded audio data is empty from file: {file_name}")
        
        print(f"Successfully loaded audio: {file_name}")
        print(f"  Duration: {len(y) / sr:.2f} seconds")
        print(f"  Sampling rate: {sr} Hz")
        print(f"  Channels: {1 if y.ndim == 1 else y.shape[0]}")
        print(f"  Samples: {y.size}")
        
        return y, sr
        
    except FileNotFoundError:
        error_msg = f"Audio file not found: {file_name}"
        print(f"\n[load_audio] File not found: {error_msg}")
        raise FileNotFoundError(error_msg)
        
    except sf.LibsndfileError as e:
        error_msg = f"Error reading audio file {file_name}: {e}"
        print(f"\n[load_audio] File reading error: {error_msg}")
        raise ValueError(error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected error loading audio file {file_name}: {e}"
        print(f"\n[load_audio] Unexpected error: {error_msg}")
        print("Traceback:")
        traceback.print_exc()
        raise RuntimeError(error_msg)


def list_audio_devices() -> None:
    """
    List all available audio devices on the system.
    
    This helper function displays information about available audio input
    and output devices, which can be useful for debugging recording issues.
    """
    try:
        print("Available audio devices:")
        print("-" * 50)
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"{i}: {device['name']} "
                      f"(Inputs: {device['max_input_channels']}, "
                      f"Sample Rate: {device['default_samplerate']})")
    except Exception as e:
        print(f"Error querying audio devices: {e}")


def validate_recording_parameters(fs: int, duration: float, channels: int, bit_depth: int) -> bool:
    """
    Validate recording parameters before starting recording.
    
    Parameters:
    -----------
    fs : int
        Sampling frequency
    duration : float
        Recording duration
    channels : int
        Number of channels
    bit_depth : int
        Bit depth
        
    Returns:
    --------
    bool
        True if parameters are valid, False otherwise
    """
    try:
        # Check if default input device exists and has sufficient channels
        default_device = sd.query_devices(kind='input')
        if default_device['max_input_channels'] < channels:
            print(f"Warning: Default input device only supports "
                  f"{default_device['max_input_channels']} channels, but {channels} requested.")
            return False
        
        # Check if sampling rate is supported
        supported_rates = [8000, 11025, 16000, 22050, 44100, 48000, 96000]
        if fs not in supported_rates:
            print(f"Warning: Sampling rate {fs} Hz may not be supported by all devices.")
            print(f"Common rates: {supported_rates}")
        
        # Estimate file size
        estimated_size_mb = (fs * duration * channels * bit_depth) / (8 * 1024 * 1024)
        if estimated_size_mb > 100:  # 100MB threshold
            print(f"Warning: Estimated file size is {estimated_size_mb:.1f} MB")
        
        return True
        
    except sd.PortAudioError as e:
        print(f"Cannot validate parameters: Audio system error - {e}")
        return False
