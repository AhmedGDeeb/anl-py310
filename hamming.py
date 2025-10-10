from math import pi, cos
from typing import List, Optional

# Module-level cache to store computed Hamming windows
_cache = {}

def hamming_window(N: int) -> List[float]:
    """
    Generate a Hamming window of length N.
    
    The Hamming window is defined by:
    w(n) = 0.54 - 0.46 * cos(2πn / (N-1))
    
    Args:
        N: Window length (number of samples). Must be positive integer.
        
    Returns:
        List of float: Hamming window coefficients of length N.
        
    Raises:
        ValueError: If N is not a positive integer.
        TypeError: If N is not an integer.
        
    Examples:
        >>> hamming_window(4)
        [0.08, 0.54, 0.54, 0.08]
        
        >>> hamming_window(1)
        [1.0]
    """
    # Input validation
    if not isinstance(N, int):
        raise TypeError(f"Window length N must be an integer, got {type(N).__name__}")
    
    if N <= 0:
        raise ValueError(f"Window length N must be positive, got {N}")
    
    # Return cached result if available
    if N in _cache:
        return _cache[N]
    
    # Special case: window of length 1
    if N == 1:
        window = [1.0]
    else:
        window = []
        for n in range(N):
            # Hamming window formula
            coefficient = 0.54 - 0.46 * cos(2 * pi * n / (N - 1))
            window.append(coefficient)
    
    # Cache the result for future use
    _cache[N] = window
    
    return window

def apply_hamming_window(signal: List[float]) -> Optional[List[float]]:
    """
    Apply Hamming window to a signal.
    
    Multiplies each element of the input signal by the corresponding
    Hamming window coefficient.
    
    Args:
        signal:  list of Input signal samples
        
    Returns:
        List of float: Windowed signal, or None if input signal is empty.
        
    Raises:
        TypeError: If signal is not a list or contains non-numerical values.
        ValueError: If signal is empty.
        
    Examples:
        >>> apply_hamming_window([1, 2, 3, 4])
        [0.08, 1.08, 1.62, 0.32]
        
        >>> apply_hamming_window([])
        None
    """
    # Input validation
    if not isinstance(signal, list):
        raise TypeError(f"Signal must be a list, got {type(signal).__name__}")
    
    if len(signal) == 0:
        return None
    
    # Get Hamming window of appropriate length
    N = len(signal)
    try:
        window = hamming_window(N)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Failed to generate Hamming window for signal length {N}: {e}")
    
    # Apply window to signal
    windowed_signal = []
    for i in range(N):
        windowed_signal.append(signal[i] * window[i])
    
    return windowed_signal

def clear_cache() -> None:
    """
    Clear the Hamming window cache.
    
    This function can be used to free memory or reset the cache
    for testing purposes.
    
    Examples:
        >>> clear_cache()
        >>> len(_cache)
        0
    """
    _cache.clear()

def get_cache_size() -> int:
    """
    Get the number of cached Hamming windows.
    
    Returns:
        int: Number of cached window configurations.
        
    Examples:
        >>> get_cache_size()
        3
    """
    return len(_cache)