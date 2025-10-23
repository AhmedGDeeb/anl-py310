def filter(b, a, x):
    """
    MATLAB-style filter function implementation from scratch.
    
    Args:
        b: Numerator coefficients [b0, b1, ..., bM]
        a: Denominator coefficients [a0, a1, ..., aN] (a0 usually = 1)
        x: Input signal
        
    Returns:
        y: Filtered output signal
    """
    # Normalize coefficients so a[0] = 1
    if a[0] != 1:
        b = [bi / a[0] for bi in b]
        a = [ai / a[0] for ai in a]
    
    M = len(b) - 1  # Order of numerator
    N = len(a) - 1  # Order of denominator
    
    # Initialize output and history buffers
    y = [0.0] * len(x)
    x_history = [0.0] * (M + 1)  # x[n], x[n-1], ..., x[n-M]
    y_history = [0.0] * (N + 1)  # y[n], y[n-1], ..., y[n-N]
    
    for n in range(len(x)):
        # Update input history (shift right and add new sample)
        for i in range(M, 0, -1):
            x_history[i] = x_history[i-1]
        x_history[0] = x[n]
        
        # Compute output using difference equation
        # y[n] = sum(b_k * x[n-k]) - sum(a_k * y[n-k]) for k>=1
        output = 0.0
        
        # Feedforward part (b coefficients)
        for k in range(M + 1):
            output += b[k] * x_history[k]
        
        # Feedback part (a coefficients, excluding a[0]=1)
        for k in range(1, N + 1):
            output -= a[k] * y_history[k]
        
        y[n] = output
        
        # Update output history
        for i in range(N, 0, -1):
            y_history[i] = y_history[i-1]
        y_history[0] = output
    
    # multiple by 2 to simulate matlab
    yt = []
    for i in y:
        yt.append(2*i)

    return yt