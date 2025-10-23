import cmath
from typing import List, Union, Optional

def fft(x: List[complex], N: Optional[int] = None) -> List[complex]:
    """
    Compute the Fast Fourier Transform (FFT) of a 1D complex-valued input array.
    
    Args:
        x: List of complex numbers (input signal)
        N: Number of points in the output FFT. If None, uses input length.
                     If larger than input length, zero-padding is applied.
                     If smaller than input length, input is truncated.
    
    Returns:
        List of complex numbers (frequency domain representation) with length = output_points
    
    Raises:
        ValueError: If input length is not a power of 2 after adjustment
        TypeError: If input contains non-complex values
    """
    # Input validation
    if not all(isinstance(val, complex) for val in x):
        raise TypeError("All input elements must be complex numbers")
    
    if len(x) == 0:
        raise ValueError("Input signal cannot be empty")
    
    # Handle output points specification
    if N is None:
        N = len(x)
    elif N <= 0:
        raise ValueError(f"N must be positive, got {N}")
    
    # Adjust input length to match output_points requirement
    current_length = len(x)
    
    if N > current_length:
        # Zero-padding
        x_padded = x + [complex(0, 0)] * (N - current_length)
    elif N < current_length:
        # Truncation
        x_padded = x[:N]
    else:
        # No change needed
        x_padded = x

    n = N

    # Check if n is a power of 2
    if n & (n - 1) != 0:
        raise ValueError(f"Output length {n} must be a power of 2 for FFT algorithm")
    
    # Base case: if the input size is 1, return the input
    if n == 1:
        return x_padded
    
    # Split into even and odd indices
    even = fft(x_padded[0::2], N=None)  # Even indices: 0, 2, 4, ...
    odd = fft(x_padded[1::2], N=None)   # Odd indices: 1, 3, 5, ...
    
    # Combine results
    result = [complex(0, 0)] * n
    for k in range(n // 2):
        # Twiddle factor: e^(-2πi*k/n)
        twiddle = cmath.exp(-2j * cmath.pi * k / n)
        
        # Butterfly operation
        result[k] = even[k] + twiddle * odd[k]
        result[k + n // 2] = even[k] - twiddle * odd[k]
    
    return result


def fft_real(signal: List[Union[int, float]], 
             N: Optional[int] = None) -> List[float]:
    """
    Compute FFT for real-valued input with flexible input and output points.
    
    Args:
        signal: List of real numbers (input signal)
        N: Number of points in the output FFT. If None, uses input_points.
                     Must be a power of 2.
    
    Returns:
        List of complex numbers (frequency domain representation) with length = output_points
    
    Raises:
        ValueError: If input parameters are invalid
        TypeError: If input contains non-numerical values
    """
    # Input validation
    if len(signal) == 0:
        raise ValueError("Input signal cannot be empty")
    
    if not all(isinstance(val, (int, float)) for val in signal):
        raise TypeError("All input elements must be numerical values (int or float)")
    
    # Handle input points specification
    input_points = len(signal)
    if input_points <= 0:
        raise ValueError(f"signal must not be empty, got {input_points} samples")
    
    if input_points < N:
        # Zero-padding at the end
        x_adjusted = signal + [0.0] * (input_points - N)
    elif input_points > N:
        # Truncation
        x_adjusted = signal[:input_points]
    else:
        # No change needed
        x_adjusted = signal
    
    # Convert to complex
    x_complex = [complex(val, 0.0) for val in x_adjusted]
    
    # Compute FFT with specified output points
    complex_fft = fft(x_complex, N)

    # calculate magnitude for each point and return
    return [(i.imag**2 + i.real**2)**0.5 for i in complex_fft]

    


