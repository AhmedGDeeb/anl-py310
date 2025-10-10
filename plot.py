import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Union, Any

def plot_subplots(file_name: Optional[str], x: List[Dict], y: List[Dict]) -> None:
    """
    Create multiple subplots with customizable properties for each subplot.
    
    This function creates a vertical stack of subplots where each subplot can have
    individual titles, labels, grid settings, and data.
    
    Parameters:
    -----------
    file_name : str or None
        If provided, saves the plot as a PNG file with the given name.
        If None, the plot is only displayed.
    x : List[Dict]
        List of dictionaries containing x-axis data and properties for each subplot.
        Each dictionary should contain:
        - 'data': array-like data for x-axis
        - Optional: 'grid', 'x_label'
    y : List[Dict]
        List of dictionaries containing y-axis data and properties for each subplot.
        Each dictionary should contain:
        - 'data': array-like data for y-axis
        - Optional: 'title', 'ylabel', 'grid', 'x_label'
        
    Raises:
    -------
    ValueError
        If x and y lists have different lengths
        If required 'data' keys are missing
    TypeError
        If inputs are not of expected types
        
    Examples:
    ---------
    >>> x_data = [{'data': time1}, {'data': time2, 'grid': True}]
    >>> y_data = [
    ...     {'data': amplitude1, 'title': 'Signal 1', 'ylabel': 'Amplitude'},
    ...     {'data': amplitude2, 'title': 'Signal 2', 'grid': True}
    ... ]
    >>> plot_subplots("my_plot", x_data, y_data)
    """
    # Input validation
    if not isinstance(x, list) or not isinstance(y, list):
        raise TypeError("x and y must be lists of dictionaries")
    
    if len(x) != len(y):
        raise ValueError(f"x and y must be the same length. Got x: {len(x)}, y: {len(y)}")
    
    if len(x) == 0:
        raise ValueError("x and y lists cannot be empty")
    
    # Validate each subplot data
    for i, (x_dict, y_dict) in enumerate(zip(x, y)):
        if not isinstance(x_dict, dict) or not isinstance(y_dict, dict):
            raise TypeError(f"All elements in x and y must be dictionaries. Index: {i}")
        
        if 'data' not in x_dict:
            raise ValueError(f"x[{i}] must contain 'data' key")
        if 'data' not in y_dict:
            raise ValueError(f"y[{i}] must contain 'data' key")
        
        # Check data lengths match
        if len(x_dict['data']) != len(y_dict['data']):
            raise ValueError(f"Data length mismatch at index {i}. "
                           f"x: {len(x_dict['data'])}, y: {len(y_dict['data'])}")

    try:
        # Create subplots
        fig, axes = plt.subplots(len(y), 1, figsize=(12, 10))
        
        # Handle single subplot case (axes is not a list)
        if len(y) == 1:
            axes = [axes]
        
        # Plot each subplot
        for i, (x_dict, y_dict) in enumerate(zip(x, y)):
            axes[i].plot(x_dict['data'], y_dict['data'])
            
            # Apply properties from y_dict
            if 'title' in y_dict:
                axes[i].set_title(y_dict['title'])
            if 'ylabel' in y_dict:
                axes[i].set_ylabel(y_dict['ylabel'])
            
            # Apply grid settings (y_dict takes precedence over x_dict)
            grid_enabled = False
            if 'grid' in y_dict:
                grid_enabled = y_dict['grid']
            elif 'grid' in x_dict:
                grid_enabled = x_dict['grid']
            
            if grid_enabled:
                axes[i].grid(True)
            
            # Apply x-label (from y_dict with fallback to x_dict)
            if 'x_label' in y_dict:
                axes[i].set_xlabel(y_dict['x_label'])
            elif 'x_label' in x_dict:
                axes[i].set_xlabel(x_dict['x_label'])

        plt.tight_layout()
        
        # Save if file_name provided
        if file_name is not None:
            if not isinstance(file_name, str):
                raise TypeError("file_name must be a string or None")
            plt.savefig(f'plot_subplots_{file_name}.png', dpi=300, bbox_inches='tight')
        
        plt.show()
        
    except Exception as e:
        plt.close('all')  # Clean up any created figures
        raise RuntimeError(f"Error creating subplots: {str(e)}") from e


