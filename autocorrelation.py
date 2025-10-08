import numpy as np
from typing import List, Tuple, Optional, Union

def _corr(s: List[float], k: int) -> float:
    """
    Compute the circular autocorrelation of a signal at a given lag.
    
    This helper function calculates the unnormalized circular autocorrelation 
    by shifting the signal and computing the dot product with itself.
    
    Parameters:
    -----------
    s : list or array-like
        Input signal samples
    k : int
        Lag value (can be positive or negative)
        
    Returns:
    --------
    phi : float
        Unnormalized autocorrelation value at lag k
        
    Raises:
    -------
    TypeError: If input is not a list or k is not integer
    ValueError: If signal is empty
    """
    # Input validation
    if not isinstance(s, (list, np.ndarray)):
        raise TypeError(f"Signal must be list or array-like, got {type(s)}")
    if not isinstance(k, int):
        raise TypeError(f"Lag k must be integer, got {type(k)}")
    if len(s) == 0:
        raise ValueError("Signal cannot be empty")
    
    phi = 0.0
    l = len(s)
    for m in range(l):
        phi += s[m] * s[(m + k) % l]  # Circular indexing for periodic signals
    return phi


def correlations(s: List[float]) -> Optional[List[float]]:
    """
    Compute the normalized autocorrelation function of a signal.
    
    Calculates the autocorrelation for lags from -N to +N, where N is half
    the signal length, and normalizes by the number of lags.
    
    Parameters:
    -----------
    s : list or array-like
        Input signal samples
        
    Returns:
    --------
    c : list or None
        List of normalized autocorrelation values for each lag
        Returns None if input signal is too short
        
    Raises:
    -------
    TypeError: If input is not a list or array-like
    ValueError: If signal contains non-numeric values
    """
    # Input validation
    if not isinstance(s, (list, np.ndarray)):
        raise TypeError(f"Signal must be list or array-like, got {type(s)}")
    
    if len(s) == 0:
        return None
        
    # Check for numeric values
    try:
        float(s[0])
    except (TypeError, ValueError):
        raise ValueError("Signal must contain numeric values")
    
    c = []
    N = len(s) // 2  # Maximum lag is half the signal length
    if N == 0:
        return None
    
    try:
        for k in range(-N, N + 1):
            # Normalize by number of lags considered
            ek = (1 / (2 * N + 1)) * _corr(s, k)
            c.append(ek)
    except Exception as e:
        raise RuntimeError(f"Error computing correlations: {str(e)}")
    
    return c


def fi_correlation(s: List[float], fs: float, i: int = 1) -> Tuple[Optional[float], Optional[float], Optional[int]]:
    """
    Estimate the i-th harmonic frequency using autocorrelation peak analysis.
    
    This function analyzes the autocorrelation function to find spectral peaks
    and estimates the frequency of the i-th harmonic component.
    
    Parameters:
    -----------
    s : list or array-like
        Input signal samples
    fs : float
        Sampling frequency in Hz
    i : int, optional
        Harmonic index to estimate (default=1 for fundamental frequency)
        
    Returns:
    --------
    fi : float or None
        Estimated frequency of the i-th harmonic in Hz
    Ti : float or None  
        Estimated period of the i-th harmonic in seconds
    index_peak : int or None
        Lag index difference between the fundamental and i-th harmonic peaks
        Returns (None, None, None) if input is invalid or insufficient peaks
        
    Raises:
    -------
    TypeError: If inputs have incorrect types
    ValueError: If inputs have invalid values
    """
    # Input validation
    if not isinstance(s, (list, np.ndarray)):
        raise TypeError(f"Signal must be list or array-like, got {type(s)}")
    if not isinstance(fs, (int, float)) or fs <= 0:
        raise ValueError(f"Sampling frequency must be positive number, got {fs}")
    if not isinstance(i, int) or i < 0:
        raise ValueError(f"Harmonic index must be non-negative integer, got {i}")
    
    # Explicit conversion to list to ensure indexable sequence
    try:
        s = list(s)  
    except Exception as e:
        raise TypeError(f"Could not convert signal to list: {str(e)}")
    
    # Input validation
    if len(s) == 0:
        return None, None, None
    if fs == 0 or i == 0:
        return None, None, None

    try:
        # Compute autocorrelation function
        c = correlations(s)
        if c is None:
            return None, None, None

        # Extract peaks from autocorrelation function
        peaks = []
        peaks.append(c[0])  # Always include the zero-lag peak (maximum)
        
        # Find local maxima and minima in autocorrelation
        for j in range(1, len(c) - 1):
            # Peak detection: product of slopes changes sign at extrema
            if (c[j - 1] - c[j]) * (c[j] - c[j + 1]) <= 0:
                peaks.append(c[j]) 

        # Check if we have enough peaks for the requested harmonic
        if len(peaks) <= i:  # Changed to <= since we need index i
            return None, None, None
            
        # Sort peaks in descending order (largest correlation first)
        sorted_peaks = sorted(peaks, reverse=True)
        peak_0 = sorted_peaks[0]  # Fundamental frequency peak (largest)
        peak_index = sorted_peaks[i]  # i-th harmonic peak
        
        # Calculate lag difference between fundamental and harmonic
        index_peak = abs(c.index(peak_index) - c.index(peak_0))

        # Convert lag to time and frequency
        Ti = index_peak / fs  # Period in seconds
        fi = 1 / Ti  # Frequency in Hz
        
        return fi, Ti, index_peak
        
    except Exception as e:
        raise RuntimeError(f"Error in frequency estimation: {str(e)}")