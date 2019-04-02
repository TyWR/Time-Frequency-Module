"""
=================================================================================
                                    read

This file contains several functions to read different types of files.
=================================================================================
"""

def xyz_to_montage(path) :
    """Reads and convert xyz positions to a mne montage type"""
    from mne.channels import Montage
    import numpy as np

    n = int(open(path).readline().split(' ')[0])
    coord = np.loadtxt(path, skiprows = 1, usecols = (0,1,2), max_rows = n)
    names = np.loadtxt(path, skiprows = 1, usecols = 3, max_rows = n, dtype = np.dtype(str)).tolist()
    return Montage(coord, names, 'standard_1005', selection = [i for i in range(n)])

def float_(value) :
    """float with handle of none values"""
    if value is None :
        return None
    else :
        return float(value)

def int_(value) :
    """int with handle of none values"""
    if value is None :
        return None
    else :
        return int(value)
