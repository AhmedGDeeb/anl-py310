import numpy as np
from scipy.signal import lfilter
from scipy.linalg import toeplitz

def lpc(signal, order):
    # Autocorrelation method to calculate LPC coefficients
    autocorr = np.correlate(signal, signal, mode='full')
    autocorr = list(autocorr[len(autocorr)//2:])  # Keep only positive lags

    R = toeplitz(autocorr[:order])  # Autocorrelation matrix
    r = autocorr[1:order+1]         # Right-hand side vector

    # Solve for LPC coefficients
    lpc_coeffs = np.linalg.solve(R, r)
    lpc_coeffs = np.concatenate(([1], -lpc_coeffs))  # Add leading 1 for filter

    return lpc_coeffs