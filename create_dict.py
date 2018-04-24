import numpy as np


def create_dictionary(model_name, epoch, max_time, max_amp, sites):
    """

    Parameters
    ----------
    model_name: Cascadia
    epoch: time stamp in seconds (earthquake origin)
    max_time: time of the maximum waveheight
    max_amp: value of the maximum waveheight
    sites: lat/lon of all sites

    Returns
    -------
    db_dict: returns the final dict
    """

    db_dict = {}
    db_dict['t'] = epoch
    db_dict['model'] = model_name
    time = np.ndarray.tolist(max_time)
    db_dict['max_time'] = time
    waveheight = np.ndarray.tolist(max_amp)
    db_dict['max_waveheight'] = waveheight
    locs = np.ndarray.tolist(sites)
    db_dict['locations'] = locs
    return(db_dict)