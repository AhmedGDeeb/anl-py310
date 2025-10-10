from typing import List

def pre_emphasis_filter(signal: List[float], alpha: float = 0.97) -> List[float]:
    """
    Apply pre-emphasis filter to a signal using the formula: y[t] = x[t] - α*x[t-1]
    
    Pre-emphasis filter enhances high-frequency components and attenuates low-frequency components.
    This is commonly used in speech processing to flatten the spectral envelope.
    
    Args:
        signal: Input signal as list of float values
        alpha: Pre-emphasis coefficient (typically 0.95-0.97 for speech processing)
    
    Returns:
        List[float]: Pre-emphasized signal
    
    Raises:
        ValueError: If alpha is not in range [0, 1] or signal is empty
        TypeError: If signal contains non-numerical values
    """
    # Input validation
    if not isinstance(signal, list):
        raise TypeError(f"Signal must be a list, got {type(signal).__name__}")
    
    if not len(signal):
        raise ValueError("Input signal cannot be empty.")
    
    if not all(isinstance(x, (int, float)) for x in signal):
        raise TypeError("All signal elements must be numerical values (int or float).")
    
    if not 0 <= alpha <= 1:
        raise ValueError(f"Alpha must be between 0 and 1, got {alpha}.")
    
    # Apply pre-emphasis filter: y[t] = x[t] - α*x[t-1]
    pre_emphasized = []
    
    for i in range(len(signal)):
        if i == 0:
            # For the first sample, assume x[-1] = 0
            # So y[0] = x[0] - α*0 = x[0]
            pre_emphasized.append(signal[0])
        else:
            # For all other samples: y[t] = x[t] - α*x[t-1]
            emphasized_value = signal[i] - alpha * signal[i-1]
            pre_emphasized.append(emphasized_value)

    pre_emphasized[0] = pre_emphasized[1]
    
    return pre_emphasized