def plot_multiple(file_name: Optional[str], x: Dict, y: List[Dict]) -> None:
    """
    Plot multiple datasets on a single plot with customizable properties.
    
    This function creates a single plot with multiple lines, each with potential
    custom colors, labels, and styling.
    
    Parameters:
    -----------
    file_name : str or None
        If provided, saves the plot as a PNG file with the given name.
        If None, the plot is only displayed.
    x : Dict
        Dictionary containing x-axis data and properties.
        Should contain:
        - 'data': array-like data for x-axis
        - Optional: 'title', 'x_label'
    y : List[Dict]
        List of dictionaries containing y-axis data and properties for each line.
        Each dictionary should contain:
        - 'data': array-like data for y-axis
        - Optional: 'color', 'label', 'grid'
        
    Raises:
    -------
    ValueError
        If required 'data' keys are missing
        If data lengths don't match
    TypeError
        If inputs are not of expected types
        
    Examples:
    ---------
    >>> x_data = {'data': time, 'title': 'Multiple Signals', 'x_label': 'Time (ms)'}
    >>> y_data = [
    ...     {'data': signal1, 'color': 'red', 'label': 'Signal 1'},
    ...     {'data': signal2, 'color': 'blue', 'label': 'Signal 2', 'grid': True}
    ... ]
    >>> plot_multiple("comparison", x_data, y_data)
    """
    # Input validation
    if not isinstance(x, dict):
        raise TypeError("x must be a dictionary")
    if not isinstance(y, list):
        raise TypeError("y must be a list of dictionaries")
    
    if 'data' not in x:
        raise ValueError("x must contain 'data' key")
    
    if len(y) == 0:
        raise ValueError("y list cannot be empty")
    
    # Validate each dataset
    for i, y_dict in enumerate(y):
        if not isinstance(y_dict, dict):
            raise TypeError(f"All elements in y must be dictionaries. Index: {i}")
        if 'data' not in y_dict:
            raise ValueError(f"y[{i}] must contain 'data' key")
        
        # Check data lengths match
        if len(x['data']) != len(y_dict['data']):
            raise ValueError(f"Data length mismatch at index {i}. "
                           f"x: {len(x['data'])}, y: {len(y_dict['data'])}")

    try:
        # Create single plot
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Apply x-axis properties
        if 'title' in x:
            ax.set_title(x['title'])
        if 'x_label' in x:
            ax.set_xlabel(x['x_label'])
        
        # Plot each dataset
        for i, y_dict in enumerate(y):
            color = y_dict.get('color')
            label = y_dict.get('label')
            
            if color is not None and label is not None:
                ax.plot(x['data'], y_dict['data'], color=color, label=label)
            elif color is not None:
                ax.plot(x['data'], y_dict['data'], color=color)
            elif label is not None:
                ax.plot(x['data'], y_dict['data'], label=label)
            else:
                ax.plot(x['data'], y_dict['data'])
            
            # Apply grid settings (last one wins)
            if 'grid' in y_dict:
                ax.grid(y_dict['grid'])
        
        # Add legend if any labels were provided
        has_labels = any('label' in y_dict for y_dict in y)
        if has_labels:
            ax.legend()
        
        plt.tight_layout()
        
        # Save if file_name provided
        if file_name is not None:
            if not isinstance(file_name, str):
                raise TypeError("file_name must be a string or None")
            plt.savefig(f'plot_multiple_{file_name}.png', dpi=300, bbox_inches='tight')
        
        plt.show()
        
    except Exception as e:
        plt.close('all')  # Clean up any created figures
        raise RuntimeError(f"Error creating multiple plot: {str(e)}") from e